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

const int led = 2;

void handleRoot() {
  digitalWrite(led, 1);
  digitalWrite(led, 0);
}

void handleNotFound(){
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void setup(void){
  pinMode(2, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println(ssid);
  Serial.println(WiFi.localIP());
  server.on("/", handleRoot);
  server.on("/pin", HTTP_GET, pin);
  server.on("/inline", [](){
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);
  server.begin();
}

void loop(void){
  server.handleClient();
}

// String html = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>209bot</title></head><body bgcolor=\"DeepSkyBlue\"><p style=\"margin-top: 5vh;font-size: 200px;color: #fff;margin: 0;\">:(</p><p style=\"font-size: 30px;color: #fff;\">&#x60A8;&#x8BBF;&#x95EE;&#x7684;&#x9875;&#x9762;&#x8FD8;&#x5728;&#x7F8E;&#x5316;&#x4E2D;,&#x4F46;&#x662F;&#x529F;&#x80FD;&#x5B8C;&#x5168;&#x5B9E;&#x73B0;</p><p style=\"text-align: center;font-size: 100px;margin: 0;\">209&#x5BBF;&#x820D;&#x706F;&#x63A7;&#x7CFB;&#x7EDF;</p><p style=\"text-align: center;font-size: 25px;\">209 Dormitory light control system</p><p style=\"text-align: center; margin-top: 5vh;\"><a href=\"./pin?light=on\" ><input type=\"button\" value=\"&#x5F00;&#x706F;\" style=\"width:200px;height:160px;font-size:80px;\"></a></p><p style=\"text-align: center;\"><a href=\"./pin?light=off\"><input type=\"button\" value=\"&#x5173;&#x706F;\" style=\"width:200px;height:160px;font-size:80px;\"></a></p><p style=\"text-align: center;font-size: 40px;margin: 0;margin-top: 10vh\">&#x96BE;&#x770B;&#x662F;&#x96BE;&#x770B;&#x4E86;&#x70B9;,&#x4F46;......</p><p style=\"text-align: center;\"><img src=\"http://keai.icu/static/login/ybsbny.jpg\"></p><p style=\"text-align: center;font-size: 30px;margin: 0\">&#x8981;&#x602A;&#x5C31;&#x602A;ESP8266&#x5185;&#x5B58;&#x592A;&#x5C0F;&#x4E86;</p><p style=\"text-align: center;font-size: 20px;margin:0;color:#fff;margin-top:5vh\">209Bot-Project</p><p style=\"text-align: center;font-size: 20px;margin:0;color:#fff\">Power by: Emp-project | Evileyesaint</p></body></html>";
