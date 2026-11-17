---
id: computing-software.cybersecurity-defensive.splunk.http-event-collector-setup
name: http-event-collector-setup
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, http-event-collector, hec, indexer-acknowledgement, inputs-conf, token-management, load-balancer]
level: practitioner
status: draft
description: "Stand up Splunk HTTP Event Collector: tokens scoped to index and sourcetype, indexer acknowledgement, load-balanced endpoints and how to verify delivery."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector", "https://docs.splunk.com/Documentation/Splunk/latest/Data/AboutHECIDXAck", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Inputsconf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splunk HTTP Event Collector (HEC)

**Goal:** accept JSON/raw events over HTTPS from apps, cloud services and collectors
without a forwarder, with one token per source and no silent loss.

## 1. Enable and create tokens
Global settings (Settings > Data inputs > HTTP Event Collector > Global Settings): enable,
keep SSL on, default port 8088. On indexers or heavy forwarders behind a load balancer,
push the same config from the cluster manager / deployment server:
```
# inputs.conf
[http]
disabled = 0
enableSSL = 1
port = 8088

[http://aws_firehose]
token = <generated-guid>
index = aws
indexes = aws
sourcetype = aws:cloudwatchlogs
useACK = 1
disabled = 0
```
- One token per source system. `indexes` restricts where the sender may write; without it a
  sender can set `"index"` in the payload and write anywhere the token owner can.
- Generate the GUID once and distribute the identical stanza to every receiver behind the
  load balancer, otherwise requests fail on whichever node lacks the token.

## 2. Send and test
```
curl -k https://hec.example.internal:8088/services/collector/event \
  -H "Authorization: Splunk <token>" \
  -d '{"time":1760600000,"host":"app01","sourcetype":"myapp:json","event":{"action":"login","user":"alice"}}'
```
Endpoints: `/services/collector/event` (JSON envelope, timestamp from `time`),
`/services/collector/raw` (line-broken by props.conf like file input),
`/services/collector/health` (LB health check, no token needed).

## 3. Indexer acknowledgement
With `useACK = 1` the sender must pass a channel GUID and poll for acks:
```
curl ... -H "X-Splunk-Request-Channel: <channel-guid>" -d '...'   # returns {"ackId":7}
curl ... /services/collector/ack -d '{"acks":[7]}'                # {"acks":{"7":true}}
```
Only enable ACK when the sender implements polling (Firehose, OTel collector and Splunk
Connect for Kubernetes do). A client that ignores acks fills the channel quota
(`maxEventsPerChannel`) and then gets HTTP 503s. LB stickiness by channel header is needed
because acks are tracked per receiver.

## 4. Response codes worth knowing
`0 Success`, `2/3 token disabled/invalid` (HTTP 403/401), `6 invalid data format`,
`7 incorrect index` (index not in `indexes` or does not exist), `9 server busy` (queue
full, back off), `12 event field is required`.

## Gotchas
- `time` must be epoch seconds (decimals allowed). Milliseconds land events in the year 57000.
- Events to `/event` skip line breaking but still go through timestamp and TRANSFORMS rules.
- Tokens are bearer secrets; store them in the sender's secret store and rotate by adding a
  second token, moving senders, then disabling the old one.
- A TLS terminating load balancer must forward the `Authorization` header unchanged.

## Verify
```
index=_internal sourcetype=splunkd component=HttpInputDataHandler (ERROR OR WARN)
| stats count by message
index=_introspection component=HttpEventCollector | stats sum(data.num_of_events) by data.token_name
```
Every token should show steady event counts and zero parse errors.
