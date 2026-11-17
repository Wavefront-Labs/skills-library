---
id: computing-software.cybersecurity-defensive.trivy.secret-config-file-and-custom-rules
name: secret-config-file-and-custom-rules
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [secret-config, trivy-secret-yaml, custom-rules, regex, keywords, secret-group-name]
level: practitioner
status: docs-checked
description: "Define custom secret detection rules in trivy-secret.yaml or a file given by --secret-config, including required fields, keywords and Go regexp caveats."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/secret/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy loads `trivy-secret.yaml` from the current directory by default. If it does not exist, only built-in rules are used. Change the path with `--secret-config`.

Trivy uses the Go regexp package, so to use `^` and `$` as line begin and end you must use multi-line mode, `(?m)`.

A custom rule:

```yaml
rules:
  - id: rule1
    category: general
    title: Generic Rule
    severity: HIGH
    path: .*\.sh
    keywords:
      - secret
    regex: (?i)(?P<key>(secret))(=|:).{0,5}['"](?P<secret>[0-9a-zA-Z\-_=]{8,64})['"]
    secret-group-name: secret
    allow-rules:
      - id: skip-text
        description: skip text files
        path: .*\.txt
```

Fields:
- `id` (required): unique identifier.
- `category` (required): string for metadata and reporting.
- `title` (required): short human-readable title.
- `severity` (required): CRITICAL, HIGH, MEDIUM or LOW.
- `regex` (required): Go regular expression that detects secrets.
- `path` (optional): Go regular expression matching file paths.
- `keywords` (optional, recommended): pre-regex filter. A quick case-insensitive string comparison (ASCII letters only) runs first. An empty keyword, or one with a non-ASCII letter that has upper and lower case such as `ö`, skips the check and runs the regex on all content, which is slower.
- `allow-rules` (optional): per-rule allow rules.

## Checked

2026-11-03. Read and confirmed against the Secret Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
