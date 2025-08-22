# 파일명: sequence_controller.py

import arduino_controller

# 풀리 모터와 카트 이동에 필요한 물리적 파라미터 정의
PULLY_MOTOR_NUMBER = 4

# 카트의 첫 이동 스텝 수
STEPS_TO_POSITION_1 = 17131  # 370mm에 해당하는 스텝 수로 변경

# 염료 투하 지점 사이의 일정 거리
STEPS_BETWEEN_STATIONS = 11580 # 250mm에 해당하는 스텝 수로 유지

# 3번 지점에서 최종 출구까지의 스텝 수
STEPS_TO_FINAL_EXIT = 19859 # 428.50mm에 해당하는 스텝 수로 변경

def run_full_sequence(m1_steps, m2_steps, m3_steps):
    """
    카트 이동과 염료 투하를 순차적으로 제어하는 함수 (전진 부분만)
    """
    print("\n[기계 동작] 순차적인 염료 투하 프로세스 시작...")

    # 1. 카트를 1번 지점으로 이동 (입구로부터)
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_TO_POSITION_1)
    
    # 2. 1번 염료 모터 동작
    arduino_controller.send_motor_command(1, m1_steps)

    # 3. 카트를 2번 지점으로 이동 (1번 지점으로부터)
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_BETWEEN_STATIONS)

    # 4. 2번 염료 모터 동작
    arduino_controller.send_motor_command(2, m2_steps)

    # 5. 카트를 3번 지점으로 이동 (2번 지점으로부터)
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_BETWEEN_STATIONS)
    
    # 6. 3번 염료 모터 동작
    arduino_controller.send_motor_command(3, m3_steps)
    
    # 7. 카트를 최종 출구 지점으로 이동 (3번 지점으로부터)
    print("[기계 동작] 최종 출구 위치로 카트 이동 시작...")
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, STEPS_TO_FINAL_EXIT)
    
    print("\n[기계 동작] 염료 투하 및 전진 시퀀스 완료.")

def return_to_start():
    """
    카트를 시작 지점으로 복귀시키는 함수
    """
    TOTAL_FORWARD_STEPS = STEPS_TO_POSITION_1 + (STEPS_BETWEEN_STATIONS * 2) + STEPS_TO_FINAL_EXIT
    print("\n[기계 동작] 시작 지점으로 카트 복귀 시작...")
    arduino_controller.send_motor_command(PULLY_MOTOR_NUMBER, -TOTAL_FORWARD_STEPS)
    print("\n[기계 동작] 카트 복귀 완료.")