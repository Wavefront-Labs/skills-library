---
id: computing-software.cybersecurity-defensive.trivy.secret-allow-rules
name: secret-allow-rules
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [allow-rules, false-positives, known-secrets, path-allow, regex-allow, global-allow]
level: practitioner
status: docs-checked
description: "Suppress known or test secrets with global and per-rule allow-rules matched by regex or path in Trivy's secret configuration."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/secret/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Allow rules reduce false positives for known secrets. If a detected secret matches the allow rule `regex`, it is skipped and not reported. The same logic applies to `path`. Allow rules can be defined globally at the top level and per rule inside a rule; the fields are the same.

```yaml
rules:
  - id: rule1
    category: general
    title: Generic Rule
    severity: HIGH
    regex: (?i)(?P<key>(secret))(=|:).{0,5}['"](?P<secret>[0-9a-zA-Z\-_=]{8,64})['"]
    allow-rules:
      - id: skip-text
        description: skip text files
        path: .*\.txt
allow-rules:
  - id: social-security-number
    description: skip social security number
    regex: 219-09-9999
```

Fields:
- `id` (required): unique identifier for the allow rule.
- `description` (optional): short human-readable description.
- `regex` (optional): Go regular expression used to allow detected secrets.
- `path` (optional): Go regular expression used to allow matched paths.

Either `regex` or `path` must be specified.

A path-based global example from the page's full sample skips a log directory:

```yaml
allow-rules:
  - id: log-dir
    description: skip log directory
    path: ^\/var\/log\/
```

Trivy also ships built-in allow rules, for instance Markdown files are ignored by default. See the enable and disable rules skill to turn those off.

## Checked

2026-11-03. Read and confirmed against the Secret Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
