#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "homenetwork";
const char* password = "88888888";
ESP8266WebServer server(80);

void pin(){
  if(server.arg("light")=="on"){
    digitalWrite(2, 0);
  }
  if(server.arg("light")=="off"){
    digitalWrite(2, 1);
  }
}
void setup(void){
  pinMode(2, OUTPUT);
  digitalWrite(2, 0);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println(ssid);
  Serial.println(WiFi.localIP());
  server.on("/pin", HTTP_GET, pin);
  server.begin();
}

void loop(void){
  server.handleClient();
}