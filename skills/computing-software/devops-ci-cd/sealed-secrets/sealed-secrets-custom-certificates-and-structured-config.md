---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-custom-certificates-and-structured-config
name: sealed-secrets-custom-certificates-and-structured-config
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, bring-your-own-certificates, config-template, structured-config, faq]
level: advanced
status: docs-checked
description: "Know the supported workarounds for custom certificates and for updating single fields inside a structured config file stored in a sealed Secret."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets custom certificates and structured config

Two frequent questions have documented workarounds rather than built-in features.

Bring your own certificates. The controller can consume pre-generated certificates; the README points to a dedicated document (docs/bring-your-own-certificates.md in the repository) describing the workaround.

Updating part of a JSON, YAML or TOML file held in a secret. A Kubernetes Secret is a flat map of key/value pairs. SealedSecrets work at that level and are agnostic about value content, so they cannot update an individual field inside a structured config file. For legacy applications the project ships an example of a workaround (docs/examples/config-template in the repository); the README says `template.data` can be used to template complex values on the Secret.

Related community tooling listed in the README includes `kseal`, `kubeseal-convert`, a Visual Studio Code extension, WebSeal (generates secrets in the browser) and a TypeScript HybridEncrypt implementation. These are third-party.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), FAQ sections on custom certificates and structured files, Related projects, template section.
Confirmed: both workarounds exist and where the README points, flat key/value reasoning, related projects list.
Removed: the step-by-step description of the config-template example (the example directory was not read).
Method: documentation only; no commands were run.
