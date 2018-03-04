#include <Wire.h>

int cmd = 0;

void setup() {
  Wire.begin(0x55);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent); 
  Serial.begin(9600);           
  Serial.println("i2c slave ready.");
}

void loop() {
  delay(100);
}

// Реализовать для себя !!!!!!!
// true - когда надо выключить
// false - когда не надо
bool canShutdown()
{
  return true;
}

void requestEvent()
{
  if (cmd == 1)
  switch (canShutdown())
  {
    case true:
      Wire.write(0x01);
      break;
    case false:
      Wire.write(0x05);
      break;
  }
  else
    Wire.write(0x03);
}

void receiveEvent(int howMany)
{
  while (Wire.available() > 0)
  {
    char c = Wire.read(); // receive byte as a character
    Serial.println(c);         // print the character
    if (c == 'U')
    {
      cmd = 1;
    }
    else
    {
      cmd = 0;  
    }
  }  
}
