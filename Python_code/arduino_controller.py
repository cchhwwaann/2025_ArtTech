# 명령 전송 (시리얼통신)
import time
import serial
import serial.tools.list_ports

def send_motor_command(motor_number, steps):
    try:
        # 포트 번호 (예: COM5)
        with serial.Serial('COM5', 9600, timeout=1) as ser: 
            command = f"NUMBER:{motor_number},STEPS:{steps}\n"
            ser.write(command.encode('utf-8'))
            print(f"[기계 제어] 모터 {motor_number}에 {steps} 스텝 명령 전송 완료.")

    except serial.SerialException as e:
        print(f"[기계 제어] 시리얼 통신 오류 발생: {e}")
    except Exception as e:
        print(f"[기계 제어] 모터 제어 중 알 수 없는 오류 발생: {e}")
