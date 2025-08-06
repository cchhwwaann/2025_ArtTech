# machine_controller.py 파일 내용
import time
import serial
import serial.tools.list_ports

def calculate_and_send_to_machine(score, magnitude, user_input_text):
    """
    감정 분석 결과를 바탕으로 3가지 모터의 파라미터를 계산하고 제어합니다.
    """
    print("\n[기계 제어] --- 기념품 제작 파라미터 계산 중 ---")

    # --- 1. 물리적 파라미터 정의 ---
    SYRINGE_AREA_MM2 = 2000.0
    MM_PER_REVOLUTION = 69.08
    STEPS_PER_REVOLUTION = 1600
    MM_PER_STEP = MM_PER_REVOLUTION / STEPS_PER_REVOLUTION
    MM3_PER_ML = 1000.0
    
    TOTAL_VOLUME_ML = 100.0

    # --- 2. score와 magnitude를 이용해 RGB 비율 계산 ---
    g_ratio = 1.0 - abs(score)
    final_g_ratio = g_ratio * (1.0 - magnitude)
    
    remaining_ratio = 1.0 - final_g_ratio
    
    final_r_ratio = max(0, score) * remaining_ratio
    final_b_ratio = max(0, -score) * remaining_ratio
    
    total_ratio_sum = final_r_ratio + final_b_ratio + final_g_ratio
    if total_ratio_sum > 0:
        final_r_ratio /= total_ratio_sum
        final_b_ratio /= total_ratio_sum
        final_g_ratio /= total_ratio_sum

    # --- 3. 각 색상의 용량과 스텝 수 계산 ---
    r_volume_ml = TOTAL_VOLUME_ML * final_r_ratio
    g_volume_ml = TOTAL_VOLUME_ML * final_g_ratio
    b_volume_ml = TOTAL_VOLUME_ML * final_b_ratio
    
    r_steps = int((r_volume_ml * MM3_PER_ML) / SYRINGE_AREA_MM2 / MM_PER_STEP)
    g_steps = int((g_volume_ml * MM3_PER_ML) / SYRINGE_AREA_MM2 / MM_PER_STEP)
    b_steps = int((b_volume_ml * MM3_PER_ML) / SYRINGE_AREA_MM2 / MM_PER_STEP)

    # --- 4. 모터 제어 파라미터 출력 및 전송 ---
    print(f"[기계 제어] 총 용량: {TOTAL_VOLUME_ML:.2f} ml")
    print(f"[기계 제어] 결정된 색상 비율 (R, G, B): {final_r_ratio:.2f}, {final_g_ratio:.2f}, {final_b_ratio:.2f}")
    print(f"[기계 제어] 결정된 각 색상 스텝 (R, G, B): {r_steps}, {g_steps}, {b_steps}")
    
    try:
        arduino_port = 'COM5'
        
        if arduino_port:
            ser = serial.Serial(arduino_port, 9600, timeout=1) 
            time.sleep(2) 
            print(f"[기계 제어] 아두이노에 연결되었습니다: {arduino_port}")

            # 3개의 모터에 대한 명령을 각각 보냅니다.
            # 이 명령을 받을 수 있도록 아두이노 코드도 수정되어야 합니다.
            commands_to_send = [
                f"COLOR:R,STEPS:{r_steps}\n",
                f"COLOR:G,STEPS:{g_steps}\n",
                f"COLOR:B,STEPS:{b_steps}\n",
            ]
            
            for command in commands_to_send:
                ser.write(command.encode('utf-8'))
                print(f"[기계 제어] 명령어 전송: {command.strip()}")
                time.sleep(1) # 각 명령 사이에 약간의 시간 간격 주기

            ser.close()
        else:
            print("[기계 제어] 오류: 포트 번호가 지정되지 않았습니다.")

    except serial.SerialException as e:
        print(f"[기계 제어] 시리얼 통신 오류 발생: {e}")
    
    return "복합", "3가지 색상", "3개 모터"