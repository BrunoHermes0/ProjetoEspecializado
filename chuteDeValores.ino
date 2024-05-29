#include <Arduino.h>
#include <stdio.h>

const int motorPin1A = 33;
const int motorPin1B = 25;
const int motorPin2A = 27;
const int motorPin2B = 26;
const int motorSpeedPin1  = 32;  // Pino PWM para motor 1
const int motorSpeedPin2 = 14;  // Pino PWM para motor 2


void setup() {
  // Define os pinos dos motores como saídas
  pinMode(motorPin1A, OUTPUT);
  pinMode(motorPin1B, OUTPUT);
  pinMode(motorSpeedPin1, OUTPUT);

  pinMode(motorPin2A, OUTPUT);
  pinMode(motorPin2B, OUTPUT);
  pinMode(motorSpeedPin2, OUTPUT);
}

void loop() {
  // Define a velocidade dos motores
  int speed1 = 255; // Velocidade do motor 1 (0 a 255)
  int speed2 = 255; // Velocidade do motor 2 (0 a 255)

  // Controla a direção dos motores
  digitalWrite(motorPin1A, HIGH);
  digitalWrite(motorPin1B, LOW); // Motor 1 para frente

  digitalWrite(motorPin2A, HIGH);
  digitalWrite(motorPin2B, LOW); // Motor 2 para frente

  // Define a velocidade dos motores usando PWM
  analogWrite(motorSpeedPin1, speed1);
  analogWrite(motorSpeedPin2, speed2);

  delay(100); // Espera 1 segundo

  int speed3 = 60; // Velocidade do motor 1 (0 a 255)
  int speed4 = 60; // Velocidade do motor 2 (0 a 255)

  // Controla a direção dos motores
  digitalWrite(motorPin1A, HIGH);
  digitalWrite(motorPin1B, LOW); // Motor 1 para frente

  digitalWrite(motorPin2A, HIGH);
  digitalWrite(motorPin2B, LOW); // Motor 2 para frente

  // Define a velocidade dos motores usando PWM
  analogWrite(motorSpeedPin1, speed3);
  analogWrite(motorSpeedPin2, speed4);
  delay(4000); // Espera 1 segundo
   // Define a velocidade dos motores
  int speed5 = 0; // Velocidade do motor 1 (0 a 255)
  int speed6 = 0; // Velocidade do motor 2 (0 a 255)

  // Controla a direção dos motores
  digitalWrite(motorPin1A, HIGH);
  digitalWrite(motorPin1B, LOW); // Motor 1 para frente

  digitalWrite(motorPin2A, HIGH);
  digitalWrite(motorPin2B, LOW); // Motor 2 para frente

  // Define a velocidade dos motores usando PWM
  analogWrite(motorSpeedPin1, speed5);
  analogWrite(motorSpeedPin2, speed6);
  delay(4000); // Espera 1 segundo

  int speed7 = 60; // Velocidade do motor 1 (0 a 255)
  int speed8 = 60; // Velocidade do motor 2 (0 a 255)

  // Controla a direção dos motores
  digitalWrite(motorPin1A, HIGH);
  digitalWrite(motorPin1B, LOW); // Motor 1 para frente

  digitalWrite(motorPin2A, HIGH);
  digitalWrite(motorPin2B, LOW); // Motor 2 para frente

  // Define a velocidade dos motores usando PWM
  analogWrite(motorSpeedPin1, speed7);
  analogWrite(motorSpeedPin2, speed8);
  delay(4000); // Espera 1 segundo
}