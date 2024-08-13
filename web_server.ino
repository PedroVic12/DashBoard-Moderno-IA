#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char *ssid = "**********";
const char *password = "*********";
const int led = 2;

ESP8266WebServer server(80);

void handleRoot()
{
    digitalWrite(led, 1);

    String textoHTML;

    textoHTML = "Ola!! Aqui &eacute; o <b>ESP8266</b> falando! ";
    textoHTML += "Porta A0: ";
    textoHTML += analogRead(A0);

    server.send(200, "text/html", textoHTML);
    digitalWrite(led, 0);
}

class WebServer
{
private:
    ESP8266WebServer server;
    int ledPin;
    String textoHTML;

public:
    WebServer(int ledPin)
    {
        this->ledPin = ledPin;
        server.begin();
    }

    void setup()
    {
        pinMode(ledPin, OUTPUT);
        digitalWrite(ledPin, LOW);
    }

    void loop()
    {
        server.handleClient();
        if (server.uri() == "/")
        {
            handleRoot();
        }
        else
        {
            handleNotFound();
        }
    }

    void handleRoot()
    {
        digitalWrite(led, 1);

        String textoHTML;

        textoHTML = "Ola!! Aqui &eacute; o <b>ESP8266</b> falando! ";
        textoHTML += "Porta A0: ";
        textoHTML += analogRead(A0);

        server.send(200, "text/html", textoHTML);
        digitalWrite(led, 0);
    }
    void handleNotFound()
    {
        digitalWrite(led, 1);
        String message = "File Not Found\n\n";
        message += "URI: ";
        message += server.uri();
        message += "\nMethod: ";
        message += (server.method() == HTTP_GET) ? "GET" : "POST";
        message += "\nArguments: ";
        message += server.args();
        message += "\n";
        for (uint8_t i = 0; i < server.args(); i++)
        {
            message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
        }
        server.send(404, "text/plain", message);
        digitalWrite(led, 0);
    }
};

WebServer webServer(LED_BUILTIN);

//! SKETCH ARDUINO

void connectServer()
{
    pinMode(led, OUTPUT);
    digitalWrite(led, 0);
    Serial.println("Conectando ao servidor...");
    Serial.begin(115200);
    Wifi.mode(WIFI_STA);
    Wifi.begin(ssid, password);

    while (Wifi.status() != WL_CONNECTED)
    {
        delay(500);

        Serial.print(".");
        escreve();
    }
}

void escreve()
{
    Serial.println("Conectado ao servidor");
    Serial.println(ssid);
    Seriaç.println(" IP Address");
    Serial.println(Wifi.localIP());

    if (MDNS.begin("esp3266"))
    {
        Serial.println("Responder started");
        // MDNS.addService("http", "tcp", 80);
    }

    webServer.on("/", handleRoot);
    webServer.on("/inline", []()
                 { webServer.send(200, "text/plain", "this works as well"); });
    webServer.onNotFound(handleNotFound);
    webServer.begin();
    Serial.println("HTTP Web server Started - By PV Peter Parker");
}

void setup()
{
    // webServer.setup();
    connectServer();
}

void loop()
{
    webServer.loop();

    Serial.println("End pointing...");
    delay(1000);
}