---
id: computing-software.cloud-infrastructure-engineering.datadog.sensitive-data-scanner
name: sensitive-data-scanner
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, sensitive-data-scanner, pii-redaction, log-scrubbing, scanning-rules]
level: practitioner
status: docs-checked
description: "Redact PII and secrets from logs with Agent log_processing_rules and the cloud-side Sensitive Data Scanner."
sources: ["https://docs.datadoghq.com/agent/logs/advanced_log_collection/", "https://docs.datadoghq.com/security/sensitive_data_scanner/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive Data Scanner and log scrubbing
Goal: stop sensitive values reaching storage.

```yaml
# Agent-side masking (integration config file; example from the Datadog docs)
logs:
 - type: file
   path: /my/test/file.log
   service: cardpayment
   source: java
   log_processing_rules:
      - type: mask_sequences
        name: mask_credit_cards
        replace_placeholder: "[masked_credit_card]"
        pattern: (?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})
```

- In an integration config use `log_processing_rules`; in the Agent's main configuration the global equivalent is `processing_rules`.
- The Agent's `mask_sequences` type replaces every matched group with `replace_placeholder`. Containers use the `com.datadoghq.ad.logs` label or the pod annotation `ad.datadoghq.com`.
- Sensitive Data Scanner (cloud): set up a scanning group (what to scan), then scanning rules, either from the Scanning Rule Library (emails, credit card numbers, API keys, tokens, and more) or your own regex.
- Actions per rule: Redact, Partially redact, Hash (all sources), and Mask (logs, APM spans and RUM events; users with `Data Scanner Unmask` can unmask).
- It scans logs, APM spans, RUM events, events, Agent Observability traces, S3 buckets and code repositories.
- Cloud scanning happens in the Datadog backend during processing, so data leaves your environment before redaction but is redacted before indexing and display. Agent-side rules scrub before sending, so use both for defence in depth.
- The Findings page lists matches by rule; notification rules for logs do not include log samples.

Gotcha: with cloud scanning the raw data does leave your environment first, so use Agent-side rules for values that must never leave the host.

## Verify
- A test log containing a fake card number arrives masked in the Log Explorer.

## Checked
2026-11-09. Confirmed against the Advanced Log Collection page (`log_processing_rules`, `mask_sequences`, `replace_placeholder`, Docker label, Kubernetes annotation, the card example) and the Sensitive Data Scanner page (actions and support table, Mask and Data Scanner Unmask, scanning groups and rules, library, regex, backend processing note, sources, Findings, notification note). Removed: my own card regex and `/var/log/myapp` path (replaced by the docs example), "test regexes for performance", the claim that earlier-ingested logs stay unmasked and the rotate-credentials advice, non-production scoping advice, and the redacted-event-count monitoring advice.
Method: documentation only; no commands were run.
