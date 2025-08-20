# 파일명: arduino_controller.py

import serial
import serial.tools.list_ports
import time

def send_motor_command(motor_number, steps):
    """
    지정된 모터 번호와 스텝 수로 명령을 보내고, 아두이노의 'DONE' 신호를 기다립니다.
    """
    print(f"[기계 제어] 모터 {motor_number}에 {steps} 스텝 명령 준비.")
    
    try:
        arduino_port = 'COM6'
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
    send_motor_command(1, 3200)