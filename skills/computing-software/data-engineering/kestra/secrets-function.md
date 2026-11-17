---
id: computing-software.data-engineering.kestra.secrets-function
name: secrets-function
category: computing-software
field: data-engineering
product: kestra
tags: [secrets, secret-function, oss, env-variables, namespaces]
level: practitioner
status: docs-checked
description: "Keep credentials out of Kestra flow YAML with the secret() function, reading across namespaces, and how OSS differs from the Enterprise secrets manager."
sources:
  - https://kestra.io/docs/concepts/secret
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Secrets hold API keys, passwords and certificates outside flow definitions and are injected at runtime.

```yaml
message: "{{ secret('API_TOKEN') }}"
```

In the Enterprise Edition, `secret()` reads by default from the flow's own namespace; pass a `namespace` argument to read a secret stored in a different namespace of the same tenant. The secret resolves using the target namespace's own backend:

```yaml
message: "{{ secret('SHARED_TOKEN', namespace='shared.secrets') }}"
```

Open source: there is no dedicated store. Kestra reads base64-encoded environment variables with the `SECRET_` prefix and exposes them through `secret()`. This keeps values out of YAML but gives no encryption at rest, no audit trail and no access control beyond the host environment.

Enterprise Edition: a Secrets Manager backed by AWS Secrets Manager, Azure Key Vault, HashiCorp Vault or Kestra's own store. Secrets are available under Namespaces, then the namespace, then Secrets, or under Tenant, then Secrets; each has a key name, optional description and tags, and can be copied as a Pebble expression. Cross-namespace access is allowed by default; restrict it by configuring `allowedNamespaces` on the target namespace.

Secrets suit static sensitive values (API keys, passwords, webhook URLs, certificates, long-lived tokens). Where Kestra must mint or refresh short-lived tokens at runtime for server-to-server authentication, use Credentials instead; Credentials can reference secrets.

## Checked

2026-11-04. Confirmed against "Store and Access Sensitive Information Securely" (concepts/secret): secret() purpose, Enterprise backends and UI locations, cross-namespace reads and allowedNamespaces, OSS SECRET_ base64 environment variables and their limits, Credentials guidance. Removed: "Never emit secrets through task outputs" (not on the page) and the implication that cross-namespace reads apply to OSS (the page places them under Enterprise Edition).
Method: documentation only; no commands were run.
