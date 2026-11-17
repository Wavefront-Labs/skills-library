---
id: computing-software.systems-network-administration.healthchecks.arduino-ping
name: arduino-ping
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, arduino, arduinohttpclient, wifinina, embedded-heartbeat]
level: practitioner
status: docs-checked
description: "Send an HTTPS ping to Healthchecks from an Arduino board using ArduinoHttpClient and WiFiNINA, with a GET to the check's UUID path."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/arduino.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ArduinoHttpClient is the most straightforward option. The docs example uses WiFiNINA and was tested on the Arduino Nano 33 IoT. The library also works with the Ethernet and ESP8266WiFi network libraries.

```
#include <ArduinoHttpClient.h>
#include <WiFiNINA.h>

WiFiSSLClient wifi;
HttpClient client = HttpClient(wifi, "hc-ping.com", 443);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  WiFi.begin("your-network-ssid", "your-network-password");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  client.get("/your-uuid-here");
  Serial.println(client.responseStatusCode());
  Serial.println(client.responseBody());
}

void loop() {
}
```

Points:
- It connects to `hc-ping.com` on port 443 over SSL and GETs the check-specific path (the check's UUID).
- Credentials and UUID are hardcoded for simplicity; for real projects the docs suggest keeping them in SECRET_ fields.
## Checked

2026-11-04. Confirmed against the Healthchecks Arduino page: ArduinoHttpClient as the easiest option, WiFiNINA tested on the Arduino Nano 33 IoT, Ethernet and ESP8266WiFi compatibility, hc-ping.com on port 443, the UUID path GET, and the SECRET_ fields advice. Removed the claim that a 200 status with body OK means the ping was recorded, which the page does not state.

Method: documentation only; no commands were run.
