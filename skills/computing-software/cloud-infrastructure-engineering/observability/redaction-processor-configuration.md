---
id: computing-software.cloud-infrastructure-engineering.observability.redaction-processor-configuration
name: redaction-processor-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [redaction-processor-config, sensitive-data-masking, transforming-telemetry, otel-collector, pii-scrubbing]
level: advanced
status: docs-checked
description: "Configure the OTel redaction processor: allowlist vs allow_all_keys, blocked values and key patterns, hashing, ignored keys, summary attributes, and testing coverage."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor", "https://opentelemetry.io/docs/security/handling-sensitive-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redaction processor configuration

The redaction processor enforces an attribute policy on spans, logs and metric datapoints. For logs with a map body it also
reports on and filters the body map keys. It is intended as one line of defence, not the only compliance measure.

## Allowlist mode (strictest)
```yaml
processors:
  redaction/strict:
    allow_all_keys: false
    allowed_keys: [http.request.method, http.route, http.response.status_code, url.scheme, error.type,
                   db.system.name, db.operation.name, messaging.system, rpc.method]
    ignored_keys: [trace.sampled]          # neither redacted nor checked
    summary: info                           # adds redaction.redacted.keys / .count attributes
```
Any attribute not listed is **deleted**. Good for egress to third parties.

## Blocklist mode
```yaml
processors:
  redaction/pii:
    allow_all_keys: true
    blocked_key_patterns: [".*token.*", ".*password.*", ".*secret.*", "^http\\.request\\.header\\.authorization$"]
    blocked_values:
      - "4[0-9]{12}(?:[0-9]{3})?"           # Visa PAN
      - "5[1-5][0-9]{14}"                   # Mastercard
      - "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"   # email
    allowed_values: [".+@example\\.com"]   # exceptions to blocked_values
    hash_function: sha3                     # hash matches instead of asterisks
    summary: debug
```
Matched parts of values in `blocked_values` are masked with a fixed length of asterisks (or hashed); the values of keys matching
`blocked_key_patterns` are masked. `allowed_values` takes precedence over `blocked_values`. Patterns apply in the listed order.
Supported `hash_function` values: `md5`, `sha1`, `sha3` (SHA-256), `hmac-sha256`, `hmac-sha512`; the HMAC variants need
`hmac_key` (for example `${env:REDACTION_SECRET_KEY}`) and are recommended for low-entropy data such as IP addresses.
Other options: `ignored_key_patterns` (regexes for keys to pass untouched), `redact_all_types: true` (check non-string values
such as ints), `url_sanitizer` and `db_sanitizer` (strip variable parts of URLs and database queries).

## Placement
Agents (before data leaves the node) or the gateway before any external exporter. The processor only sees data that has
already been produced, so put it after any processor that creates attributes.

## Summary attributes
`summary: debug` adds the redacted, masked and allowed key names plus counts; `info` only counts; `silent` adds nothing.
The README warns that a list of redacted attributes can leak information, so avoid `debug` toward third parties.
Attributes added: `redaction.redacted.keys`/`.count`, `redaction.masked.keys`/`.count`, `redaction.allowed.keys`/`.count`,
`redaction.ignored.count` (and `redaction.body.*` for log bodies); zero counts are not emitted.

## Test
Send a fixture containing known fake secrets through the pipeline with `summary: debug`, then confirm the exported data
contains no raw values and that the `redaction.*` attributes list what you expect.

## Checked

2026-10-24. OpenTelemetry Collector contrib redaction processor README (main branch). Confirmed: fail-closed `allowed_keys` and `allow_all_keys`, `ignored_keys`, `blocked_key_patterns`, `blocked_values`, `allowed_values` precedence, supported `hash_function` values and `hmac_key`, `summary` levels (`debug`, `info`, `silent`) and the `redaction.*` audit attribute names, and that log body maps are processed.

Method: documentation only; no commands were run.
