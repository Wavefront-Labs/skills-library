---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-helmchart-values-from-secrets
name: k3s-helmchart-values-from-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, values-secrets, ignore-updates, basic-auth-repo]
level: advanced
status: docs-checked
description: "Feed confidential chart values from Secrets with spec.valuesSecrets and authenticate to private chart repos."
sources:
  - https://docs.k3s.io/add-ons/helm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use valuesSecrets instead of spec.set or spec.valuesContent when passing credentials into charts that cannot reference an existing Secret (the existingSecret pattern).

Rules:

- Secrets referenced by spec.valuesSecrets, spec.authSecret and spec.dockerRegistrySecret must be in the same namespace as the HelmChart.
- Each entry has name (required), keys (required list of keys read in the listed order) and ignoreUpdates (optional, default false).
- With ignoreUpdates false or unset, the Secret and all listed keys must exist, and any change to the Secret updates the chart.
- With ignoreUpdates true, the Secret is used if it exists when the chart is created or updated for other reasons, but later Secret changes do not trigger an update.

Example fragment:

```
valuesSecrets:
  - name: example-app-custom-values
    ignoreUpdates: false
    keys:
      - someValues
      - moreValues
```

Private chart repository: set spec.authSecret to a Secret of type kubernetes.io/basic-auth holding username and password, and spec.repoCAConfigMap to a ConfigMap holding the CA certificate (key ca.crt in the docs example). Set spec.authPassCredentials true to pass basic auth credentials to all domains. For an OCI chart registry use spec.dockerRegistrySecret (type kubernetes.io/dockerconfigjson).

## Checked

2026-11-08. Read the full K3s Helm page (docs/add-ons/helm.md in the k3s-io/docs repo). Confirmed: valuesSecrets purpose, same-namespace rule, name, keys and ignoreUpdates fields and semantics, the example fragment, authSecret with kubernetes.io/basic-auth, repoCAConfigMap with ca.crt, authPassCredentials, and dockerRegistrySecret with kubernetes.io/dockerconfigjson. Nothing removed.

Method: documentation only; no commands were run.
