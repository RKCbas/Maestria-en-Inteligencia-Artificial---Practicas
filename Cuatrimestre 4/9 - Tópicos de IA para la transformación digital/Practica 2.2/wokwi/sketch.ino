/*
  Practica 2.2 - Controlador difuso Mamdani para ventilacion (IA aplicada al IoT)
  Autor: Marco Sebastian Hernandez Parada

  ESP32 + DHT22 + LED (ventilador por PWM) + LCD 16x2 I2C, telemetria por MQTT.
  Entradas: temperatura (0-50 C) y humedad relativa (0-100 %).
  Salida:   velocidad del ventilador (0-100 %).
  Inferencia Mamdani: AND = min, implicacion = min, agregacion = max,
  defuzzificacion por centroide sobre un universo discreto con paso de 0.5.
  Es la traduccion directa de la implementacion en Python del notebook.
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHTesp.h"

// Pines
const int PIN_DHT = 15;
const int PIN_VENTILADOR = 4;  // LED azul que representa el ventilador (PWM)

// Red WiFi simulada de Wokwi y broker MQTT publico
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";
const char* MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* TOPIC_TELEMETRIA = "mshp/iot/p22/telemetria";

const unsigned long INTERVALO_MS = 2500;  // el DHT22 necesita al menos 2 s entre lecturas
const unsigned long REINTENTO_MQTT_MS = 5000;

// Conjunto difuso trapezoidal (a, b, c, d); un triangulo es un trapecio con b == c
struct Conjunto {
  const char* nombre;
  float a, b, c, d;
};

// Variables linguisticas (mismos parametros que en Python)
const Conjunto TEMPERATURA[3] = {
  { "Fria", 0, 0, 10, 20 },
  { "Templada", 10, 20, 25, 35 },
  { "Caliente", 25, 35, 50, 50 }
};
const Conjunto HUMEDAD[3] = {
  { "Baja", 0, 0, 20, 50 },
  { "Media", 20, 50, 50, 80 },
  { "Alta", 50, 80, 100, 100 }
};
const Conjunto VELOCIDAD[3] = {
  { "Baja", 0, 0, 0, 50 },
  { "Media", 25, 50, 50, 75 },
  { "Alta", 50, 100, 100, 100 }
};

// Base de reglas: REGLAS[temperatura][humedad] = indice del conjunto de VELOCIDAD
enum { V_BAJA = 0, V_MEDIA = 1, V_ALTA = 2 };
const int REGLAS[3][3] = {
  //  H Baja  H Media  H Alta
  { V_BAJA, V_BAJA, V_MEDIA },  // T Fria
  { V_BAJA, V_MEDIA, V_ALTA },  // T Templada
  { V_MEDIA, V_ALTA, V_ALTA }   // T Caliente
};

const float PASO = 0.5;
const int PUNTOS = 201;  // 0, 0.5, ..., 100

WiFiClient espClient;
PubSubClient mqtt(espClient);
DHTesp dht;
LiquidCrystal_I2C lcd(0x27, 16, 2);
unsigned long ultimoEnvio = 0;
unsigned long ultimoIntentoMQTT = 0;

// Resultado de una inferencia, util para mostrar el seguimiento paso a paso
struct Resultado {
  float muT[3];
  float muH[3];
  float activacion[3];
  float velocidad;
};

float trapmf(float x, const Conjunto& s) {
  if (x < s.a || x > s.d) return 0.0;
  if (x >= s.b && x <= s.c) return 1.0;
  if (x < s.b) return (x - s.a) / (s.b - s.a);
  return (s.d - x) / (s.d - s.c);
}

Resultado mamdani(float temp, float hum) {
  Resultado r;
  temp = constrain(temp, 0.0, 50.0);
  hum = constrain(hum, 0.0, 100.0);

  // 1. Fuzzificacion
  for (int i = 0; i < 3; i++) {
    r.muT[i] = trapmf(temp, TEMPERATURA[i]);
    r.muH[i] = trapmf(hum, HUMEDAD[i]);
    r.activacion[i] = 0.0;
  }

  // 2. Evaluacion de reglas (AND = min) y union por consecuente (max)
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      float fuerza = min(r.muT[i], r.muH[j]);
      int k = REGLAS[i][j];
      r.activacion[k] = max(r.activacion[k], fuerza);
    }
  }

  // 3. Implicacion (min) y agregacion (max) punto a punto
  // 4. Defuzzificacion por centroide
  float num = 0.0, den = 0.0;
  for (int p = 0; p < PUNTOS; p++) {
    float z = p * PASO;
    float mu = 0.0;
    for (int k = 0; k < 3; k++) {
      mu = max(mu, min(r.activacion[k], trapmf(z, VELOCIDAD[k])));
    }
    num += z * mu;
    den += mu;
  }
  r.velocidad = (den > 0.0) ? num / den : 0.0;
  return r;
}

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

// Intento no bloqueante: el control difuso sigue funcionando aunque no haya broker
void conectarMQTT() {
  if (ultimoIntentoMQTT != 0 && millis() - ultimoIntentoMQTT < REINTENTO_MQTT_MS) return;
  ultimoIntentoMQTT = millis();
  String clientId = "esp32-mshp-" + String(esp_random(), HEX);
  Serial.print("Conectando a MQTT...");
  if (mqtt.connect(clientId.c_str())) {
    Serial.println(" conectado");
  } else {
    Serial.printf(" fallo (rc=%d)\n", mqtt.state());
  }
}

void mostrarLCD(float temp, float hum, float vel) {
  char linea[17];
  lcd.setCursor(0, 0);
  snprintf(linea, sizeof(linea), "T:%4.1fC H:%4.1f%%", temp, hum);
  lcd.print(linea);
  lcd.setCursor(0, 1);
  snprintf(linea, sizeof(linea), "Ventilador:%4.0f%%", vel);
  lcd.print(linea);
}

void publicarTelemetria(float temp, float hum, const Resultado& r) {
  if (!mqtt.connected()) return;
  char payload[200];
  snprintf(payload, sizeof(payload),
           "{\"temperatura\":%.1f,\"humedad\":%.1f,\"velocidad\":%.2f,"
           "\"activacion\":{\"baja\":%.2f,\"media\":%.2f,\"alta\":%.2f}}",
           temp, hum, r.velocidad,
           r.activacion[V_BAJA], r.activacion[V_MEDIA], r.activacion[V_ALTA]);
  mqtt.publish(TOPIC_TELEMETRIA, payload);
  Serial.print("Publicado -> ");
  Serial.println(payload);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_VENTILADOR, OUTPUT);
  dht.setup(PIN_DHT, DHTesp::DHT22);

  lcd.init();
  lcd.backlight();
  lcd.print("Control difuso");
  lcd.setCursor(0, 1);
  lcd.print("Mamdani - P2.2");

  conectarWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
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

    Resultado r = mamdani(datos.temperature, datos.humidity);
    analogWrite(PIN_VENTILADOR, (int)round(r.velocidad * 255.0 / 100.0));
    mostrarLCD(datos.temperature, datos.humidity, r.velocidad);

    Serial.printf("T=%.1f C  H=%.1f %%\n", datos.temperature, datos.humidity);
    Serial.printf("  muT [Fria, Templada, Caliente] = [%.2f, %.2f, %.2f]\n",
                  r.muT[0], r.muT[1], r.muT[2]);
    Serial.printf("  muH [Baja, Media, Alta]        = [%.2f, %.2f, %.2f]\n",
                  r.muH[0], r.muH[1], r.muH[2]);
    Serial.printf("  Activacion [Baja, Media, Alta] = [%.2f, %.2f, %.2f]\n",
                  r.activacion[0], r.activacion[1], r.activacion[2]);
    Serial.printf("  Velocidad del ventilador       = %.2f %%\n", r.velocidad);
    publicarTelemetria(datos.temperature, datos.humidity, r);
  }
}
