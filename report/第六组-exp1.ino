/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);//信号灯
  pinMode(10, INPUT);//传感器
}

int last = 1;
int now = 1;

void loop() {
  //判断有无障碍  1：有障碍   0： 无障碍
  int now = digitalRead(10);
  if(now != last){
    if(now == 0){
      Serial.print("yes");
      //digitalWrite(LED_BUILTIN, HIGH);
      }
    else{
      Serial.print("no");
      //digitalWrite(LED_BUILTIN, LOW);
    }
  }
  last = now;

  String ctrl = Serial.readString();
  Serial.println(ctrl);
  if(ctrl[0]=='0' ){
    //南北
    Serial.println("ctrl=='0'");
    digitalWrite(3, LOW);
    digitalWrite(2, HIGH);

    digitalWrite(6, LOW);
    digitalWrite(7, LOW);

    digitalWrite(8, LOW);
    digitalWrite(9, LOW);

    digitalWrite(12, LOW);
    digitalWrite(13, LOW);
    
  }
  if(ctrl[0]=='1' ){
    Serial.println("ctrl=='1'");
    digitalWrite(3, LOW);
    digitalWrite(2, LOW);

    digitalWrite(6, HIGH);
    digitalWrite(7, LOW);

    digitalWrite(8, LOW);
    digitalWrite(9, LOW);

    digitalWrite(12, LOW);
    digitalWrite(13, LOW);
  }
  if(ctrl[0]=='2' ){
    Serial.println("ctrl=='2'");
    digitalWrite(3, LOW);
    digitalWrite(2, LOW);

    digitalWrite(6, LOW);
    digitalWrite(7, LOW);

    digitalWrite(8, LOW);
    digitalWrite(9, HIGH);

    digitalWrite(12, LOW);
    digitalWrite(13, LOW);
   }
  if(ctrl[0]=='3' ){
    Serial.println("ctrl=='3'");
    digitalWrite(3, LOW);
    digitalWrite(2, LOW);

    digitalWrite(6, LOW);
    digitalWrite(7, LOW);

    digitalWrite(8, LOW);
    digitalWrite(9, LOW);

    digitalWrite(12, HIGH);
    digitalWrite(13, LOW);
  }
}
