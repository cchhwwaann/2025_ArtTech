# test_logic_manual.py
import machine_controller
import sys
import time

def run_test():
    """
    사용자 입력을 받아 machine_controller를 실행하는 테스트 함수
    """
    print("--- 감정-모터 제어 로직 테스트 프로그램 ---")
    print("감정 점수(score)와 감정 강도(magnitude)를 직접 입력하세요.")
    print("종료하려면 'q'를 입력하세요.")
    
    while True:
        try:
            score_input = input("\n감정 점수(score, -1.0 ~ 1.0): ")
            if score_input.lower() == 'q':
                break
            
            magnitude_input = input("감정 강도(magnitude, 0.0 ~ 1.0): ")
            if magnitude_input.lower() == 'q':
                break

            score = float(score_input)
            magnitude = float(magnitude_input)
            
            # 입력 값 유효성 검사
            if not (-1.0 <= score <= 1.0):
                print("오류: score는 -1.0과 1.0 사이의 값이어야 합니다.")
                continue
            if not (0.0 <= magnitude <= 1.0): # magnitude도 0.0~1.0 범위로 가정
                print("오류: magnitude는 0.0과 1.0 사이의 값이어야 합니다.")
                continue

            print(f"\n입력된 값 -> score: {score:.2f}, magnitude: {magnitude:.2f}")

            # machine_controller.py의 함수 호출
            # user_text는 임시로 "수동 테스트" 문자열을 사용합니다.
            calculated_info, color_desc, motor_desc = machine_controller.calculate_and_send_to_machine(
                score, magnitude, "수동 테스트"
            )
            
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")

    print("프로그램을 종료합니다.")
    
if __name__ == "__main__":
    run_test()