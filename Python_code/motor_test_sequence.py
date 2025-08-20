# 파일명: motor_test_sequence.py

import arduino_controller
import time

def run_motor_test_sequence():
    """
    모터 4개가 순서대로 잘 동작하는지 테스트하는 함수
    """
    print("\n--- 모터 테스트 시퀀스 시작 ---")
    
    test_steps = 3200 # 테스트용 스텝 수

    # 1. 1번 염료 모터 테스트
    print("\n[테스트] 1번 염료 모터 구동...")
    arduino_controller.send_motor_command(1, test_steps)
    
    # 2. 2번 염료 모터 테스트
    print("\n[테스트] 2번 염료 모터 구동...")
    arduino_controller.send_motor_command(2, test_steps)
    
    # 3. 3번 염료 모터 테스트
    print("\n[테스트] 3번 염료 모터 구동...")
    arduino_controller.send_motor_command(3, test_steps)

    # 4. 풀리 모터 테스트 (카트 이동)
    print("\n[테스트] 4번 풀리 모터 구동...")
    arduino_controller.send_motor_command(4, test_steps)

    print("\n--- 모든 모터 테스트 완료 ---")

if __name__ == "__main__":
    run_motor_test_sequence()