---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.remote-write-2-protocol
name: remote-write-2-protocol
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, remote-write, remote-write-2-protocol, prw2, protobuf-message, native-histograms, metadata, string-interning]
level: advanced
status: verified
description: "Adopt Prometheus Remote-Write 2.0 (protobuf_message io.prometheus.write.v2.Request): what it adds, sender/receiver config, fallback, and checking it is in use."
sources: ["https://prometheus.io/docs/specs/prw/remote_write_spec_2_0/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote-Write 2.0

## What changes vs 1.0
| | 1.0 (`prometheus.WriteRequest`) | 2.0 (`io.prometheus.write.v2.Request`) |
|---|---|---|
| Labels | repeated strings per series | string-interned symbol table (smaller payloads, less CPU) |
| Metadata (type, help, unit) | separate, best-effort | inline per series |
| Native histograms, exemplars, created timestamps | partial | first class |
| Response | status code only | `X-Prometheus-Remote-Write-*-Written` response headers (mandatory) report samples/histograms/exemplars actually written |
Content-Type: `application/x-protobuf;proto=io.prometheus.write.v2.Request`, snappy-compressed.

## Sender (Prometheus 3.x)
```yaml
remote_write:
  - url: https://receiver.example.com/api/v1/write
    protobuf_message: io.prometheus.write.v2.Request    # default prometheus.WriteRequest (1.0)
```
For the v2 message `send_native_histograms` is a no-op (always true) and `metadata_config.send` is redundant (3.15.1 logs
`usage of 'metadata_config.send' is redundant when using remote write v2`): metadata is taken from the WAL for every series.
No feature flag was needed on the sender in 3.15.1.

## Receiver (Prometheus as receiver)
`--web.enable-remote-write-receiver`. Prometheus 3.15.1 accepted both messages with only that flag; to restrict it, repeat
`--web.remote-write-receiver.accepted-protobuf-messages=<message>` once per message (a comma-separated list is rejected at start-up).
A receiver that does not accept the message answers `415 Unsupported Media Type` (a sender with `io.prometheus.write.v2.Request`
against a receiver restricted to `prometheus.WriteRequest` logged `non-recoverable error ... 415` and dropped the batch); the
sender must be switched back to 1.0, there is no automatic downgrade in the config. Check other backends' documentation.

## Why bother
- Smaller payloads: for 100 series with short names sending the same 2,100 samples, v1 sent 18,692 bytes and v2 16,834 (about 10 %);
  the saving grows with longer and more numerous labels.
- Metadata (type, help, unit) travels with the series.
- Partial-write accounting lets senders detect silently dropped data.

## Gotchas
- Mixing 1.0 and 2.0 senders on one receiver is fine when the receiver accepts both messages (it did in the test).
- Proxies or gateways that inspect/rewrite payloads must understand the new message or pass it through untouched.

## Verify
- [ ] `prometheus_http_requests_total{handler="/api/v1/write"}` on the receiver shows `204` and no `415`.
- [ ] `prometheus_remote_storage_bytes_total` dropped compared to 1.0 for the same series.
- [ ] Native histogram queries at the receiver return data.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), Prometheus Operator API reference (main), jq 1.8.2.
- Three sender/receiver pairs: a v2 sender to a default receiver (204, samples queryable with external labels), a v2 sender to a receiver started with `--web.remote-write-receiver.accepted-protobuf-messages=prometheus.WriteRequest` (415, `non-recoverable error`, batch dropped), and a v1 and a v2 sender scraping the same 100-series target into one receiver (`prometheus_remote_storage_bytes_total` 18,692 against 16,834, both 2,100 samples). A comma-separated value for the accepted-messages flag made the server exit at start-up.
- `metadata_config.send` warning: sender log. `send_native_histograms` no-op for v2 and `protobuf_message` default: 3.15 configuration page.
- Content type `application/x-protobuf;proto=...`, snappy, the mandatory `X-Prometheus-Remote-Write-*-Written` headers and the 415 rule: remote-write 2.0 specification on prometheus.io.
