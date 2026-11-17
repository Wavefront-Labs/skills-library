---
id: computing-software.cybersecurity-defensive.zeek.websocket-api
name: websocket-api
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, websocket, external-clients, listen-websocket, use-websocket]
level: advanced
status: docs-checked
description: "Let external clients exchange Zeek events over WebSocket: UseWebSocket in zeekctl.cfg, Cluster::listen_websocket, websocat check, no authentication."
sources: ["https://docs.zeek.org/en/current/advanced/devel/websocket-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# websocket api

External clients can connect over WebSocket, subscribe to topics, and exchange Zeek events with cluster nodes and other clients. This is an alternative to the file-based Input and Configuration frameworks for runtime interaction.

For a zeekctl cluster, add to `zeekctl.cfg`:

```
UseWebSocket = 1
```

That enables a server on the manager, equivalent to:

```
event zeek_init()
    {
    if ( Cluster::local_node_type() == Cluster::MANAGER )
        Cluster::listen_websocket([$listen_addr=127.0.0.1, $listen_port=27759/tcp]);
    }
```

Check it with websocat. The empty array is the client's subscription list:

```
echo '[]' | websocat ws://127.0.0.1:27759/v1/messages/json
```

An ack message comes back, and `cluster.log` records the client connection.

Security: there is no authentication or authorisation. Any client can subscribe to every topic prefix and publish any event to any topic, so clients are implicitly trusted. Lock access down with a firewall, network namespaces, or a reverse proxy such as nginx or haproxy for basic or certificate authentication. TLS is supported, but a reverse proxy is the recommended place for it outside localhost.

## Checked

2026-11-08. Read the WebSocket API page in full; every claim confirmed.

Method: documentation only; no commands were run.
