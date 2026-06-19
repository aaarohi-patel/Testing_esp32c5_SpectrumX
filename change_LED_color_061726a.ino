#define BUTTON_PIN 2 //button
#define BUZZER_PIN 3 //buzzer

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP); // Use internal pull-up resistor; automatically turns HIGH
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(BUZZER_PIN, LOW); //buzzer starts silent

}

void loop() {
  int buttonState = digitalRead(BUTTON_PIN);

 
  if (buttonState == LOW) {
    Serial.println("Button Pressed -> Buzzer BEEPING");
    // digitalWrite(BUZZER_PIN, HIGH);
    tone(BUZZER_PIN, 1000);
  } else {
    // Button is released
    // digitalWrite(BUZZER_PIN, LOW);   //stops active buzzer
    noTone(BUZZER_PIN);
 
  }

  delay(50); // delay to help debounce the button 

}
