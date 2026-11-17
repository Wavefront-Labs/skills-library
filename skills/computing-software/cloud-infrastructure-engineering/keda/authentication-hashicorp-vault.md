---
id: computing-software.cloud-infrastructure-engineering.keda.authentication-hashicorp-vault
name: authentication-hashicorp-vault
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [hashicorp-vault, hashicorpvault, vault-kubernetes-auth, vault-token, secrets-mapping]
level: advanced
status: docs-checked
description: "Fetch scaler secrets from HashiCorp Vault with token or kubernetes authentication in a TriggerAuthentication, including namespace and service account token defaults."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You define authentication metadata such as the Vault address and the authentication method, and a secrets list maps the path and key of each Vault secret to a trigger parameter. Values pulled this way are merged with any other sources into the authentication data for the scaler.
The `hashiCorpVault` provider pulls secrets from Vault straight into trigger parameters.

```yaml
hashiCorpVault:
  address: {hashicorp-vault-address}
  namespace: {hashicorp-vault-namespace}
  authentication: token | kubernetes
  role: {hashicorp-vault-role}
  mount: {hashicorp-vault-mount}
  credential:
    token: {hashicorp-vault-token}
    serviceAccount: {path-to-service-account-file}
  secrets:
  - parameter: {scaledObject-parameter-name}
    key: {hashicorp-vault-secret-key-name}
    path: {hashicorp-vault-secret-path}
```

Required: `address`, `authentication` and the `secrets` list. Everything else is optional.

- `authentication: token` takes the Vault token from `credential.token`.
- `authentication: kubernetes`: the page says to provide `role` and `mount` as well (the example marks them optional), and `credential.serviceAccount` is the path to the service account token file. The default is `/var/run/secrets/kubernetes.io/serviceaccount/token`.
- `namespace` targets a Vault Enterprise namespace; the default is the root namespace.
- Each `secrets` entry maps the secret `path` and `key` inside Vault to a trigger `parameter`.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: hashiCorpVault fields, token and kubernetes methods, default token path. Removed: the claim that Vault can supply only sensitive parameters, and a gloss on the token path.

Method: documentation only; no commands were run.
