// #include <SoftwareSerial.h>
// SoftwareSerial node(A1, A0); 
 #define tempPin A0 
 #define voltPin A1 
 
 int voltValue; 
 double dutyCycle = 145; 
 int minDutyCycle = 102; 
 int maxDutyCycle = 153;
 
 double tempValue = 0;
 double OUTPUTatZERO = .500;
 double TEMPCOFF = .010; 
 double averageTempF = 0;
 double averageTempC = 0; 
 double totalTempF = 0;
 double totalTempC = 0;
 double averageValue; 
 double totalValue;
 
 void setup() {
  
  //bitwise operations that set the frequency of
  //either pin 3 or 11's PWM frequency to 31kHz
  TCCR2B = TCCR2B & B11111000 | B00000001;

  pinMode(3, OUTPUT);      //sets pin 3 used for PWM to output
  pinMode(tempPin, INPUT); //sets pin A0 used to read temp to input
  pinMode(voltPin, INPUT); //sets pin A1 used to read battery voltage to input  

  //sets baudrate
  Serial.begin(9600);
}

void loop() {

  //writes  PWM signal to pin 3 (first parameter)
  //with a duty cycle of the second parameter 
  //divided by 255

  voltValue = analogRead(voltPin); 
  //BOOST CONVERTER VOLTAGE CONTROL
  if (voltValue > 737) {            //greater than 3.6V
    dutyCycle = dutyCycle - 2;   //decrease duty cycle
    dutyCycle = min(maxDutyCycle, dutyCycle);
    displayDecreaseInfo(); 
  
    
  } else  {                      //less than 3.6V
    dutyCycle = dutyCycle + 2;   //increase duty cycle
    dutyCycle = max(minDutyCycle, dutyCycle);
    displayIncreaeInfo(); 
 
  }
  analogWrite(3, dutyCycle);      //sets dutycycle to PWM pin
  
   int numRead = 100;

   averageTempF = 0; 
   averageTempC = 0; 
   totalTempF = 0; 
   totalTempC = 0; 
   totalValue = 0; 
   for (int i = 0; i < numRead; i++) {

     tempValue = analogRead(tempPin);
     delay(10); 
     totalValue = totalValue + tempValue; 
      

     //converting analog readings to C and F temps
     double voltOut = tempValue * 0.004887;                  //convert analog value to voltage
     double actTempC =  (voltOut - OUTPUTatZERO) / TEMPCOFF; //convert voltage to temp in C based on equation in data sheet
     double actTempF = actTempC * 9/5 + 32;                  //convert C temp to F temp
 
     totalTempF = totalTempF + actTempF; 
     totalTempC = totalTempC + actTempC;

   } 
   
  averageTempF = totalTempF / numRead; 
  averageTempC = totalTempC / numRead;  
  //Serial.println("_____________________"); 
  Serial.print("Temperature in F: ");
  Serial.print(averageTempF); 
  Serial.println("F");
  Serial.print("Temperature in C: "); 
  Serial.print(averageTempC);
  Serial.println("C");
  Serial.println("_____________________");
  delay(1000);  
}

void displayIncreaeInfo() {
    Serial.println("The duty cycle has INCREASED"); 
    Serial.print("The voltage read: "); 
    Serial.println(voltValue * 0.004887);
    Serial.print("The dutyCycle: ");
    Serial.print((dutyCycle / 255) * 100);
    Serial.println("%"); 
}

void displayDecreaseInfo() {
    Serial.println("The duty cycle has DECREASED");
    Serial.print("The voltage read: "); 
    Serial.println(voltValue  * 0.004887);
    Serial.print("The dutyCycle: " );
    Serial.print((dutyCycle / 255) * 100);
    Serial.println("%"); 
}
