# machine_controller.py 파일 내용
import time
import serial
import serial.tools.list_ports # 이 라이브러리는 더 이상 필요 없지만 import 문은 그대로 둡니다.

def calculate_and_send_to_machine(score, magnitude, user_input_text):
    """
    감정 분석 결과를 바탕으로 단일 모터의 파라미터를 계산하고 제어합니다.
    """
    print("\n[기계 제어] --- 기념품 제작 파라미터 계산 중 ---")

    # --- 1. 감정 기반 색상 결정 ---
    color_code = ''  
    color_name = ''  

    if score > 0.3:
        color_code = 'R'
        color_name = '빨강'
    elif score < -0.3:
        color_code = 'B'
        color_name = '파랑'
    else:
        color_code = 'G'
        color_name = '초록'

    # --- 2. 감정 강도를 스텝 수로 변환 ---
    min_steps = 100
    max_steps = 2000
    total_steps = int(min_steps + (magnitude * (max_steps - min_steps)))

    # --- 3. 모터 제어 파라미터 출력 및 전송 ---
    print(f"[기계 제어] 결정된 색상: {color_name}")
    print(f"[기계 제어] 결정된 총 스텝 수: {total_steps} steps")

    try:
        # ---------------------------------------------
        # 수동으로 포트 지정 (자동 감지 로직 제거)
        # ---------------------------------------------
        # Windows 장치 관리자에서 아두이노의 COM 포트 번호를 확인하고 입력하세요.
        arduino_port = 'COM5'  # <-- 여기에 확인한 COM 포트를 입력하세요 (예: 'COM5')
        
        if arduino_port:
            ser = serial.Serial(arduino_port, 9600, timeout=1) 
            time.sleep(2) 
            print(f"[기계 제어] 아두이노에 연결되었습니다: {arduino_port}")

            data_to_send = f"COLOR:{color_code},STEPS:{total_steps}\n"
            ser.write(data_to_send.encode('utf-8'))
            print(f"[기계 제어] 데이터 전송 완료: {data_to_send.strip()}")
            
            ser.close()
        else:
            print("[기계 제어] 오류: 포트 번호가 지정되지 않았습니다.")

    except serial.SerialException as e:
        print(f"[기계 제어] 시리얼 통신 오류 발생: {e}")
    
    return color_name, total_steps, "고정된 속도"