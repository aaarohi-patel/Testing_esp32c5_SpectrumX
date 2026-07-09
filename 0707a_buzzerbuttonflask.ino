// #define BUTTON_PIN 2  // button
// #define BUZZER_PIN 3  // buzzer

// bool lastPressed = false;  // remember last state so we only report changes

// void setup() {
//   Serial.begin(115200);

//   pinMode(BUTTON_PIN, INPUT_PULLUP);  // internal pull-up; released reads HIGH
//   pinMode(BUZZER_PIN, OUTPUT);

//   digitalWrite(BUZZER_PIN, LOW);  // buzzer starts silent
// }

// void loop() {
//   bool pressed = (digitalRead(BUTTON_PIN) == LOW);  // LOW = pressed

//   // --- buzzer logic (unchanged) ---
//   if (pressed) {
//     tone(BUZZER_PIN, 1000);
//   } else {
//     noTone(BUZZER_PIN);
//   }

//   // --- tell the dashboard, only on a state change ---
//   if (pressed != lastPressed) {
//     Serial.println(pressed ? "1" : "0");
//     lastPressed = pressed;
//   }

//   delay(50);  // simple debounce
// }



#define BUTTON_PIN 2
#define BUZZER_PIN 3

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(BUZZER_PIN, LOW);  // buzzer starts silent
}

void loop() {
  int rawValue = digitalRead(BUTTON_PIN);

  if (rawValue == LOW) {
    // button is pressed
    tone(BUZZER_PIN, 1000);
    Serial.println("1");
  } else {
    // button is not pressed
    noTone(BUZZER_PIN);
    Serial.println("0");
  }

  delay(200);
}




