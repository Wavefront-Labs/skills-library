---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-common-secret-types
name: external-secrets-operator-common-secret-types
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [secret-types, tls, dockerconfigjson, template]
level: intro
status: docs-checked
description: "Create typical Kubernetes Secret types such as dockerconfigjson, ssh-auth and TLS from ExternalSecrets using templates."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/common-k8s-secret-types.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build a dockerconfigjson pull secret from registry name, host and password using template data and the b64enc and lower functions.
Set the target template type and render the `.dockerconfigjson` key from separate provider values:

```yaml
spec:
  target:
    template:
      type: kubernetes.io/dockerconfigjson
      data:
        .dockerconfigjson: '{"auths":{"{{ .registryName | lower }}.{{ .registryHost }}":{"username":"{{ .registryName }}","password":"{{ .password }}","auth":"{{ printf "%s:%s" .registryName .password | b64enc }}"}}}'
  data:
  - secretKey: registryName
    remoteRef:
      key: secret/docker-registry-name
  - secretKey: registryHost
    remoteRef:
      key: secret/docker-registry-host
  - secretKey: password
    remoteRef:
      key: secret/docker-registry-password
```

If the whole docker config JSON is stored as one provider secret, template it straight into `.dockerconfigjson`. Helm interprets `{{ }}` itself, so inside a Helm chart escape the template delimiters (the docs link Helm issue 2798).

Verify with `kubectl get secret NAME -n NS -o jsonpath="{.data.\.dockerconfigjson}" | base64 -d`.

For ssh-auth, store the private key in the provider; the generated Secret holds it under `ssh-privatekey`.

For TLS, the documented route is to bundle an existing certificate and key into a pkcs12 file with `openssl pkcs12 -export -out certificate.p12 -inkey privkey.pem -in cert.pem`, store it in the provider and template the resulting Secret.

## Checked

2026-11-03. Claims were read against guides/common-k8s-secret-types.md in the external-secrets docs source. Removed: basic-auth (not on the page) from the description.

Method: documentation only; no commands were run.
