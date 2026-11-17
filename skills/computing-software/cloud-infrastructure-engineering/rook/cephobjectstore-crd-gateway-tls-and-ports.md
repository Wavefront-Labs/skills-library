---
id: computing-software.cloud-infrastructure-engineering.rook.cephobjectstore-crd-gateway-tls-and-ports
name: cephobjectstore-crd-gateway-tls-and-ports
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [gateway, sslcertificateref, cabundleref, secureport, instances, externalrgwendpoints, additionalvolumemounts]
level: advanced
status: docs-checked
description: "Configure CephObjectStore gateway ports, TLS certificate secrets, CA bundles, instance count, external RGW endpoints and extra volume mounts."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Object-Storage/ceph-object-store-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.gateway` corresponds to the RGW daemon settings.

Ports and scale:
- `port`: where the service is reachable. With host networking the daemons also listen on it; on the SDN the daemon listens internally on 8080.
- `securePort`: needs a TLS certificate via `sslCertificateRef` or service annotations.
- `instances`: number of pods load-balancing the store.
- `hostNetwork`: if unset, the cluster CR network settings apply.

TLS:
- `sslCertificateRef`: name of an opaque or tls Secret with the certificate. For an opaque Secret Rook reads the `cert` key. An internal-CA chain can be appended leaf first, then intermediates, then root: the beast frontend uses only the first cert, while the operator uses the entire chain to manage RGW.
- If the certificate DNS lacks the in-cluster service name, add `insecureSkipVerify: true` to the secret data. This is not recommended, as TLS is then open to machine-in-the-middle attacks.
- `caBundleRef`: an opaque Secret in the cluster namespace (key `cabundle`) with extra CAs that RGW uses to verify external services such as LDAP servers or another multisite realm. The operator does not use it.

Other fields: `externalRgwEndpoints` (external mode only; give a single load-balancer endpoint for stable OBCs), `annotations`, `labels`, `placement`, `resources`, `priorityClassName`, and `additionalVolumeMounts` (mounted under `/var/rgw` with a `subPath`).

## Checked

2026-11-03. Confirmed against the CephObjectStore CRD page: port and the internal 8080 on SDN, securePort, instances, hostNetwork, sslCertificateRef with the cert key and chain order, insecureSkipVerify, caBundleRef with the cabundle key, externalRgwEndpoints and additionalVolumeMounts under /var/rgw. Removed: nothing.

Method: documentation only; no commands were run.
