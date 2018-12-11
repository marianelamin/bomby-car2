/*
  
*/

#include <WiFi.h>
#include <ArduinoJson.h>

const char* ssid     = "Min_iPhone";
const char* password = "123456789";

//WiFiServer server(80);
WiFiServer server(5005);
const int trigPin = 15;
const int echoPin = 5;
const int inBoardLed = 2;
const int anotherPin = 13;


// distance sensor variable
int  sensorPin =  0;
long duration;
int distance;
int prevState =-1;
int number = 0;
int value = 0;

void setup()
{
  Serial.begin(115200);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(anotherPin, OUTPUT);      // set the LED pin mode
  pinMode(inBoardLed, OUTPUT);   // status pin inboard
  delay(20);


  // We start by connecting to a WiFi network
  digitalWrite(inBoardLed, HIGH);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (digitalRead(inBoardLed) == LOW)
    {
      digitalWrite(inBoardLed, HIGH);
    }
    else {
      digitalWrite(inBoardLed, LOW);
    }
    /*TODO:
      1. offer a default wifi connection and then change it to
      a customized network, by asking the user to input ssid and password
    */
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(inBoardLed, LOW);

  server.begin();

}


void loop() {
  WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    digitalWrite(inBoardLed, HIGH);
    number = number + 1;
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    String request = "";
    while (client.connected()) {            // loop while the client's connected
      togglePin(inBoardLed);
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {

            // Allocate JsonBuffer
            // Use arduinojson.org/assistant to compute the capacity.
            StaticJsonBuffer<500> jsonBuffer;

            // Create the root object
            JsonObject& root = jsonBuffer.createObject();

            // Create the "analog" array
            JsonArray& analogValues = root.createNestedArray("analog");
            for (int pin = 0; pin < 5; pin++) {
              // Read the analog input
              int value = pin;

              // Add the value at the end of the array
              analogValues.add(value);
            }

            // Create the "digital" array
            JsonArray& digitalValues = root.createNestedArray("digital");
            for (int pin = 4; pin > 0; pin--) {
              // Read the digital input
              int value = pin;

              // Add the value at the end of the array
              digitalValues.add(value);
            }
            root["numero"] = number;
            root["request"] = request;
            root["dist"] = getDistance();


            Serial.print(F("Sending: "));
            root.printTo(Serial);
            Serial.println();

            // Write response headers
            client.println("HTTP/1.0 200 OK");
            client.println("Content-Type: application/json");
            client.println("Connection: close");
            client.println();

            // Write JSON document
            root.printTo(client);

            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        // Check to see what the client request was
        if (currentLine.endsWith("GET /L")) {
//          digitalWrite(anotherPin, HIGH);               // GET /H turns the LED on
          Serial.println("\nL requested: Move left");
          request = "L requested: Move left";
        }
        else if (currentLine.endsWith("GET /R")) {
          
          Serial.println("\nR requested: Move right");
          request = "R requested: Move right";
        }
        else if (currentLine.endsWith("GET /S")) {
          Serial.println("\nS requested: stop");
          digitalWrite(anotherPin, LOW);
          request = "S requested: stop";
        }
        else if (currentLine.endsWith("GET /B")) {
          Serial.println("\nB requested: start");
          digitalWrite(anotherPin, HIGH);
          delay(20);
          digitalWrite(anotherPin, LOW);
          request = "B requested: start";
        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
    digitalWrite(inBoardLed, LOW);
  }
  
}

int getDistance()
{
  digitalWrite(trigPin, LOW);
delayMicroseconds(2);

// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);

// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);

// Calculating the distance
distance= duration*0.034/2;

// Prints the distance on the Serial Monitor
Serial.print("Distance: ");
Serial.println(distance);
return distance;
  }


void togglePin(int pin){
    if(digitalRead(pin) == LOW)
    digitalWrite(pin, HIGH);
    else{
    digitalWrite(pin, LOW);
    }
    
    }

//JsonObject& gatherInformation(int num){
//  // Allocate JsonBuffer
//  // Use arduinojson.org/assistant to compute the capacity.
//  StaticJsonBuffer<500> jsonBuffer;
//
//  // Create the root object
//  JsonObject& root = jsonBuffer.createObject();
//
//  // Create the "analog" array
//  JsonArray& analogValues = root.createNestedArray("analog");
//  for (int pin = 0; pin < 6; pin++) {
//    // Read the analog input
//    int value = pin;
//
//    // Add the value at the end of the array
//    analogValues.add(value);
//  }
//
//  // Create the "digital" array
//  JsonArray& digitalValues = root.createNestedArray("digital");
//  for (int pin = 14; pin > 0; pin--) {
//    // Read the digital input
//    int value = pin;
//
//    // Add the value at the end of the array
//    digitalValues.add(value);
//  }
//  root["numero"] = num;


//  return root;
//  }
