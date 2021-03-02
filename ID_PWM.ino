 int tempPin = A0; 
 double tempValue = 0;
 double OUTPUTatZERO = .500;
 double TEMPCOFF = .010; 
 void setup() {
  //bitwise operations that set the frequency of
  //either pin 3 or 11's PWM frequency to 31kHz
  TCCR2B = TCCR2B & B11111000 | B00000001;

  //sets pin 3 to output mode
  pinMode(3, OUTPUT); 

  Serial.begin(9600);
}

void loop() {

  //writes  PWM signal to pin 3 (first parameter)
  //with a duty cycle of the second parameter 
  //divided by 255
  analogWrite(3, 170); 
  tempValue = analogRead(tempPin); 
  double voltOut = tempValue * 0.004887;
  double actTempC =  (voltOut - OUTPUTatZERO) / TEMPCOFF;
  double actTempF = actTempC * 9/5 + 32;  
  Serial.println(actTempF);
  delay(100);
}
