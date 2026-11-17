---
id: computing-software.messaging-and-integration.redpanda.http-proxy-produce-and-fetch-over-rest
name: http-proxy-produce-and-fetch-over-rest
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [http-proxy, pandaproxy, rest-api, port-8082, produce, fetch, basic-auth, oidc]
level: practitioner
status: docs-checked
description: "Produce and fetch records through Redpanda HTTP Proxy on port 8082, with the vnd.kafka content types and SCRAM Basic or OIDC bearer authentication."
sources:
  - https://docs.redpanda.com/streaming/current/develop/http-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTP Proxy (`pandaproxy`) is a REST API for listing topics and brokers, producing and fetching events, and consumer groups. It is enabled by default on port 8082; change it in `redpanda.yaml`:

```yaml
pandaproxy:
  pandaproxy_api:
    - address: 0.0.0.0
      port: 8082
```

**Authentication** depends on the `authentication_method` broker property and `http_authentication` cluster settings. With SCRAM, pass Basic auth; with OIDC, a bearer token:

```bash
curl -s -u "<username>:<password>" "http://<host-address>:8082/topics"
curl -s -H "Authorization: Bearer <oidc-token>" "http://<host-address>:8082/topics"
```

**Produce.** POST to `/topics/<topic>` with `Content-Type: application/vnd.kafka.json.v2+json` and a body of the form `{"records":[...]}`. The reply lists the partition and offset of each record, for example `{"offsets":[{"partition":0,"offset":0},...]}`.

**Fetch from one partition.** GET `/topics/test_topic/partitions/0/records?offset=0&timeout=1000&max_bytes=100000` with `Accept: application/vnd.kafka.json.v2+json`.

To create a test topic: `rpk topic create test_topic -p 3`.

The `$base_uri/brokers` and `$base_uri/topics` endpoints list brokers and topics. For exploring endpoints, run Swagger UI in Docker and point it at `http://<host-address>:8082/v1`.

## Checked

Port, YAML, authentication forms, content types, fetch URL, the brokers and topics endpoints and the Swagger tip were confirmed on the HTTP Proxy page, read in full.

Method: docs-checked 2026-11-09 against the Use Redpanda with the HTTP Proxy API page, read in full; no commands were run.
