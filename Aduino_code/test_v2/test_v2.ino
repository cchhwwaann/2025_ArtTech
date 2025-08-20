// 시리얼 통신으로 파이썬과 연동하여 스테핑 모터 제어
// -------------------------------------------------------------
// 파이썬의 arduino_controller.py와 호환되도록 작성되었습니다.
// -------------------------------------------------------------

// --- 핀 정의 (사용하는 모터 드라이버에 맞게 변경) ---
#define M1_PUL 7 // 모터 1 (염료)
#define M1_DIR 6
#define M1_ENA 5

#define M2_PUL 10 // 모터 2 (염료)
#define M2_DIR 9
#define M2_ENA 8

#define M3_PUL 13 // 모터 3 (염료)
#define M3_DIR 12
#define M3_ENA 11

#define M4_PUL 4 // 모터 4 (풀리)
#define M4_DIR 3
#define M4_ENA 2

// --- 변수 선언 ---
String command;
int motorNumber;
long steps;
const int microsecondDelay = 100; // 펄스 간격 (모터 속도)

void setup() {
  Serial.begin(9600);
  pinMode(M1_PUL, OUTPUT); pinMode(M1_DIR, OUTPUT); pinMode(M1_ENA, OUTPUT);
  pinMode(M2_PUL, OUTPUT); pinMode(M2_DIR, OUTPUT); pinMode(M2_ENA, OUTPUT);
  pinMode(M3_PUL, OUTPUT); pinMode(M3_DIR, OUTPUT); pinMode(M3_ENA, OUTPUT);
  pinMode(M4_PUL, OUTPUT); pinMode(M4_DIR, OUTPUT); pinMode(M4_ENA, OUTPUT);

  // 모든 모터 드라이버를 항상 활성화 (HIGH)
  digitalWrite(M1_ENA, HIGH);
  digitalWrite(M2_ENA, HIGH);
  digitalWrite(M3_ENA, HIGH);
  digitalWrite(M4_ENA, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    parseCommand(command);
    
    if (motorNumber > 0 && steps != 0) {
      controlMotor(motorNumber, steps);
    }
    
    // 다음 명령을 위해 변수 초기화
    motorNumber = 0;
    steps = 0;
  }
}

// 시리얼 명령을 파싱하는 함수
void parseCommand(String cmd) {
  int numberIndex = cmd.indexOf("NUMBER:");
  int stepsIndex = cmd.indexOf(",STEPS:");
  
  if (numberIndex != -1 && stepsIndex != -1) {
    motorNumber = cmd.substring(numberIndex + 7, stepsIndex).toInt();
    steps = cmd.substring(stepsIndex + 7).toInt();
  }
}

// 모터를 실제로 제어하는 함수
void controlMotor(int motorNum, long numSteps) {
  
  // 방향 설정
  bool direction = (numSteps > 0);
  
  // 모터 번호에 맞는 핀 선택
  int pulPin, dirPin;
  switch (motorNum) {
    case 1: pulPin = M1_PUL; dirPin = M1_DIR; break;
    case 2: pulPin = M2_PUL; dirPin = M2_DIR; break;
    case 3: pulPin = M3_PUL; dirPin = M3_DIR; break;
    case 4: pulPin = M4_PUL; dirPin = M4_DIR; break;
    default:
      return;
  }
  
  // 방향 설정
  digitalWrite(dirPin, direction ? HIGH : LOW);
  
  // 펄스를 보내 모터 회전
  for (long i = 0; i < abs(numSteps); i++) {
    digitalWrite(pulPin, HIGH);
    delayMicroseconds(microsecondDelay);
    digitalWrite(pulPin, LOW);
    delayMicroseconds(microsecondDelay);
  }
  
  // 참고: 모터 비활성화 코드를 삭제했음.
  
  // 작업 완료 신호 전송
  Serial.println("DONE");
}