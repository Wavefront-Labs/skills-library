---
id: computing-software.cloud-infrastructure-engineering.observability.redacting-pii-and-secrets-in-log-pipelines
name: redacting-pii-and-secrets-in-log-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-redaction-pipeline, pii-scrubbing, structured-logging, redaction-processor, data-privacy]
level: advanced
status: docs-checked
description: "Scrub PII and secrets from logs before storage: OTel redaction and transform processors, Alloy stage.replace and loki.secretfilter, and canary verification."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor", "https://grafana.com/docs/alloy/latest/reference/components/loki/loki.secretfilter/", "https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/#stagereplace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redacting PII and secrets in the pipeline

## Layers (defence in depth)
1. **App**: never log credentials, tokens, full card numbers, passwords. Hash identifiers you need to join on.
2. **Agent/collector**: regex and key-based scrubbing for what slips through. The redaction processor README itself calls the processor one line of defence, not the only compliance measure.
3. **Backend**: access control, plus a deletion path for incidents.

## OTel Collector
```yaml
processors:
  redaction:
    allow_all_keys: true
    blocked_values:
      - "4[0-9]{12}(?:[0-9]{3})?"                 # Visa
      - "(5[1-5][0-9]{14})"                       # MasterCard
    blocked_key_patterns: [".*token.*", ".*api_key.*"]
    hash_function: hmac-sha256                    # optional; masks with a fixed string if unset
    hmac_key: "${env:REDACTION_SECRET_KEY}"
    summary: info                                 # adds redaction.masked.count etc.; silent removes them
  transform/pii:
    log_statements:
      - context: log
        statements:
          - replace_pattern(body, "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[a-z]{2,}", "<email>")
          - set(attributes["user.id"], SHA256(attributes["user.id"])) where attributes["user.id"] != nil
          - delete_key(attributes, "http.request.header.authorization")
```
- `allowed_keys` fails closed: if it is empty and `allow_all_keys` is false, every attribute is removed. `blocked_values` apply to the values of allowed keys, in the order listed. `allowed_values` wins over `blocked_values`.
- Masking uses `****` by default (`masking_string`). Supported `hash_function` values: `md5`, `sha1`, `sha3`, `hmac-sha256`, `hmac-sha512`. `md5` and `sha1` are rejected in FIPS mode; the README recommends HMAC variants for low-entropy data such as IP addresses.
- `summary` is `debug` (counts and key names), `info` (counts only) or `silent`. Audit attributes are named `redaction.redacted.count`, `redaction.masked.count`, `redaction.allowed.count` and so on.
- The processor works on span, log and datapoint attributes and reports on map-shaped log bodies; for free-text string bodies use the transform processor's `replace_pattern`. `delete_key`, `replace_pattern`, `set` and `SHA256` are OTTL functions.

## Alloy
```alloy
loki.process "scrub" {
  stage.replace {
    expression = "(?i)password=(\\S+)"
    replace    = "****"
  }
  forward_to = [loki.write.default.receiver]
}
loki.secretfilter "s" { forward_to = [loki.process.scrub.receiver] }
```
- `stage.replace` takes an RE2 `expression` with capture groups, and each capture group is replaced by `replace` (an empty `replace` omits the captured text). Backslashes in the expression must be escaped as in `"\\w*"`. `source` selects an extracted value instead of the log line.
- `loki.secretfilter` detects secrets with regex patterns from an embedded Gitleaks config (or a custom Gitleaks-style file). It works on log lines only, not labels or metadata; PII is out of scope and some secrets may remain; scanning can raise CPU use significantly. Grafana says not to rely on it alone.

## Verify
Send a canary log containing a fake card number, a `password=` pair and an email address; assert that none appear raw in the backend. Run it in CI against the pipeline config.

## Gotchas
- Regex costs CPU per line; measure collector CPU after adding patterns.
- Redact before any buffer (queue or message bus), or raw PII sits in the buffer.
- Masking the body does not touch already-extracted labels or attributes; redact both.

## Checked
Date: 2026-11-09. Confirmed in the redactionprocessor README (options, defaults, hash functions, FIPS note, summary levels, audit attribute names, map body reporting), the OTTL functions README (delete_key, replace_pattern, set, SHA256 exist), the Alloy loki.process stage.replace section and the loki.secretfilter page. Removed: the OWASP source (not confirmed), in-app library names, Fluent Bit filters, Loki delete requests, the card-number replace template using $1 (Alloy replace is a Go template, not shown to accept $1), the LogQL canary query and the claim that the processor ignores log bodies entirely.
Method: docs-checked 2026-11-09 against the redactionprocessor README, the OTTL functions README, and the Grafana Alloy loki.process and loki.secretfilter pages.
