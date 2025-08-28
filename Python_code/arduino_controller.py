# 파일명: arduino_controller.py

import serial
import serial.tools.list_ports
import time

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
            print(f"[기계 제어] 모터 {motor_number}에 {steps} 스텝 명령 전송 완료. 'DONE' 신호 대기 중...")
            
            # 아두이노의 응답(DONE)을 기다리는 루프
            while True:
                response = ser.readline().decode('utf-8').strip()
                if "DONE" in response:
                    print(f"[기계 제어] 아두이노로부터 'DONE' 신호 수신!")
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
    print("\n[기계 동작] 순차적인 염료 투하 프로세스 시작...")

    # 1. 카트를 1번 지점으로 이동 (입구로부터)
    send_motor_command(3, 1600) #2120
    
    # 2. 1번 염료 모터 동작
    #send_motor_command(1, 200)

    # 3. 카트를 2번 지점으로 이동 (1번 지점으로부터)
    #send_motor_command(4, 200) #1090

    # 4. 2번 염료 모터 동작
    #send_motor_command(2, 200)

    # 5. 카트를 3번 지점으로 이동 (2번 지점으로부터)
    #send_motor_command(4, 200) #1090
    
    # 6. 3번 염료 모터 동작
    #send_motor_command(3, 200)
    
    # 7. 카트를 최종 출구 지점으로 이동 (3번 지점으로부터)
    #print("[기계 동작] 최종 출구 위치로 카트 이동 시작...")
    #send_motor_command(4, 200) #2300
    
    print("\n[기계 동작] 염료 투하 및 전진 시퀀스 완료.")