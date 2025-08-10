# 명령 전송 (시리얼통신)
import time
import serial
import serial.tools.list_ports

# 파일명: machine_controller_1.py
# ...
def send_motor_command(motor_number, steps):
    try:
        # 포트 번호를 확인해주세요 (예: COM5)
        with serial.Serial('COM5', 9600, timeout=1) as ser: 
            command = f"NUMBER:{motor_number},STEPS:{steps}\n"
            ser.write(command.encode('utf-8'))
            print(f"[기계 제어] 모터 {motor_number}에 {steps} 스텝 명령 전송 완료.")

    except serial.SerialException as e:
        print(f"[기계 제어] 시리얼 통신 오류 발생: {e}")
    except Exception as e:
        print(f"[기계 제어] 모터 제어 중 알 수 없는 오류 발생: {e}")
# ...
# 밑에는 프로그램이 동작하는지 확인용으로 이파일만 단독 실행하면 1번모터만 1000스텝 회전
if __name__ == "__main__":
    print("--- Machine Controller 단독 테스트 ---")
    send_motor_command(1, 1000)