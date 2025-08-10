# 파일명: 2025_ArtTech_1.py

import os
import warnings
import sys
import json 
from google.cloud import language_v1
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

# 모듈
import sequence_controller
import step_calculator_1

warnings.filterwarnings('ignore', category=UserWarning) # api 기한 안내 메세지 생략

# 1. 서비스 계정 키 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ghksc/Desktop/2025_ArtTech/smart-mark-464523-g6-6f8d28d38fc0.json"

# --- Gemini 감정 비율 추출 함수 ---
def analyze_emotions_with_gemini(user_input_text):
    project_id = "smart-mark-464523-g6" 
    location = "us-central1"

    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.5-flash") 
    except Exception as e:
        print(f"Gemini 모델 초기화 또는 Vertex AI 설정 오류: {e}")
        return None

    prompt = f"""당신은 사용자의 감정을 분석하는 감정 전문가입니다. 
    사용자의 입력 텍스트에 포함된 감정을 'joy', 'sadness', 'anger', 'fear', 'surprise', 
    그리고 'calm'의 6가지 카테고리로 분류하고, 각 감정의 비율을 0.0에서 1.0 사이의 소수점으로 반환해주세요. 
    반환 값은 JSON 형식으로, 6가지 감정 모두 포함해야 합니다. 감정의 총합은 1.0이 되어야 합니다.
    다른 설명이나 추가적인 텍스트는 일절 포함하지 말고, 오직 JSON 데이터만 반환하세요.

    ---
    사용자 입력: "{user_input_text}"
    ---
    
    JSON 형식으로만 응답:
    """

    try:
        response = model.generate_content([Part.from_text(prompt)])
        
        json_text = response.text.strip()
        if json_text.startswith('```json'):
            json_text = json_text.strip('` \njson')
        
        return json.loads(json_text) 
    except Exception as e:
        print(f"Gemini 감정 분석 API 호출 중 오류가 발생했습니다: {e}")
        print(f"반환된 텍스트 내용: '{response.text}'")
        return None

# --- Gemini 심리 상담 메시지 생성 함수 ---
def generate_counseling_message_with_gemini(emotion_data, user_input_text):
    project_id = "smart-mark-464523-g6" 
    location = "us-central1"

    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.5-flash") 
    except Exception as e:
        return f"Gemini 모델 초기화 또는 Vertex AI 설정 오류: {e}\nGoogle Cloud 프로젝트 ID와 지역, API 활성화 및 권한을 확인해주세요."

    emotion_summary = ""
    if emotion_data:
        sorted_emotions = sorted(emotion_data.items(), key=lambda item: item[1], reverse=True)
        top_3_emotions = [f"{emotion}: {ratio*100:.0f}%" for emotion, ratio in sorted_emotions[:3]]
        emotion_summary = ", ".join(top_3_emotions)
    else:
        emotion_summary = "감정 분석 결과를 얻을 수 없습니다."

    prompt = f"""당신은 사용자의 감정을 섬세하게 이해하고 공감하는 따뜻하고 지지적인 심리 상담가입니다.
    당신은 사용자에게 전문적인 진단이나 의료적 조언, 약물 권유를 절대 하지 않습니다.
    오직 사용자의 감정을 반영하고, 자기 성찰을 돕고, 긍정적인 방향으로 나아갈 수 있도록 격려하는 메시지를 제공합니다.
    사용자의 입력과 감정 분석 결과를 바탕으로 3~5문장으로 친절하고 부드러운 상담 메시지를 생성해주세요. 또한, 사용자가 지금 느끼고 있는 감정이 어떻게 
    발현되었고, 어떻게 변해갈지에 대해서도 설명해주면 좋겠습니다. 전반적으로 사용자가 입력한 감정을 단순히 되풀이하고 해석하는게 아닌, 정말로 사용자 스스로도 몰랐을지 모르는
    사용자의 내면에 관한 고찰이 추가되면 좋겠습니다.

    ---
    사용자 원본 입력: "{user_input_text}"
    감정 분석 결과 요약: "{emotion_summary}"
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
    print("오늘 당신의 감정을 3문장 이내로 자유롭게 입력해주세요.")
    
    while True:
        user_text = input("\n>>> ")

        if user_text.lower() in ['종료']:
            print("프로그램을 종료합니다. 참여해주셔서 감사합니다!")
            break

        if not user_text.strip():
            print("텍스트가 입력되지 않았습니다. 다시 입력해주세요.")
            continue

        print("\n당신의 감정을 분석 중입니다... 잠시만 기다려주세요.")
        try:
            # 1. 감정 비율 추출
            emotion_data = analyze_emotions_with_gemini(user_text)
            if not emotion_data:
                print("감정 분석에 실패했습니다. 다음 참여자를 기다립니다...")
                continue
            
            # 2. 감정 비율로 각 염료 모터의 스텝 수 계산
            m1_steps, m2_steps, m3_steps = step_calculator_1.calculate_steps_from_emotions(emotion_data)
            
            # -------------------------------------------------------------
            print("\n--- 감정 분석 결과 ---")
            for emotion, ratio in sorted(emotion_data.items(), key=lambda item: item[1], reverse=True):
                print(f"- {emotion.capitalize()}: {ratio*100:.1f}%")
            print("-----------------------")
            
            print(f"\n[염료 제어] 결정된 각 색상 스텝 (M1, M2, M3): {m1_steps}, {m2_steps}, {m3_steps}")
            # -------------------------------------------------------------
            
            # 3. 순차적인 모터 제어 함수를 호출
            sequence_controller.run_full_sequence(m1_steps, m2_steps, m3_steps)
            
            # 4. 모터가 작동하는 동안 상담 메시지 생성
            consultation_message = generate_counseling_message_with_gemini(emotion_data, user_text)
            
            # 5. 메시지 출력
            print("\n--- 심리 상담 결과 ---")
            print(consultation_message)
            print("-----------------------")
            
            print("\n다음 참여자를 기다립니다...")

        except Exception as e:
            print(f"\n프로그램 실행 중 오류가 발생했습니다: {e}")
            print("API 호출 설정 및 인터넷 연결을 확인해주세요.")
            print("다음 참여자를 기다립니다...")