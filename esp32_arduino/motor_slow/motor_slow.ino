// Test all sensors connected to the
// arduino 
// 
// Marianela Crissman

#define leftFactor 10
#define rightFactor 10
#define speedSet  80
*
#include <UCMotor.h>

//pin definition
int controlPin = 2;

//variables on the program
int startM =0;
int prevState =-1;


UC_DCMotor leftMotor(3, MOTOR34_64KHZ);
UC_DCMotor rightMotor(4, MOTOR34_64KHZ);


void setup() 
{
  pinMode(controlPin, INPUT);
  delay(20);
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Inicializacion exitosa!");
  Serial.println("================================");

}

void loop() {
  // put your main code here, to run repeatedly:

      if( digitalRead(controlPin)==LOW){
          if(prevState != 0)
            {
              Serial.print("ahora esta en LOW");
              prevState = 0;
              moveForward();
              delay(500);
              moveNot();
            }
      }
      else{
          if(prevState != 1)
            {
              Serial.print("ahora esta en HIGH");
              prevState = 1;
              moveForward();
              delay(500);
              moveNot();
            }
        delay(10);
      }
//      Serial.println("Move wheels...");
//      delay(2000);
//      moveForward(); delay(1000);
//      moveBackward(); delay(1000);
//      turnLeft(); delay(1000);
//      turnRight(); delay(1000);
//      moveNot();

//      Serial.println("Move servo...");
//      delay(5000);
      
    


}

void moveForward() {
  Serial.print(" forward -> ");
  leftMotor.run(FORWARD);
  rightMotor.run(FORWARD);
  leftMotor.setSpeed(speedSet + leftFactor);
  rightMotor.setSpeed(speedSet + rightFactor);
}
void turnLeft() {
  Serial.print(" left -> ");
  leftMotor.run(BACKWARD);
  rightMotor.run(FORWARD);
  leftMotor.setSpeed(speedSet + leftFactor);
  rightMotor.setSpeed(speedSet + rightFactor);
  delay(400);
//  moveStop();
}
void turnRight() {
  Serial.print(" right -> ");
  leftMotor.run(FORWARD);
  rightMotor.run(BACKWARD);
  leftMotor.setSpeed(speedSet + leftFactor);
  rightMotor.setSpeed(speedSet + rightFactor);
  delay(400);
//  moveStop();
}
void moveBackward() {
  Serial.print(" backward -> ");
  leftMotor.run(BACKWARD);
  rightMotor.run(BACKWARD);
  leftMotor.setSpeed(speedSet + leftFactor);
  rightMotor.setSpeed(speedSet + rightFactor);
}
void moveStop() {
  Serial.print(" (release) ");
  leftMotor.run(RELEASE);
  rightMotor.run(RELEASE);
}

void moveNot()
{
  Serial.println(" stop.");
  leftMotor.run(STOP);
  rightMotor.run(STOP);
//  leftMotor.setSpeed(speedSet + leftFactor);
//  rightMotor.setSpeed(speedSet + rightFactor);
}
