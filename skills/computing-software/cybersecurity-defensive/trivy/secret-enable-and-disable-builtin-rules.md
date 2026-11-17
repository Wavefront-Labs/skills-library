---
id: computing-software.cybersecurity-defensive.trivy.secret-enable-and-disable-builtin-rules
name: secret-enable-and-disable-builtin-rules
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [enable-builtin-rules, disable-rules, disable-allow-rules, rule-ids, markdown, performance]
level: practitioner
status: docs-checked
description: "Narrow secret scanning to chosen built-in rule IDs, drop noisy rules, or disable built-in allow rules such as markdown, and know which setting wins when both are set."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/secret/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All built-in rules are enabled by default, so scanning with all of them takes time. Two settings in the secret config file narrow that.

`enable-builtin-rules` lists the only built-in rule IDs to run. All other rules are disabled, so scanning is much faster, and the page strongly recommends it if you do not need every rule. For AWS only:

```yaml
enable-builtin-rules:
  - aws-access-key-id
  - aws-account-id
  - aws-secret-access-key
```

`disable-rules` removes specific rules. If you do not use Slack, disable its rules to reduce false positives. You can also disable built-in allow rules with `disable-allow-rules`. Markdown files are ignored by default; adding `markdown` to `disable-allow-rules` makes Trivy scan them.

```yaml
disable-rules:
  - slack-access-token
  - slack-web-hook
disable-allow-rules:
  - markdown
```

Specify either `enable-builtin-rules` or `disable-rules`. If both are given, `disable-rules` takes precedence: if `github-pat` appears in both, it is disabled.

Choose `enable-builtin-rules` when you need only a few detections, for example only AWS; choose `disable-rules` when you only want to remove some built-in rules. The secret scanning page links the full lists of built-in rule IDs and built-in allow rule IDs.

## Checked

2026-11-03. Read and confirmed against the Secret Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: the claim that the full rule lists are in the source files builtin-rules.go and builtin-allow-rules.go (the page only links the lists).

Method: documentation only; no commands were run.
