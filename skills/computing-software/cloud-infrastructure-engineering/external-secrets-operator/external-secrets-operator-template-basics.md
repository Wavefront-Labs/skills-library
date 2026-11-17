---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-template-basics
name: external-secrets-operator-template-basics
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [templating, go-template, target-template, engineversion]
level: practitioner
status: docs-checked
description: "Transform provider data into a Secret with spec.target.template, Go template rules, dashed keys with index and Helm escaping."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.target.template` lets ESO transform provider data before it is stored as a `Kind=Secret`. Every data value is a Go template, and referencing a key that does not exist raises an error rather than being silently empty.

```yaml
spec:
  target:
    template:
      engineVersion: v2
      data:
        config.yaml: |
          username: {{ .username }}
          password: {{ .password }}
```

Notes from the docs:
- Use camelCase for `spec.data[].secretKey` (for example `serviceAccountToken`) so it is easy to reference.
- If a key contains dashes, reference it with `index`: `{{ index .data "service-account-token" }}`.
- Installing the ExternalSecret through Helm: Helm would render `{{ }}` itself, so escape the template, most simply with backtick raw string constants.
- Templates can inject several keys into one config file mounted into a pod, or define multiple output keys in the same Secret.

## Checked

2026-11-03. Claims were read against guides/templating.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
