# 파일명: step_calculator_1.py

# --- 캐릭터별 레진 용량 정의 ---
character_volumes = {
    '1': 35.0,
    '2': 40.0,
    '3': 45.0,
    '4': 50.0,
    '5': 55.0
}

# --- 염료 모터 스텝 파라미터 정의 ---
#  10ml당 240 스텝이므로, 1ml당 24 스텝-----> 실험적으로 수정필요
STEPS_PER_ML = 24.0

def get_volume(character_name):
    """
    캐릭터 이름에 해당하는 레진 용량을 반환합니다.
    """
    return character_volumes.get(character_name, None)


def calculate_steps_from_emotions(emotion_data, total_volume_ml):
    """
    감정 분석 결과를 바탕으로 3가지 색상 모터의 스텝 수를 계산하여 반환합니다.
    """
    if not emotion_data or not isinstance(emotion_data, dict):
        print("오류: 유효한 감정 분석 데이터가 제공되지 않았습니다.")
        return 0, 0, 0

    # --- 1. 감정 비율을 색상 비율로 매핑 ---
    # M1 (따뜻한 색): 'joy', 'anger' // M2 (중성색): 'surprise', 'calm' // M3 (차가운 색): 'sadness', 'fear'
    
    m1_ratio = emotion_data.get('joy', 0) + emotion_data.get('anger', 0)
    m2_ratio = emotion_data.get('surprise', 0) + emotion_data.get('calm', 0)
    m3_ratio = emotion_data.get('sadness', 0) + emotion_data.get('fear', 0)
    
    total_ratio_sum = m1_ratio + m2_ratio + m3_ratio
    
    # 비율의 합이 1.0이 되도록 정규화
    if total_ratio_sum > 0:
        final_M1_ratio = m1_ratio / total_ratio_sum
        final_M2_ratio = m2_ratio / total_ratio_sum
        final_M3_ratio = m3_ratio / total_ratio_sum
    else:
        # 감정이 감지되지 않으면 기본값으로 설정
        final_M1_ratio, final_M2_ratio, final_M3_ratio = 1/3, 1/3, 1/3

    # --- 2. 각 색상의 용량과 스텝 수 계산 ---
    M1_volume_ml = total_volume_ml * final_M1_ratio
    M2_volume_ml = total_volume_ml * final_M2_ratio
    M3_volume_ml = total_volume_ml * final_M3_ratio
    
    # 새로운 STEPS_PER_ML 파라미터를 사용하여 스텝 계산
    M1_steps = int(M1_volume_ml * STEPS_PER_ML)
    M2_steps = int(M2_volume_ml * STEPS_PER_ML)
    M3_steps = int(M3_volume_ml * STEPS_PER_ML)

    return M1_steps, M2_steps, M3_steps