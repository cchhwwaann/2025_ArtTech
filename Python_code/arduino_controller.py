# 파일명: arduino_controller.py

import serial
import serial.tools.list_ports
import time

# step_file_manager 모듈 임포트
import step_file_manager

def send_motor_command(motor_number, steps):
    """
    지정된 모터 번호와 스텝 수로 명령을 보내고, 아두이노의 'DONE' 신호를 기다립니다.
    """
    # print(f"[기계 제어] 모터 {motor_number}에 {steps} 스텝 명령 준비.")
    
    try:
        arduino_port = 'COM6' # 아두이노 포트 번호 맞게
        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            time.sleep(2) # 아두이노와의 연결 안정화

            command = f"NUMBER:{motor_number},STEPS:{steps}\n"
            ser.write(command.encode('utf-8'))
            print(f"{motor_number} for {steps}")
            
            # 아두이노의 응답(DONE)을 기다리는 루프
            while True:
                response = ser.readline().decode('utf-8').strip()
                if "DONE" in response:
                    print(f"DONE")
                    break # 신호 수신 시 루프 종료
    
    except serial.SerialException as e:
        print(f"[기계 제어] 시리얼 통신 오류 발생: {e}")
        return False
    except Exception as e:
        print(f"[기계 제어] 모터 제어 중 알 수 없는 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("--- Machine Controller 단독 테스트 ---")
    
    # 1. 파일에서 기존 누적 스텝 불러오기
    m1_cumulative_steps, m2_cumulative_steps, m3_cumulative_steps, m4_cumulative_steps = step_file_manager.load_cumulative_steps()
    
    # 2. 테스트용 모터 명령 및 스텝 정의
    # 각 튜플은 (모터_번호, 스텝_수)를 의미합니다.
    test_commands = [
        (2, -200), # 카트를 1번 지점으로 이동
        (1, -200),  # 1번 염료 모터 동작
        (2, 200), # 카트를 2번 지점으로 이동
        (1, 200),  # 2번 염료 모터 동작
        #(4, 100), # 카트를 3번 지점으로 이동
        #(3, 100),  # 3번 염료 모터 동작
        #(4, 100)  # 카트를 최종 출구 지점으로 이동
    ]
    
    # 3. 명령을 순차적으로 실행하고 누적 스텝 기록
    for motor_number, steps in test_commands:
        print(f"\n[테스트] 모터 {motor_number}에 {steps} 스텝 명령 전송...")
        
        # 모터 제어 명령 전송
        success = send_motor_command(motor_number, steps)
        
        if success:
            # 누적 스텝 업데이트
            if motor_number == 1:
                m1_cumulative_steps += steps
            elif motor_number == 2:
                m2_cumulative_steps += steps
            elif motor_number == 3:
                m3_cumulative_steps += steps
            elif motor_number == 4:
                m4_cumulative_steps += steps
                
            # 업데이트된 누적 스텝 파일에 저장
            step_file_manager.save_cumulative_steps([m1_cumulative_steps, m2_cumulative_steps, m3_cumulative_steps, m4_cumulative_steps])
            
        else:
            print("[테스트] 명령 실행 실패. 다음 명령을 건너뜁니다.")

    print("\n--- 단독 테스트 완료 ---")
    # 1번 모터 드라이버 2번 모터 드라이버(단선예상) 이상함