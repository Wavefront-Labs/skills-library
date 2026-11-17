---
id: computing-software.cloud-infrastructure-engineering.cert-manager.csi-driver
name: csi-driver
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [csi-driver, volumeattributes, use-token-request, pod-certificates, pkcs12, csi-cert-manager-io]
level: advanced
status: docs-checked
description: "Mount per-pod cert-manager certificates with the CSI driver: volumeAttributes with defaults, variables, token-request mode and what it cannot do."
sources:
  - https://cert-manager.io/docs/usage/csi-driver/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Driver name `csi.cert-manager.io` under `csi.driver` in the pod volume (use `readOnly: true`). The driver generates the key locally per pod, requests a certificate, mounts it with no intermediate Secret, and destroys both when the app ends. The pod stays Pending until issuance completes.

`volumeAttributes` (prefix `csi.cert-manager.io/`):
- `issuer-name`, `issuer-kind` (default `Issuer`), `issuer-group` (default `cert-manager.io`)
- `key-algorithm` RSA (default), ECDSA, Ed25519; `key-size` RSA 2048-4096 (default 2048), ECDSA 256/384/521 (default 256); `key-encoding` PKCS1 or PKCS8
- `common-name`, `dns-names`, `uri-sans` (variables allowed), `ip-sans`, `is-ca` (default false), `key-usages`
- `duration` default `720h`; `renew-before` default one third of duration; `reuse-private-key` default false
- `certificate-file` (`tls.crt`), `ca-file` (`ca.crt`), `privatekey-file` (`tls.key`)
- `fs-group`: match the container's `runAsGroup`
- `pkcs12-enable`, `pkcs12-filename` (`keystore.p12`), `pkcs12-password` (required when enabled)

Variables in `common-name`, `dns-names`, `uri-sans`: `${POD_NAME}`, `${POD_NAMESPACE}`, `${POD_UID}`, `${SERVICE_ACCOUNT_NAME}`.

Token-request mode: `--use-token-request` on the DaemonSet makes the pod's ServiceAccount create the CertificateRequest, pairing with approver-policy. It needs RBAC `create` on `certificaterequests`; the sample binds `system:authenticated`, which the page warns is dangerous in production.

Limits: SelfSigned Issuers cannot be used; unsuitable for certificates that must survive node restarts or be shared. The page's attribute table has inconsistencies (`pkcs12-enable` naming), so verify against the API docs.

## Checked

2026-11-03: Confirmed against the csi-driver page: driver name `csi.cert-manager.io`, `readOnly: true`, local key generation, no intermediate Secret, Pending until issuance, every `volumeAttributes` default and range listed (issuer kind and group, key algorithm, key size, key encoding, duration `720h`, renew-before one third, reuse-private-key, file names, fs-group, PKCS12 attributes), the four variables for `common-name`, `dns-names`, `uri-sans`, `--use-token-request` with the RBAC warning, SelfSigned not usable, and the when-not-to-use list. Fixed: the field path was written `volume.csi.driver`; the page shows `csi.driver` inside the volume.

Method: documentation only; no commands were run.
