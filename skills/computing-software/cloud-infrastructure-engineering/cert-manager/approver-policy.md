---
id: computing-software.cloud-infrastructure-engineering.cert-manager.approver-policy
name: approver-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [approver-policy, certificaterequestpolicy, cel, rbac-use, constraints, selector]
level: advanced
status: docs-checked
description: "Write approver-policy CertificateRequestPolicy resources: allowed, constraints, selector and plugins, the RBAC use binding, and approve/deny semantics."
sources:
  - https://cert-manager.io/docs/policy/approval/approver-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `CertificateRequestPolicy` (group `policy.cert-manager.io`) has these blocks:

- `allowed`: attributes a request may contain; omitted attributes are denied. Set `required: true` to make one mandatory (not for `isCA` or `usages`). Fields: `commonName`, `dnsNames`, `ipAddresses`, `uris`, `emailAddresses`, `isCA`, `usages`, `subject` (`organizations`, `countries`, `organizationalUnits`, `localities`, `provinces`, `streetAddresses`, `postalCodes`, `serialNumber`). Strings accept `*`; list fields permit any subset.
- `allowed` CEL validations (0.11.0+): `rule` and `message`; request value is `self`, request metadata is `cr` (`username`, `groups`, `namespace`, `name`).
- `constraints`: `minDuration`, `maxDuration`, `privateKey` (`algorithm`, `minSize`, `maxSize`). Omitted means anything.
- `selector` (required): `issuerRef` (`name`, `kind`, `group`, wildcards), `namespace` (`matchNames`, `matchLabels`), or both (both must match). `{}` matches everything.
- `plugins`: named blocks with `values` for compiled-in plugins.

RBAC: a policy applies only if the requester is bound to it. Grant a ClusterRole verb `use` on `certificaterequestpolicies` in `policy.cert-manager.io` with `resourceNames`, then a ClusterRoleBinding. For Certificate resources, bind the cert-manager controller ServiceAccount because it creates the requests.

Evaluation: any matching policy that permits approves; matching policies that all refuse deny, permanently failing the request (Certificate issuance retries with backoff); no matching policy leaves the request unprocessed.

## Checked

2026-11-03: Confirmed against the approver-policy page: the four parts (allowed, constraints, selector, plugins), omitted-means-deny rules, `required` limits, wildcards and subset list semantics, the allowed field list, CEL validations from 0.11.0 with `self` and `cr` (`username`, `groups`, `namespace`, `name`), constraints fields, selector rules (issuerRef and namespace, `{}` matches all, both must match), the `use` verb RBAC binding including the cert-manager controller ServiceAccount note, and approve/deny/unprocessed semantics. Removed: the sentence about disabling the default approver (not on this page).

Method: documentation only; no commands were run.
