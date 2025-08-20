# 파일명: sequence_controller.py

import arduino_controller

# 풀리 모터와 카트 이동에 필요한 물리적 파라미터 정의
PULLY_MOTOR_NUMBER = 4
STEPS_TO_POSITION_1 = 500  # 1번 지점까지 이동하는 스텝 수
STEPS_TO_POSITION_2 = 500  # 2번 지점까지 이동하는 스텝 수
STEPS_TO_POSITION_3 = 500  # 3번 지점까지 이동하는 스텝 수
# 새로운 변수 추가: 카트가 최종적으로 이동해야 하는 스텝 수
STEPS_TO_FINAL_POSITION = 500 

def run_full_sequence(m1_steps, m2_steps, m3_steps):
    """
    카트 이동과 염료 투하를 순차적으로 제어하는 함수
    """
    print("\n[기계 동작] 순차적인 염료 투하 프로세스 시작...")

    # 1. 카트를 1번 지점으로 이동
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_TO_POSITION_1)
    
    # 2. 1번 염료 모터 동작
    arduino_controller.send_motor_command(1, m1_steps)

    # 3. 카트를 2번 지점으로 이동
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_TO_POSITION_2)

    # 4. 2번 염료 모터 동작
    arduino_controller.send_motor_command(2, m2_steps)

    # 5. 카트를 3번 지점으로 이동
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_TO_POSITION_3)
    
    # 6. 3번 염료 모터 동작
    arduino_controller.send_motor_command(3, m3_steps)
    
    # 7. 마지막 풀리 모터 동작
    print("[기계 동작] 마지막 위치로 카트 이동 시작...")
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_TO_FINAL_POSITION)
    
    print("\n[기계 동작] 모든 모터 구동 명령이 전송되었습니다.")