# modified_2025_ArtTech.py 파일 내용
import os
from google.cloud import language_v1 # Natural Language API 사용을 위한 라이브러리
import vertexai # Gemini Pro (Vertex AI) 사용을 위한 라이브러리
from vertexai.preview.generative_models import GenerativeModel, Part

# machine_controller.py 파일을 임포트합니다.
import machine_controller 

# 1. 서비스 계정 키 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ghksc/Desktop/2025_Art_Tech/smart-mark-464523-g6-6f8d28d38fc0.json"

# --- Google Natural Language API를 사용한 감정 분석 함수 ---
def analyze_sentiment_only(text_content):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT, language="ko")
    sentiment_response = client.analyze_sentiment(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    return sentiment_response

# --- Gemini를 활용한 심리 상담 메시지 생성 함수 ---
def generate_counseling_message_with_gemini(sentiment_data, user_input_text):
    project_id = "smart-mark-464523-g6" 
    location = "us-central1" 

    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        return f"Gemini 모델 초기화 또는 Vertex AI 설정 오류: {e}\nGoogle Cloud 프로젝트 ID와 지역, API 활성화 및 권한을 확인해주세요."

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

    sentences_info = []
    for s_info in sentiment_data.sentences[:3]:
        s_score = s_info.sentiment.score if s_info.sentiment and s_info.sentiment.score is not None else 0.0
        s_magnitude = s_info.sentiment.magnitude if s_info.sentiment and s_info.sentiment.magnitude is not None else 0.0
        sentences_info.append(f"'{s_info.text.content}' (감정 점수: {s_score:.1f}, 강도: {s_magnitude:.1f})")
    
    if sentences_info:
        sentiment_summary += "\n\n문장별 감정:\n" + "\n".join(sentences_info)

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

    try:
        response = model.generate_content([Part.from_text(prompt)])
        return response.text
    except Exception as e:
        return f"Gemini API 호출 중 오류가 발생했습니다: {e}\n프롬프트 내용이나 API 사용량 제한 등을 확인해주세요."

# --- 메인 실행 부분 ---
if __name__ == "__main__":
    print("안녕하세요! 전시회 감정 분석 프로그램입니다.")
    print("오늘 당신의 감정을 3문장 이내로 자유롭게 입력해주세요.")
    print("종료하려면 '종료', 'exit', 'quit' 중 하나를 입력해주세요.")
    
    # --- 주사기 단면적(mm²) 정의 (새로 추가) ---
    syringe_area_mm2 = 2000.0  # <-- 여기에 계산한 단면적 2000.0mm²를 입력했습니다.
    
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
            sentiment_res = analyze_sentiment_only(user_text) 
            
            score = sentiment_res.document_sentiment.score
            magnitude = sentiment_res.document_sentiment.magnitude
            
            # 기계 제어 함수 호출 시 syringe_area_mm2 값을 추가로 전달
            calculated_color, calculated_steps, _ = machine_controller.calculate_and_send_to_machine(
                score, magnitude, syringe_area_mm2, user_text
            )
            
            consultation_message = generate_counseling_message_with_gemini(sentiment_res, user_text)
            
            print("\n--- 심리 상담 결과 ---")
            print(consultation_message)
            print("-----------------------")
            
            print(f"\n**[기념품 제작] 당신의 감정을 담아 {calculated_color} 색상으로 {calculated_steps} 스텝만큼 염료를 주입합니다.**")
            print("\n다음 참여자를 기다립니다...")
        except Exception as e:
            print(f"\n프로그램 실행 중 오류가 발생했습니다: {e}")
            print("API 호출 설정 및 인터넷 연결을 확인해주세요.")
            print("다음 참여자를 기다립니다...")