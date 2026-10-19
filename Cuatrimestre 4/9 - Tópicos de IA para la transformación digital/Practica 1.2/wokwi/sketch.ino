/*
  Practica 1.2 - Monitoreo remoto de temperatura y humedad (IoT)
  Autor: Marco Sebastian Hernandez Parada

  ESP32 + DHT22 + 2 LEDs, comunicacion por WiFi usando MQTT.
  - LED rojo (GPIO 2): alerta local cuando la temperatura supera el umbral.
  - LED azul (GPIO 4): simula un ventilador controlado de forma remota.
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"

// Pines
const int PIN_DHT = 15;
const int PIN_LED_ALERTA = 2;
const int PIN_LED_VENTILADOR = 4;

// Red WiFi simulada de Wokwi
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

// Broker MQTT publico
const char* MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;

// Topicos (el prefijo debe ser unico porque el broker es publico)
#define TOPIC_BASE "mshp/iot/p12"
const char* TOPIC_TELEMETRIA = TOPIC_BASE "/telemetria";
const char* TOPIC_ESTADO = TOPIC_BASE "/estado";
const char* TOPIC_VENTILADOR_SET = TOPIC_BASE "/ventilador/set";
const char* TOPIC_UMBRAL_SET = TOPIC_BASE "/umbral/set";

const unsigned long INTERVALO_MS = 5000;

WiFiClient espClient;
PubSubClient mqtt(espClient);
DHTesp dht;

float umbral = 30.0;
String modoVentilador = "AUTO";  // AUTO, ON u OFF
bool ventiladorEncendido = false;
bool alerta = false;
float ultimaTemp = NAN;
float ultimaHum = NAN;
unsigned long ultimoEnvio = 0;

void conectarWiFi() {
  Serial.print("Conectando a WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS, 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("WiFi conectado. IP: ");
  Serial.println(WiFi.localIP());
}

void actualizarActuadores() {
  alerta = !isnan(ultimaTemp) && ultimaTemp > umbral;

  if (modoVentilador == "ON") {
    ventiladorEncendido = true;
  } else if (modoVentilador == "OFF") {
    ventiladorEncendido = false;
  } else {
    ventiladorEncendido = alerta;  // AUTO: sigue a la alerta
  }

  digitalWrite(PIN_LED_ALERTA, alerta ? HIGH : LOW);
  digitalWrite(PIN_LED_VENTILADOR, ventiladorEncendido ? HIGH : LOW);
}

void publicarTelemetria() {
  if (isnan(ultimaTemp) || isnan(ultimaHum)) return;

  char payload[200];
  snprintf(payload, sizeof(payload),
           "{\"temperatura\":%.1f,\"humedad\":%.1f,\"umbral\":%.1f,"
           "\"alerta\":%s,\"ventilador\":\"%s\",\"modo\":\"%s\"}",
           ultimaTemp, ultimaHum, umbral,
           alerta ? "true" : "false",
           ventiladorEncendido ? "ON" : "OFF",
           modoVentilador.c_str());

  mqtt.publish(TOPIC_TELEMETRIA, payload);
  Serial.print("Publicado -> ");
  Serial.println(payload);
}

void alRecibirMensaje(char* topic, byte* payload, unsigned int length) {
  String mensaje;
  for (unsigned int i = 0; i < length; i++) mensaje += (char)payload[i];
  mensaje.trim();
  Serial.printf("Mensaje recibido [%s]: %s\n", topic, mensaje.c_str());

  if (strcmp(topic, TOPIC_VENTILADOR_SET) == 0) {
    mensaje.toUpperCase();
    if (mensaje != "ON" && mensaje != "OFF" && mensaje != "AUTO") {
      Serial.println("Comando no valido (use ON, OFF o AUTO)");
      return;
    }
    modoVentilador = mensaje;
  } else if (strcmp(topic, TOPIC_UMBRAL_SET) == 0) {
    char* fin;
    float nuevo = strtof(mensaje.c_str(), &fin);
    if (fin == mensaje.c_str() || *fin != '\0' || nuevo < -40 || nuevo > 80) {
      Serial.println("Umbral no valido (numero entre -40 y 80)");
      return;
    }
    umbral = nuevo;
  }

  actualizarActuadores();
  publicarTelemetria();
}

void conectarMQTT() {
  while (!mqtt.connected()) {
    String clientId = "esp32-mshp-" + String(esp_random(), HEX);
    Serial.print("Conectando a MQTT...");
    // Last Will: si el ESP32 se desconecta, el broker publica "offline"
    if (mqtt.connect(clientId.c_str(), TOPIC_ESTADO, 1, true, "offline")) {
      Serial.println(" conectado");
      mqtt.publish(TOPIC_ESTADO, "online", true);
      mqtt.subscribe(TOPIC_VENTILADOR_SET);
      mqtt.subscribe(TOPIC_UMBRAL_SET);
    } else {
      Serial.printf(" fallo (rc=%d), reintento en 2 s\n", mqtt.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED_ALERTA, OUTPUT);
  pinMode(PIN_LED_VENTILADOR, OUTPUT);
  dht.setup(PIN_DHT, DHTesp::DHT22);

  conectarWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(alRecibirMensaje);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!mqtt.connected()) conectarMQTT();
  mqtt.loop();

  if (millis() - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = millis();
    TempAndHumidity datos = dht.getTempAndHumidity();
    if (dht.getStatus() != DHTesp::ERROR_NONE) {
      Serial.print("Error del sensor: ");
      Serial.println(dht.getStatusString());
      return;
    }
    ultimaTemp = datos.temperature;
    ultimaHum = datos.humidity;
    actualizarActuadores();
    publicarTelemetria();
  }
}
