// MOTOR_1 
int ENA_1 = 1; int DIR_1 = 2; int PUL_1 = 3;
// MOTOR_2
int ENA_2 = 4; int DIR_2 = 5; int PUL_2 = 6;
// MOTOR_3 
int ENA_3 = 7; int DIR_3 = 8; int PUL_3 = 9;
// 풀리 모터
int ENA_4 = 10; int DIR_4 = 11; int PUL_4 = 12;

String incomingData = "";
bool newData = false;

// 모터 제어 함수
void moveMotor(int steps, int pulPin, int dirPin, int enaPin) {
  if (steps > 0) {
    digitalWrite(dirPin, HIGH);// (+)반시계방향 
  } else {
    digitalWrite(dirPin, LOW);// (-)시계방향 
  }
  
  digitalWrite(enaPin, HIGH); // HIGH로 활성화
  delay(50); 
  
  // 반복문은 스텝의 절댓값만큼 실행
  for (int i = 0; i < abs(steps); i++) {
    digitalWrite(pulPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(pulPin, LOW);
    delayMicroseconds(1000);
  }
  
  Serial.println("DONE");
  Serial.print("Motor operation completed.");
}

void setup() {
  Serial.begin(9600); 
  
  pinMode(PUL_1, OUTPUT); pinMode(DIR_1, OUTPUT); pinMode(ENA_1, OUTPUT);
  pinMode(PUL_2, OUTPUT); pinMode(DIR_2, OUTPUT); pinMode(ENA_2, OUTPUT);
  pinMode(PUL_3, OUTPUT); pinMode(DIR_3, OUTPUT); pinMode(ENA_3, OUTPUT);
  pinMode(PUL_4, OUTPUT); pinMode(DIR_4, OUTPUT); pinMode(ENA_4, OUTPUT);
  digitalWrite(ENA_1, LOW); digitalWrite(DIR_1, HIGH);
  digitalWrite(ENA_2, LOW); digitalWrite(DIR_2, HIGH);
  digitalWrite(ENA_3, LOW); digitalWrite(DIR_3, HIGH);
  digitalWrite(ENA_4, LOW); digitalWrite(DIR_4, HIGH);
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
    String numberStr = incomingData.substring(incomingData.indexOf(":") + 1, incomingData.indexOf(","));
    String stepsStr = incomingData.substring(incomingData.indexOf("STEPS:") + 6);
    int motorNumber = numberStr.toInt();
    int motorSteps = stepsStr.toInt();
    
    if (motorNumber == 1) {
      moveMotor(motorSteps, PUL_1, DIR_1, ENA_1);
    } else if (motorNumber == 2) {
      moveMotor(motorSteps, PUL_2, DIR_2, ENA_2);
    } else if (motorNumber == 3) {
      moveMotor(motorSteps, PUL_3, DIR_3, ENA_3);
    } else if (motorNumber == 4) {
      moveMotor(motorSteps, PUL_4, DIR_4, ENA_4);
    }
    
    incomingData = "";
    newData = false;
  }
}