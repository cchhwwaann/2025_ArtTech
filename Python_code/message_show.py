# 파일명: message_show.py

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt

# --- 터치(클릭) 시 창이 닫히는 사용자 정의 클래스 ---
class TouchToCloseWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    # 마우스 클릭(터치) 이벤트 발생 시 호출되는 메서드
    def mousePressEvent(self, event):
        self.close()

# --- 일반 텍스트 메시지를 화면에 띄우는 함수 ---
def show_text_message(message_text):
    """
    상담 메시지를 별도의 GUI 창에 띄웁니다.
    두 번째 화면의 해상도에 맞춰 창과 폰트 크기를 자동으로 조절하고,
    메시지가 중앙에 위치하도록 공백을 추가합니다.
    화면 터치 시 창이 닫힙니다.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    screens = app.screens()
    if len(screens) < 2:
        print("\n[알림] 두 번째 화면을 찾을 수 없습니다. 기본 화면에 텍스트 메시지를 표시합니다.")
        target_screen = screens[0]
    else:
        target_screen = screens[1]

    screen_geometry = target_screen.geometry()
    window_width = screen_geometry.width()   # 창 너비를 화면 너비로 설정
    window_height = screen_geometry.height() # 창 높이를 화면 높이로 설정
    
    window = TouchToCloseWindow()
    window.setWindowTitle("상담 메시지")
    window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    window.resize(window_width, window_height)

    text_label = QLabel(message_text, window)
    
    # --- 수정된 부분: 폰트 크기를 텍스트 길이에 맞춰 동적으로 조절 ---
    font_size = int(window_width * 0.04)  # 초기 폰트 크기 설정
    font = QFont("Noto Sans KR", font_size)
    metrics = QFontMetrics(font)
    
    # 여백을 고려한 텍스트 영역의 최대 크기
    max_text_width = window_width - 200  # 좌우 여백 100px씩
    max_text_height = window_height - 200 # 상하 여백 100px씩
    
    # 텍스트가 영역에 맞을 때까지 폰트 크기 줄이기
    while True:
        # 줄바꿈을 고려한 텍스트의 실제 크기 계산
        text_rect = metrics.boundingRect(0, 0, max_text_width, max_text_height, Qt.TextWordWrap, message_text)
        
        if text_rect.height() < max_text_height and text_rect.width() < max_text_width:
            break  # 텍스트가 영역 안에 잘 들어맞으면 루프 종료
        
        font_size -= 1 # 폰트 크기 1씩 줄이기
        if font_size <= 5: # 최소 폰트 크기 설정
            break
            
        font.setPointSize(font_size)
        metrics = QFontMetrics(font)
        
    text_label.setFont(font)
    text_label.setStyleSheet("color: white; background-color: black; padding: 100px;")
    text_label.setWordWrap(True)
    text_label.setAlignment(Qt.AlignCenter)
    
    # 레이블 크기를 창 크기에 맞춰 설정
    text_label.setGeometry(0, 0, window.width(), window.height())
    
    center_x = screen_geometry.x() + (screen_geometry.width() - window.width()) // 2
    center_y = screen_geometry.y() + (screen_geometry.height() - window.height()) // 2
    window.move(center_x, center_y)

    window.show()
    
    app.exec_()


# --- 테스트를 위한 메인 실행 블록 ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_message, ok = QInputDialog.getMultiLineText(None, "메시지 입력", "띄울 메시지를 입력하세요:")
    
    if not ok or not user_message:
        QMessageBox.warning(None, "입력 오류", "유효한 메시지가 입력되지 않았습니다. 프로그램을 종료합니다.")
        sys.exit()

    show_text_message(user_message)