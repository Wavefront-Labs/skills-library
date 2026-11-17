---
id: computing-software.cloud-infrastructure-engineering.cert-manager.cyberark-issuer
name: cyberark-issuer
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [venafi, cyberark, tpp, zone, vcert, custom-fields, ngts]
level: advanced
status: docs-checked
description: "Configure the cert-manager CyberArk (Venafi) issuer for SaaS, self-hosted TPP and NGTS: zones, credentials Secrets, policy caveats and custom fields."
sources:
  - https://cert-manager.io/docs/configuration/venafi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The issuer lives under `spec.venafi`.

SaaS (`cloud`): Secret key `apikey`, referenced by `cloud.apiTokenSecretRef` (`name`, `key`). `zone` is `<Application>\<Issuing Template alias>`.

Self-hosted (`tpp`): `tpp.url` is the instance `/vedsdk` endpoint; `zone` is a policy folder such as `\VED\Policy\...`. `tpp.caBundle` (base64 PEM, empty uses system roots) or `tpp.caBundleSecretRef`, not both. `tpp.credentialsRef.name` points at the auth Secret:
- Access token: key `access-token`, generated with `vcert getcred`, scope `certificate:manage,revoke`. Refresh tokens are unsupported, so use a long validity.
- Username/password: keys `username`, `password`, optional `client-id` (default `cert-manager.io`). Username format `<identity provider>:<username>`, e.g. `local:admin`.

Policy caveats: allow User Provided CSRs. Unlocked Service Generated CSRs silently override subject DN, key algorithm and size; locked ones fail with "400 PKCS#10 data will not be processed."

NGTS (`ngts`): `zone` is the template name only; `ngts.tsgID` is the Tenant Service Group ID; Secret keys `client-id`, `client-secret` (shown once). `tokenEndpoint` and `url` are optional. View Only roles are insufficient; built-in NGTS accounts cannot be used.

ClusterIssuer Secrets go in the cluster resource namespace (default `cert-manager`).

Custom fields: Certificate annotation `venafi.cert-manager.io/custom-fields` holds a JSON array of `name`/`value` objects (self-hosted); an Issuer-level annotation (since v1.20) is merged with it.

## Checked

2026-11-03. Confirmed on the cert-manager CyberArk issuer page (configuration/venafi): SaaS, self-hosted and NGTS fields, Secret keys, zone formats, CSR handling caveats, vcert getcred scope, refresh-token note, NGTS field table and custom-field annotations with their version gates. Nothing removed.
Method: documentation only; no commands were run.
