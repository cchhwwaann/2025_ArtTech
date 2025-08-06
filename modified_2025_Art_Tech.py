import os
from google.cloud import language_v1 # Natural Language API 사용을 위한 라이브러리
import vertexai # Gemini Pro (Vertex AI) 사용을 위한 라이브러리
from vertexai.preview.generative_models import GenerativeModel, Part

# machine_controller.py 파일을 임포트합니다.
import machine_controller 

# 1. 서비스 계정 키 파일 경로 설정
# 이 부분은 당신의 실제 다운로드한 키 파일의 경로와 이름으로 변경되어 있어야 합니다.
# Git에 올라가지 않도록 .gitignore 설정은 유지되어야 합니다.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ghksc/Desktop/2025_Art_Tech/smart-mark-464523-g6-6f8d28d38fc0.json"

# --- Google Natural Language API를 사용한 감정 분석 함수 (이전에 누락되었던 부분) ---
def analyze_sentiment_only(text_content):
    """
    주어진 텍스트의 감정과 문장별 감정을 분석합니다.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT, language="ko"
    )

    sentiment_response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )
    
    return sentiment_response

# --- Gemini를 활용한 심리 상담 메시지 생성 함수 ---
def generate_counseling_message_with_gemini(sentiment_data, user_input_text):
    """
    Google Natural Language API의 감정 분석 결과와 사용자 입력을 바탕으로
    Gemini를 사용하여 심리 상담 메시지를 생성합니다.
    """
    
    # 1. Vertex AI 초기화 (당신의 Google Cloud 프로젝트 ID와 지역으로 변경)
    # Gemini Pro 모델은 특정 지역에서만 사용 가능합니다. 'us-central1' 또는 'asia-east1' 등이 일반적입니다.
    project_id = "smart-mark-464523-g6" # <--- 여기에 당신의 실제 프로젝트 ID를 입력하세요!
    location = "us-central1" # <--- Gemini 2.5 flash가 지원되는 지역으로 설정하세요.

    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.5-flash") # Gemini 2.5 flash 모델 지정
    except Exception as e:
        return f"Gemini 모델 초기화 또는 Vertex AI 설정 오류: {e}\nGoogle Cloud 프로젝트 ID와 지역, API 활성화 및 권한을 확인해주세요."

    # 2. 감정 분석 결과 요약 (Gemini에게 전달할 정보)
    # Natural Language API의 결과를 Gemini가 이해하기 쉽게 요약합니다.
    document_sentiment = sentiment_data.document_sentiment
    score = document_sentiment.score
    magnitude = document_sentiment.magnitude

    sentiment_summary = ""
    if score >= 0.5:
        sentiment_summary = f"전반적으로 매우 긍정적이고 밝은 감정({score:.1f}, 강도 {magnitude:.1f})이 느껴집니다."
    elif score <= -0.5:
        sentiment_summary = f"전반적으로 다소 힘든 감정({score:.1f}, 강도 {magnitude:.1f})이 느껴집니다."
    else:
        sentiment_summary = f"복합적이거나 차분한 감정({score:.1f}, 강도 {magnitude:.1f})이 느껴집니다."

    # 문장별 감정 요약 추가 (선택 사항, 프롬프트 길이에 따라 조절)
    sentences_info = []
    for s_info in sentiment_data.sentences[:3]: # 최대 3문장만 요약
        s_score = s_info.sentiment.score if s_info.sentiment and s_info.sentiment.score is not None else 0.0
        s_magnitude = s_info.sentiment.magnitude if s_info.sentiment and s_info.sentiment.magnitude is not None else 0.0
        sentences_info.append(f"'{s_info.text.content}' (감정 점수: {s_score:.1f}, 강도: {s_magnitude:.1f})")
    
    if sentences_info:
        sentiment_summary += "\n\n문장별 감정:\n" + "\n".join(sentences_info)


    # 3. Gemini Pro에게 보낼 프롬프트 작성 (가장 중요한 부분!)
    # 역할 부여, 지시 사항, 금지 사항 등을 명확히 합니다.
    prompt = f"""당신은 사용자의 감정을 섬세하게 이해하고 공감하는 따뜻하고 지지적인 심리 상담가입니다.
    당신은 사용자에게 전문적인 진단이나 의료적 조언, 약물 권유를 절대 하지 않습니다.
    오직 사용자의 감정을 반영하고, 자기 성찰을 돕고, 긍정적인 방향으로 나아갈 수 있도록 격려하는 메시지를 제공합니다.
    사용자의 입력과 감정 분석 결과를 바탕으로 3~5문장으로 친절하고 부드러운 상담 메시지를 생성해주세요. 또한, 사용자가 지금 느끼고 있는 감정이 어떻게 
    발현되었고, 어떻게 변해갈지에 대해서도 설명해주면 좋겠습니다. 전반적으로 사용자가 입력한 감정을 단순히 되풀이하고 해석하는게 아닌, 정말로 사용자 스스로도 몰랐을지 모르는
    사용자의 내면에 관한 고찰이 추가되면 좋겠습니다.

    ---
    사용자 원본 입력: "{user_input_text}"
    감정 분석 결과 요약: "{sentiment_summary}"
    ---

    당신의 상담 메시지:
    """

    # 4. Gemini Pro 모델 호출
    try:
        response = model.generate_content([Part.from_text(prompt)])
        return response.text
    except Exception as e:
        return f"Gemini  API 호출 중 오류가 발생했습니다: {e}\n프롬프트 내용이나 API 사용량 제한 등을 확인해주세요."

# --- 메인 실행 부분 ---
if __name__ == "__main__":
    print("안녕하세요! 전시회 감정 분석 프로그램입니다.")
    print("오늘 당신의 감정을 3문장 이내로 자유롭게 입력해주세요.")
    print("종료하려면 '종료', 'exit', 'quit' 중 하나를 입력해주세요.")
    
    while True:
        user_text = input("\n>>> ")

        if user_text.lower() in ['종료', 'exit', 'quit']:
            print("프로그램을 종료합니다. 참여해주셔서 감사합니다!")
            break

        if not user_text.strip():
            print("텍스트가 입력되지 않았습니다. 다시 입력해주세요.")
            continue

        print("\n당신의 감정을 분석 중입니다... 잠시만 기다려주세요.")
        try:
            # 1. Google Natural Language API로 기본적인 감정 분석 수행
            sentiment_res = analyze_sentiment_only(user_text) # 이제 이 함수가 정의되어 있습니다.
            
            # --- 추출된 score와 magnitude를 기계 제어 함수로 전달 ---
            score = sentiment_res.document_sentiment.score
            magnitude = sentiment_res.document_sentiment.magnitude
            
            # 기계 제어 함수 호출
            # user_input_text도 전달하여 필요하면 기계 제어 로직에서 활용
            calculated_color, calculated_speed_desc, calculated_speed_val = machine_controller.calculate_and_send_to_machine(
                score, magnitude, user_text
            )
            
            # 2. Gemini Pro를 호출하여 심리 상담 메시지 생성
            consultation_message = generate_counseling_message_with_gemini(sentiment_res, user_text)
            
            print("\n--- 심리 상담 결과 ---")
            print(consultation_message)
            print("-----------------------")
            print("\n다음 참여자를 기다립니다...")
        except Exception as e:
            print(f"\n프로그램 실행 중 오류가 발생했습니다: {e}")
            print("API 호출 설정 및 인터넷 연결을 확인해주세요.")
            print("다음 참여자를 기다립니다...")