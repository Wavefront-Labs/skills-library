---
id: computing-software.cybersecurity-defensive.trivy.custom-compliance-spec-yaml
name: custom-compliance-spec-yaml
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [custom-compliance, compliance-spec, controls, avd-id, node-collector, trivy-checks]
level: advanced
status: docs-checked
description: "Write a custom compliance YAML with controls mapped to AVD check IDs, load it with --compliance @path, and understand the command and node-collector fields for built-ins."
sources:
  - https://trivy.dev/latest/docs/guide/compliance/compliance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A custom report is a YAML document with a top-level `spec`:

```yaml
spec:
  id: "k8s-myreport"
  title: "My custom Kubernetes report"
  description: "Describe your report"
  relatedResources:
    - https://some.url
  version: "1.0"
  controls:
    - name: "Non-root containers"
      description: 'Check that container is not running as root'
      id: "1.0"
      checks:
        - id: AVD-KSV-0012
      severity: "MEDIUM"
```

Field notes from the comments in the page: `id` is unique and must not contain spaces; `title` and `name` are one-line; `relatedResources` takes URLs only; `version` is a string; each control has an `id` string and a list of existing Trivy checks. A check ID must start with `AVD-` or `CVE-`. The control `severity` is what the report shows; the severity of the underlying checks is not used.

The check ID refers to a check by its AVD ID, found in the check source metadata header or on the Aqua vulnerability DB misconfiguration and vulnerability pages.

Select your spec by file path, with `@` marking a path instead of an ID:

```
trivy --compliance @</path/to/compliance.yaml>
```

Contributing built-ins: specs in the CIS style add `platform`, `type` and `version`, and controls can carry `commands` entries such as `CMD-0001`. Commands (`id`, `key`, `title`, `nodeType` worker or master, `audit` shell command, `platforms`) are run by the node collector, which writes results into a `NodeInfo` resource that Rego checks evaluate. The `key` must match the key name the Rego check reads.

## Checked

2026-11-03. Read and confirmed against the Built-in Compliance Reports page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
