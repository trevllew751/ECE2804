void setup() {
  // put your setup code here, to run once:
  TCCR2B = TCCR2B & B11111000 | B00000001;
  pinMode(3, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(3, 135);
}
