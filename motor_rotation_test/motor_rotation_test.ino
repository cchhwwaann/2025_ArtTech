// 아두이노 IDE에 업로드할 코드 (3개 모터용)

// 빨강 모터 핀
int PUL_R = 7; 
int DIR_R = 6; 
int ENA_R = 5;

// 초록 모터 핀
int PUL_G = 10; 
int DIR_G = 9; 
int ENA_G = 8;

// 파랑 모터 핀
int PUL_B = 4; 
int DIR_B = 3; 
int ENA_B = 2;

String incomingData = "";
bool newData = false;

// 모터 제어 함수 (어떤 모터의 핀을 사용할지 인자로 받음)
void moveMotor(int steps, int pulPin, int dirPin, int enaPin) {
  digitalWrite(dirPin, HIGH); // 방향 고정
  digitalWrite(enaPin, HIGH); // 모터 활성화

  delay(500);
  
  for (int i = 0; i < steps; i++) {
    digitalWrite(pulPin, HIGH);
    delayMicroseconds(500); // 속도 고정
    digitalWrite(pulPin, LOW);
    delayMicroseconds(500);
  }
  
  digitalWrite(enaPin, LOW); // 모터 비활성화
}

void setup() {
  Serial.begin(9600); // 파이썬과 동일한 보드레이트 설정
  
  // 3개 모터의 핀들을 모두 OUTPUT으로 설정
  pinMode(PUL_R, OUTPUT); pinMode(DIR_R, OUTPUT); pinMode(ENA_R, OUTPUT);
  pinMode(PUL_G, OUTPUT); pinMode(DIR_G, OUTPUT); pinMode(ENA_G, OUTPUT);
  pinMode(PUL_B, OUTPUT); pinMode(DIR_B, OUTPUT); pinMode(ENA_B, OUTPUT);

  // 모든 모터의 초기 상태 설정
  digitalWrite(ENA_R, LOW); digitalWrite(DIR_R, HIGH);
  digitalWrite(ENA_G, LOW); digitalWrite(DIR_G, HIGH);
  digitalWrite(ENA_B, LOW); digitalWrite(DIR_B, HIGH);

  Serial.println("Arduino is ready to control 3 motors.");
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
    String colorStr = incomingData.substring(incomingData.indexOf(":") + 1, incomingData.indexOf(","));
    String stepsStr = incomingData.substring(incomingData.indexOf("STEPS:") + 6);
    int motorSteps = stepsStr.toInt();
    
    Serial.print("Received command for: ");
    Serial.print(colorStr);
    Serial.print(" with steps: ");
    Serial.println(motorSteps);
    
    // 색상 코드를 확인하여 해당하는 모터 구동
    if (colorStr.equals("R")) {
      moveMotor(motorSteps, PUL_R, DIR_R, ENA_R);
    } else if (colorStr.equals("G")) {
      moveMotor(motorSteps, PUL_G, DIR_G, ENA_G);
    } else if (colorStr.equals("B")) {
      moveMotor(motorSteps, PUL_B, DIR_B, ENA_B);
    }
    
    incomingData = "";
    newData = false;
  }
}