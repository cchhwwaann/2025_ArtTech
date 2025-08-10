// MOTOR_1
int PUL_1 = 7; 
int DIR_1 = 6; 
int ENA_1 = 5;

// MOTOR_2
int PUL_2 = 10; 
int DIR_2 = 9; 
int ENA_2 = 8;

// MOTOR_3
int PUL_3 = 4; 
int DIR_3 = 3; 
int ENA_3 = 2;

String incomingData = "";
bool newData = false;

// 모터 제어 함수
void moveMotor(int steps, int pulPin, int dirPin, int enaPin) {
  digitalWrite(dirPin, HIGH); // 방향 고정
  digitalWrite(enaPin, HIGH); // 모터 활성화

  delay(50); 
  
  for (int i = 0; i < steps; i++) {
    digitalWrite(pulPin, HIGH);
    delayMicroseconds(500); // 속도 조절
    digitalWrite(pulPin, LOW);
    delayMicroseconds(500);
  }
  
}

void setup() {
  Serial.begin(9600); 
  
  // 3개 모터의 핀들을 모두 OUTPUT으로 설정
  pinMode(PUL_1, OUTPUT); pinMode(DIR_1, OUTPUT); pinMode(ENA_1, OUTPUT);
  pinMode(PUL_2, OUTPUT); pinMode(DIR_2, OUTPUT); pinMode(ENA_2, OUTPUT);
  pinMode(PUL_3, OUTPUT); pinMode(DIR_3, OUTPUT); pinMode(ENA_3, OUTPUT);

  // 모든 모터의 초기 상태 설정
  digitalWrite(ENA_1, LOW); digitalWrite(DIR_1, HIGH);
  digitalWrite(ENA_2, LOW); digitalWrite(DIR_2, HIGH);
  digitalWrite(ENA_3, LOW); digitalWrite(DIR_3, HIGH);

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
    // ex> "NUMBER:1,STEPS:1600"
    
    // 파싱
    String numberStr = incomingData.substring(incomingData.indexOf(":") + 1, incomingData.indexOf(","));
    String stepsStr = incomingData.substring(incomingData.indexOf("STEPS:") + 6);
    int motorSteps = stepsStr.toInt();
    
    Serial.print("Received command for: ");
    Serial.print(numberStr);
    Serial.print(" with steps: ");
    Serial.println(motorSteps);
    
    // 넘버 코드를 확인하여 해당하는 모터 구동
    if (numberStr.equals("1")) {
      moveMotor(motorSteps, PUL_1, DIR_1, ENA_1);
    } else if (numberStr.equals("2")) {
      moveMotor(motorSteps, PUL_2, DIR_2, ENA_2);
    } else if (numberStr.equals("3")) {
      moveMotor(motorSteps, PUL_3, DIR_3, ENA_3);
    }
    
    incomingData = "";
    newData = false;
  }
}