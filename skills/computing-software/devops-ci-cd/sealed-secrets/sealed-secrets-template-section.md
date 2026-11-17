---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-template-section
name: sealed-secrets-template-section
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, template, sprig, secret-type, labels, annotations, immutable, sealedsecret]
level: practitioner
status: docs-checked
description: "Use spec.template in a SealedSecret to set labels, annotations, type and immutable on the generated Secret, with Sprig functions for templated values."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets template section

A SealedSecret resembles a Deployment relative to a Pod: its own metadata is not the metadata of the Secret it produces. The `spec.template` section holds everything you want the controller to put on the unsealed Secret.

```yaml
spec:
  encryptedData:
    .dockerconfigjson: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq.....
  template:
    type: kubernetes.io/dockerconfigjson
    immutable: true
    metadata:
      labels:
        "jenkins.io/credentials-type": usernamePassword
      annotations:
        "jenkins.io/credentials-description": credentials from Kubernetes
```

Rules from the README:
- The `metadata` block is copied as is. The `ownerReference` is added pointing at the SealedSecret unless owner references are disabled with an annotation.
- `type` and `immutable` are copied.
- The `data` field can template complex values; the Sprig function library is available (except `env`, `expandenv` and `getHostByName`) in addition to default Go text/template functions.
- All other Secret fields are currently ignored.

Because the Secret is a dependent object, updating or deleting the SealedSecret updates or deletes it. Annotations such as `kubectl.kubernetes.io/last-applied-configuration` on the SealedSecret itself are not copied to the Secret; use `template.metadata` for anything the Secret needs.

The repository has a config-template example for the case where one Secret value is a structured configuration file.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), section SealedSecrets as templates for secrets.
Confirmed: template section, YAML example, metadata copied, `type` and `immutable` copied, `data` templating, Sprig exclusions, other fields ignored, dependent object behaviour.
Removed: the 'embedded secret fields' wording.
Method: documentation only; no commands were run.
