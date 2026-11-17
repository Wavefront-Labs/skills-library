---
id: computing-software.messaging-and-integration.redpanda.http-proxy-consumer-groups-over-rest
name: http-proxy-consumer-groups-over-rest
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [http-proxy, consumer-groups, rest-api, subscription, offsets, pandaproxy]
level: practitioner
status: docs-checked
description: "Run a consumer group through HTTP Proxy: create the consumer, subscribe it to a topic, poll records and read offsets using the v2 content types and instance URLs."
sources:
  - https://docs.redpanda.com/streaming/current/develop/http-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Consuming through HTTP Proxy takes separate calls: create a consumer in a group, subscribe the instance to a topic, then fetch records. Assume `base_uri="http://<host-address>:8082"`.

**1. Create the consumer.** POST to `/consumers/<group>` with `Content-Type: application/vnd.kafka.v2+json`:

```bash
curl -s \
  -X POST \
  "$base_uri/consumers/test_group" \
  -H "Content-Type: application/vnd.kafka.v2+json" \
  -d '{
  "format":"json",
  "name":"test_consumer",
  "auto.offset.reset":"earliest",
  "auto.commit.enable":"false",
  "fetch.min.bytes": "1",
  "consumer.request.timeout.ms": "10000"
}'
```
The reply returns an `instance_id` and a `base_uri` such as `http://127.0.0.1:8082/consumers/test_group/instances/test_consumer`.

**2. Subscribe** with a POST to `/consumers/test_group/instances/test_consumer/subscription` (same content type) listing the topics, for example the body `{"topics": ["test_topic"]}`. The expected response is HTTP 204 with no body.

**3. Retrieve events** with GET `/consumers/test_group/instances/test_consumer/records?timeout=1000&max_bytes=100000` and `Accept: application/vnd.kafka.json.v2+json`. The page's examples run this call as the step after subscribing.

**4. Offsets.** Send a `partitions` list of topic and partition objects to `/consumers/test_group/instances/test_consumer/offsets` to read committed offsets (the page's curl and Python examples disagree on GET versus POST for this call, so confirm it in the HTTP Proxy API reference). To commit, POST to the same path with an `offset` added to each `partitions` entry; there is no response body.

**5. Delete** the consumer with DELETE on `/consumers/test_group/instances/test_consumer`. Consumers expire after five minutes of inactivity, so consume in a loop; an expired consumer can be recreated with the same name.

Content types differ: instance management uses `application/vnd.kafka.v2+json`; record payloads use `application/vnd.kafka.json.v2+json`.

## Checked

Endpoints, payload fields, reply fields, content types, the subscription body, and the commit and delete calls were confirmed on the HTTP Proxy page, read in full. The offsets read call is left unspecified because the page's examples conflict.

Method: docs-checked 2026-11-09 against the Use Redpanda with the HTTP Proxy API page, read in full; no commands were run.
