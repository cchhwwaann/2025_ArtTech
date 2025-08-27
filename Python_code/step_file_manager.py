# 파일명: step_file_manager.py

import os

def save_cumulative_steps(steps):
    """
    현재의 누적 스텝 값을 파일에 저장합니다.
    steps 리스트는 [m1, m2, m3, m4]의 순서여야 합니다.
    """
    try:
        with open("cumulative_steps.txt", "w") as f:
            f.write(f"m1:{steps[0]}\n")
            f.write(f"m2:{steps[1]}\n")
            f.write(f"m3:{steps[2]}\n")
            f.write(f"m4:{steps[3]}\n")
        print("[파일 저장] 누적 스텝이 파일에 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"[오류] 누적 스텝 저장 중 오류가 발생했습니다: {e}")

def load_cumulative_steps():
    """
    파일에서 누적 스텝을 불러옵니다. 파일이 없으면 0으로 초기화합니다.
    반환 값은 [m1, m2, m3, m4]의 순서입니다.
    """
    steps = [0, 0, 0, 0]
    try:
        with open("cumulative_steps.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("m1:"):
                    steps[0] = int(line.split(":")[1])
                elif line.startswith("m2:"):
                    steps[1] = int(line.split(":")[1])
                elif line.startswith("m3:"):
                    steps[2] = int(line.split(":")[1])
                elif line.startswith("m4:"):
                    steps[3] = int(line.split(":")[1])
        print("[파일 로드] 이전에 저장된 누적 스텝을 성공적으로 불러왔습니다.")
    except FileNotFoundError:
        print("[파일 로드] 기존 누적 스텝 파일이 없습니다. 0부터 시작합니다.")
    except Exception as e:
        print(f"[오류] 누적 스텝 로드 중 오류가 발생했습니다: {e}. 0부터 시작합니다.")
        steps = [0, 0, 0, 0]
    return steps