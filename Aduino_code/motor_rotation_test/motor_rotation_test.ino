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

// 풀리 모터
int PUL_4 = A3; // 예시: 풀리 모터 핀 설정
int DIR_4 = A2;
int ENA_4 = A1;

String incomingData = "";
bool newData = false;

// 모터 제어 함수
void moveMotor(int steps, int pulPin, int dirPin, int enaPin) {
  digitalWrite(dirPin, HIGH); // 방향 고정
  digitalWrite(enaPin, HIGH); // 모터 활성화
  
  // 모든 모터 핀에 대한 배열을 사용하여 동적으로 핀을 지정할 수 있습니다.
  // 이 예제에서는 핀을 직접 지정하여 사용합니다.

  delay(50); 
  
  for (int i = 0; i < steps; i++) {
    digitalWrite(pulPin, HIGH);
    delayMicroseconds(100); // 속도 조절
    digitalWrite(pulPin, LOW);
    delayMicroseconds(100);
  }
  
  // 동작 완료 후 파이썬으로 DONE 신호 전송
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
  // 시리얼 통신을 통해 명령어를 받음
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
    
    // 모터 번호를 확인하여 해당하는 모터 구동
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