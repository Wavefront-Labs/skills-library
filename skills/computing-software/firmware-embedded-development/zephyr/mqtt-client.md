---
id: computing-software.firmware-embedded-development.zephyr.mqtt-client
name: mqtt-client
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-mqtt, mqtt-connect, mqtt-publish, mqtt-input, mqtt-live, mqtt-tls, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run Zephyr's MQTT client: client struct setup, connect and the poll/mqtt_input/mqtt_live loop, publish/subscribe with QoS, TLS transport, and reconnect handling."
sources:
  - https://docs.zephyrproject.org/latest/connectivity/networking/api/mqtt.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/mqtt.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/lib/mqtt/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/ip/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT client

```
CONFIG_MQTT_LIB=y
CONFIG_MQTT_LIB_TLS=y            # for mqtts
CONFIG_NET_SOCKETS=y
```

## Setup
```c
#include <zephyr/net/mqtt.h>

static uint8_t rx_buf[256], tx_buf[256];
static struct mqtt_client client;
static struct net_sockaddr_storage broker;   /* 4.x names; old names need CONFIG_NET_NAMESPACE_COMPAT_MODE */

static void mqtt_evt(struct mqtt_client *c, const struct mqtt_evt *evt)
{
    switch (evt->type) {
    case MQTT_EVT_CONNACK:
        if (evt->result == 0) subscribe();
        break;
    case MQTT_EVT_PUBLISH: {
        const struct mqtt_publish_param *p = &evt->param.publish;
        uint8_t data[128];
        size_t len = MIN(p->message.payload.len, sizeof data);
        mqtt_read_publish_payload_blocking(c, data, len);   /* read the payload: the event only carries its size */
        if (p->message.topic.qos == MQTT_QOS_1_AT_LEAST_ONCE) {
            struct mqtt_puback_param ack = { .message_id = p->message_id };
            mqtt_publish_qos1_ack(c, &ack);
        }
        break;
    }
    case MQTT_EVT_DISCONNECT:
        connected = false;
        break;
    default: break;
    }
}

void client_init(void)
{
    mqtt_client_init(&client);
    client.broker = &broker;                       /* const void *, filled via zsock_getaddrinfo */
    client.evt_cb = mqtt_evt;
    client.client_id.utf8 = (uint8_t *)"dev-0001";
    client.client_id.size = strlen("dev-0001");
    client.protocol_version = MQTT_VERSION_3_1_1;
    client.rx_buf = rx_buf; client.rx_buf_size = sizeof rx_buf;
    client.tx_buf = tx_buf; client.tx_buf_size = sizeof tx_buf;
    client.keepalive = 60;
    client.transport.type = MQTT_TRANSPORT_SECURE;  /* or MQTT_TRANSPORT_NON_SECURE */
    struct mqtt_sec_config *tls = &client.transport.tls.config;
    static sec_tag_t tags[] = { CA_TAG };
    tls->peer_verify = ZSOCK_TLS_PEER_VERIFY_REQUIRED;
    tls->sec_tag_list = tags; tls->sec_tag_count = ARRAY_SIZE(tags);
    tls->hostname = "broker.example.com";           /* SNI + cert name check */
}
```

## Event loop
```c
mqtt_connect(&client);
struct zsock_pollfd fds = { .fd = client.transport.tls.sock /* or .tcp.sock */, .events = ZSOCK_POLLIN };

for (;;) {
    int rc = zsock_poll(&fds, 1, mqtt_keepalive_time_left(&client));
    if (rc > 0 && (fds.revents & ZSOCK_POLLIN)) mqtt_input(&client);   /* dispatches events */
    if (fds.revents & (ZSOCK_POLLERR | ZSOCK_POLLHUP)) break;
    mqtt_live(&client);                                                 /* sends PINGREQ when due */
}
mqtt_abort(&client);   /* then back off and reconnect */
```
`mqtt_input` is non-blocking, so wait on the socket with `poll` and call `mqtt_input` and `mqtt_live`
regularly. The headers document no thread-safety guarantees, so drive one client from one thread.

## Publish
```c
struct mqtt_publish_param p = {
    .message.topic.topic.utf8 = (uint8_t *)"dev/0001/temp",
    .message.topic.topic.size = strlen("dev/0001/temp"),
    .message.topic.qos = MQTT_QOS_1_AT_LEAST_ONCE,
    .message.payload.data = payload, .message.payload.len = len,
    .message_id = next_id++,
};
mqtt_publish(&client, &p);
```
Publish from the same thread as the loop, or serialise access with a mutex, because the headers
document no thread-safety guarantees.

## Gotchas
- The `MQTT_EVT_PUBLISH` event carries only the payload size: read the content with
  `mqtt_read_publish_payload*` (the header says it has to be read manually).
- Reconnect with exponential backoff and jitter; re-subscribe after each CONNACK (unless
  persistent session).
- The library supports MQTT 3.1.0, 3.1.1 and 5.0 (`MQTT_VERSION_5_0` needs `CONFIG_MQTT_VERSION_5_0`).

## Verify
- [ ] Survives broker restart: reconnects and resubscribes.
- [ ] Keepalive pings seen on the broker when idle.
- [ ] TLS hostname verification fails against a wrong host.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in include/zephyr/net/mqtt.h and the MQTT doc: functions mqtt_client_init, mqtt_connect, mqtt_input (non-blocking, use poll), mqtt_live, mqtt_keepalive_time_left, mqtt_abort, mqtt_publish, mqtt_subscribe, mqtt_read_publish_payload and the `_blocking` variant, mqtt_publish_qos1_ack; client fields broker (`const void *`), evt_cb, client_id, protocol_version, rx_buf/tx_buf and sizes, keepalive, transport.type, transport.tcp.sock, transport.tls.sock and transport.tls.config (peer_verify, sec_tag_list, sec_tag_count, hostname); MQTT_TRANSPORT_SECURE/NON_SECURE; events CONNACK, PUBLISH, DISCONNECT, SUBACK; Kconfig MQTT_LIB, MQTT_LIB_TLS and MQTT_VERSION_5_0; versions 3.1.0, 3.1.1 and 5.0.
Stale claims fixed: networking symbols are namespaced in 4.x (`net_sockaddr_storage`, `ZSOCK_TLS_PEER_VERIFY_REQUIRED`); the old names work only with CONFIG_NET_NAMESPACE_COMPAT_MODE (default y, to be removed). Removed unconfirmed statements about the library being unthreaded and about rx/tx buffer sizing.

Method: documentation only; no commands were run.
