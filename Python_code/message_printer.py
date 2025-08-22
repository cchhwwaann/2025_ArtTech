# 파일명: message_printer.py

import win32print
import win32api
import win32con

def print_message(message_text):
    """
    제공된 텍스트를 기본 프린터로 인쇄합니다.
    """
    try:
        # 기본 프린터 이름 가져오기
        printer_name = win32print.GetDefaultPrinter()
        
        # 프린터 설정(DEVMODE) 가져오기
        hPrinter = win32print.OpenPrinter(printer_name)
        devmode = win32print.GetPrinter(hPrinter, 2)["pDevMode"]
        
        # --- 명함 크기 용지 설정 예시 ---
        # 프린터 드라이버가 지원하는 용지 크기로 설정해야 합니다.
        # 아래는 예시이며, 실제로는 프린터 드라이버에서 설정된 명함 용지 ID를 사용해야 합니다.
        #devmode.PaperSize = win32con.DMPAPER_BUSINESS_CARD
        #devmode.PaperWidth = 550 # 55mm * 10 (twips 단위)
        #devmode.PaperLength = 900 # 90mm * 10 (twips 단위)
        
        # 인쇄 작업 시작
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("상담 메시지", None, "RAW"))
        
        if hJob > 0:
            win32print.StartPagePrinter(hPrinter)
            # 메시지를 UTF-8로 인코딩하여 인쇄
            win32print.WritePrinter(hPrinter, message_text.encode('utf-8'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            print(f"\n[인쇄 완료] '{printer_name}'로 상담 메시지를 보냈습니다.")
        else:
            print("\n[인쇄 오류] 인쇄 작업을 시작할 수 없습니다.")
            
        win32print.ClosePrinter(hPrinter)

    except ImportError:
        print("\n[인쇄 오류] 'pywin32' 모듈이 설치되지 않았습니다. 'pip install pywin32'를 실행하세요.")
    except Exception as e:
        print(f"\n[인쇄 오류] 인쇄 중 오류가 발생했습니다: {e}")