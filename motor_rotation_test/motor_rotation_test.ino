// 아두이노 IDE에 업로드할 코드 (단일 모터용)

int PUL = 7; 
int DIR = 6; 
int ENA = 5;

// 파이썬으로부터 받을 변수
String incomingData = "";
bool newData = false;

// 모터 제어 함수
void moveMotor(int steps) {
  // 모터는 항상 정방향으로만 회전합니다.
  digitalWrite(DIR, HIGH); // 방향 고정
  
  digitalWrite(ENA, HIGH); // 모터 활성화
  
  // 펄스를 보내 모터를 회전시킵니다.
  for (int i = 0; i < steps; i++) {
    digitalWrite(PUL, HIGH);
    delayMicroseconds(500); // 속도 고정 (500us 딜레이)
    digitalWrite(PUL, LOW);
    delayMicroseconds(500);
  }
  
  digitalWrite(ENA, LOW); // 모터 비활성화
}

void setup() {
  Serial.begin(9600); // 파이썬과 동일한 보드레이트 설정
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA, OUTPUT);
  digitalWrite(ENA, LOW); // 모터 비활성화 상태로 시작
  digitalWrite(DIR, HIGH); // 모터 방향을 정방향으로 고정
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    incomingData += inChar;
    if (inChar == '\n') {
      newData = true;
    }
  }

  if (newData) {
    // 예상 형식: "COLOR:R,STEPS:1600"
    
    // 파싱 로직
    String stepsStr = incomingData.substring(incomingData.indexOf("STEPS:") + 6);
    int motorSteps = stepsStr.toInt();
    
    Serial.print("Received -> STEPS:"); Serial.println(motorSteps);
    
    // 모터 구동
    moveMotor(motorSteps);
    
    incomingData = "";
    newData = false;
  }
}