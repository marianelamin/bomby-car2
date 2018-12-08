/*
 WiFi Web Server LED Blink

 A simple web server that lets you blink an LED via the web.
 This sketch will print the IP address of your WiFi Shield (once connected)
 to the Serial monitor. From there, you can open that address in a web browser
 to turn on and off the LED on pin 5.

 If the IP address of your shield is yourAddress:
 http://yourAddress/H turns the LED on
 http://yourAddress/L turns it off

 This example is written for a network using WPA encryption. For
 WEP or WPA, change the Wifi.begin() call accordingly.

 Circuit:
 * WiFi shield attached
 * LED attached to pin 5

 created for arduino 25 Nov 2012
 by Tom Igoe

ported for sparkfun esp32 
31.01.2017 by Jan Hendrik Berlin
 
 */

#include <WiFi.h>
#include <ArduinoJson.h>

const char* ssid     = "thor";
const char* password = "ironman32";

//WiFiServer server(80);
WiFiServer server(5005);

void setup()
{
    Serial.begin(115200);
    pinMode(13, OUTPUT);      // set the LED pin mode
    pinMode(2,OUTPUT);    // status pin inboard
    delay(20);


    // We start by connecting to a WiFi network
digitalWrite(2, HIGH);
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        if (digitalRead(2) == LOW)
          {
            digitalWrite(2, HIGH);
          }
          else{
            digitalWrite(2, LOW);
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
    digitalWrite(2, LOW);
    
    server.begin();

}
int number = 0;
int value = 0;

void loop(){
 WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    digitalWrite(2, HIGH);
    number = number+1;
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    String request= "";
    while (client.connected()) {            // loop while the client's connected
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
          digitalWrite(13, HIGH);               // GET /H turns the LED on
        Serial.println("\nL requested: Move left");
        request = "L requested: Move left";
        }
        else if (currentLine.endsWith("GET /R")) {
          digitalWrite(13, LOW);                // GET /L turns the LED off
        Serial.println("\nR requested: Move right");
        request = "R requested: Move right";
        }
        else if (currentLine.endsWith("GET /S")){
          Serial.println("\nS requested: stop");
          request = "S requested: stop";
          }
        else if (currentLine.endsWith("GET /B")){
          Serial.println("\nB requested: start");
          request = "B requested: start";
          }
       }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
  digitalWrite(2, LOW);
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
