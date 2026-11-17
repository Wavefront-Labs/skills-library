---
id: computing-software.firmware-embedded-development.esp-idf.esp-mqtt-client
name: esp-mqtt-client
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-networking, esp-mqtt, mqtts, last-will, qos, mqtt-outbox, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Connect ESP32 devices to an MQTT broker with ESP-MQTT: TLS and client certs, LWT, subscribing on connect, publish vs enqueue, fragmented messages and reconnect behaviour."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/mqtt.rst
  - https://github.com/espressif/esp-mqtt/blob/master/include/mqtt_client.h
  - https://github.com/espressif/esp-mqtt/blob/master/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP-MQTT client
From ESP-IDF v6.0 the ESP-MQTT component lives in its own repository and is added to a project with `idf.py add-dependency espressif/mqtt`; the API below is the same `mqtt_client.h` API.

## Configure and start
```c
#include "mqtt_client.h"
#include "esp_crt_bundle.h"

static esp_mqtt_client_handle_t client;

void mqtt_start(void)
{
    esp_mqtt_client_config_t cfg = {
        .broker.address.uri = "mqtts://broker.acme.example:8883",
        .broker.verification.crt_bundle_attach = esp_crt_bundle_attach,
        .credentials.client_id = device_id,          /* unique per device */
        .credentials.authentication.certificate = dev_cert_pem,   /* mTLS, or username/password */
        .credentials.authentication.key = dev_key_pem,
        .session.keepalive = 60,                      /* default 120 s; the client talks to the broker at half this interval */
        .session.last_will = { .topic = status_topic, .msg = "offline",
                               .qos = 1, .retain = 1 },
        .network.reconnect_timeout_ms = 10000,
    };
    client = esp_mqtt_client_init(&cfg);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event, NULL);
    esp_mqtt_client_start(client);                   /* runs its own task, auto-reconnects */
}
```

## Events
```c
static void mqtt_event(void *arg, esp_event_base_t base, int32_t id, void *data)
{
    esp_mqtt_event_handle_t e = data;
    switch ((esp_mqtt_event_id_t)id) {
    case MQTT_EVENT_CONNECTED:
        esp_mqtt_client_subscribe(client, cmd_topic, 1);           /* (re)subscribe every time */
        esp_mqtt_client_publish(client, status_topic, "online", 0, 1, 1);
        break;
    case MQTT_EVENT_DATA:
        /* large messages arrive in pieces */
        handle_chunk(e->topic, e->topic_len, e->data, e->data_len,
                     e->current_data_offset, e->total_data_len);
        break;
    case MQTT_EVENT_DISCONNECTED: set_offline(); break;
    case MQTT_EVENT_ERROR:
        log_mqtt_error(e->error_handle);   /* esp_tls error codes, connect return code */
        break;
    default: break;
    }
}
```
`topic` and `data` are **not** NUL-terminated; use the lengths. For fragmented messages
`topic` is only set on the first fragment.

## Publish vs enqueue
- `esp_mqtt_client_publish(...)`: QoS 0 messages are sent immediately in the calling task (and return -1 while disconnected); QoS 1/2 messages are queued in the outbox, even when disconnected. It returns the packet identifier, -1 on failure and -2 when the outbox is full. Never call it from ISRs. With `CONFIG_MQTT_SKIP_PUBLISH_IF_DISCONNECTED` it always returns -1 while disconnected.
- `esp_mqtt_client_enqueue(..., store)`: puts the message in the outbox to be sent later; with `store=true` all QoS levels are enqueued, otherwise only QoS 1 and 2. Same return values.
QoS 1/2 messages stay in the outbox until acknowledged; expiry is configurable
(`CONFIG_MQTT_OUTBOX_EXPIRED_TIMEOUT_MS`), and RAM grows if the broker is unreachable. Cap what
you publish while offline.

## Session and reconnect
- Clean session is the default; set `.session.disable_clean_session = true` to ask the broker to keep the session across reconnects. Still resubscribe on CONNECTED to be safe.
- The client reconnects by itself unless `.network.disable_auto_reconnect` is set (retry interval `.network.reconnect_timeout_ms`). Don't call stop/start on every disconnect; that fights the
  built-in logic.
- Keep the event handler short and hand long work off to a queue, so the client task is not held up.

## Verify
- [ ] Broker restart: device reconnects, resubscribes, and the LWT/online status is correct.
- [ ] Large payload (larger than buffer size) is reassembled correctly.
- [ ] Offline for an hour: memory stays bounded; queued QoS 1 messages delivered after reconnect.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the ESP-IDF MQTT page, mqtt_client.h and the esp-mqtt Kconfig: component moved out of ESP-IDF in v6.0 (espressif/mqtt), config structure (broker.address.uri, verification.crt_bundle_attach, credentials.client_id and authentication certificate/key, session.last_will fields, keepalive default 120 s, disable_clean_session, network.reconnect_timeout_ms and disable_auto_reconnect), event IDs, fragmented DATA events with topic only on the first, publish and enqueue semantics and return values, CONFIG_MQTT_OUTBOX_EXPIRED_TIMEOUT_MS, MQTT_SKIP_PUBLISH_IF_DISCONNECTED. Wrong: publish was described as blocking until written for QoS 1/2 (it queues them in the outbox); the v6.0 component move was missing. Removed the unconfirmed broker-disconnect claim about slow handlers.
Method: documentation only; no commands were run.
