 int tempPin = A0; 
 double tempValue = 0;
 double OUTPUTatZERO = .500;
 double TEMPCOFF = .010; 
 double averageTempF = 0;
 double averageTempC = 0; 
 double totalTempF = 0;
 double totalTempC = 0;
 void setup() {
  //bitwise operations that set the frequency of
  //either pin 3 or 11's PWM frequency to 31kHz
  TCCR2B = TCCR2B & B11111000 | B00000001;

  //sets pin 3 to output mode
  pinMode(3, OUTPUT); 
  pinMode(tempPin, INPUT); 

  
  Serial.begin(9600);
}

void loop() {

  //writes  PWM signal to pin 3 (first parameter)
  //with a duty cycle of the second parameter 
  //divided by 255
  analogWrite(3, 170); 

   int numRead = 10;

   averageTempF = 0; 
   averageTempC = 0; 
   totalTempF = 0; 
   totalTempC = 0; 
   for (int i = 0; i <= numRead; i++) {

     tempValue = analogRead(tempPin);

     //converting analog readings to C and F temps
     double voltOut = tempValue * 0.004887;                  //convert analog value to voltage
     double actTempC =  (voltOut - OUTPUTatZERO) / TEMPCOFF; //convert voltage to temp in C based on equation in data sheet
     double actTempF = actTempC * 9/5 + 32;                  //convert C temp to F temp
  
     totalTempF = totalTempF + actTempF; 
     totalTempC = totalTempC + actTempC;
      
   }

  averageTempF = totalTempF / numRead; 
  averageTempC = totalTempC / numRead;  

  Serial.println(averageTempF);
  delay(500);  
}
