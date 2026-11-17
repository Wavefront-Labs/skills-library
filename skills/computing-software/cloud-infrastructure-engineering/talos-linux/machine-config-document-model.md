---
id: computing-software.cloud-infrastructure-engineering.talos-linux.machine-config-document-model
name: machine-config-document-model
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [machine-config, multi-document, v1alpha1, document-kinds, yaml, configuration-reference]
level: intro
status: docs-checked
description: "Talos machine configuration structure: multi-document YAML, the mandatory v1alpha1 main document, named versus unnamed documents, and YAML quoting pitfalls."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/reference/configuration/overview.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/reference/configuration/v1alpha1/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A machine is configured by one YAML file holding several documents separated by `---`. Each is validated separately, merged into one effective configuration, and later documents win. The `v1alpha1` document is the only mandatory one and carries settings not yet split out (machine type, cluster secrets, `etcd`). Dedicated documents now cover networking, Kubernetes, kernel and installation; the equivalent `v1alpha1` fields are deprecated but supported, and the configuration document map says which document replaces which field.

Every other document uses:

```yaml
apiVersion: v1alpha1 # version of the document
kind: NetworkRuleConfig # type of document
name: rule1 # only for named documents
```

Unnamed documents may appear once; named ones may repeat with unique names. Quote values containing `!`, `?`, `*` or `&` (for example `diskSelector` filters).

Main document skeleton:

```yaml
version: v1alpha1
machine: # ...
cluster: # ...
```

`machine.type` is `controlplane` or `worker` (`join` is the deprecated old name for worker). Other machine fields: `token`, `ca`, `acceptedCAs`, `certSANs`, `features.diskQuotaSupport`, `logging.destinations` (for example `endpoint: tcp://1.2.3.4:12345`, `format: json_lines`, `extraTags`) and `seccompProfiles`. Cluster fields include `token`, `etcd` (`image`, `ca`, `extraArgs` such as `election-timeout: "5000"`, `advertisedSubnets`, `listenSubnets` with `!` negation), `externalCloudProvider` and `adminKubeconfig.certLifetime` (default 1 year). `debug: true` sends all system container logs to the serial console.

## Checked

2026-11-04. Overview and v1alpha1 reference pages confirm the multi-document rules, common document schema and the field names listed.

Method: documentation only; no commands were run.
