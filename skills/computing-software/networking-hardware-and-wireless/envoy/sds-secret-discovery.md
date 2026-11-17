---
id: computing-software.networking-hardware-and-wireless.envoy.sds-secret-discovery
name: sds-secret-discovery
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, sds, secret-discovery-service, tls-certificate-sds-secret-configs, spiffe, spire, certificate-rotation]
level: practitioner
status: docs-checked
description: "Deliver and rotate Envoy TLS certificates with SDS, including the warm-up rule for listeners and the secure SDS connection."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/security/secret.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sds secret discovery
Secrets can be static in bootstrap `static_resources.secrets`, or fetched by SDS. SDS's main benefit is simpler certificate management: without it, Kubernetes deployments must mount secrets as files and restart to rotate. With SDS, rotation needs no restart or connection drain.

```yaml
common_tls_context:
  tls_certificate_sds_secret_configs:
  - name: server_cert
    sds_config:
      resource_api_version: V3
      api_config_source:
        api_type: GRPC
        transport_api_version: V3
        grpc_services:
        - envoy_grpc: { cluster_name: sds_server_uds }
```
Rules from the docs:
- A listener whose certificate comes from SDS is not active, and its port stays closed, until the certificate has been fetched (a listener warm-up). Upstream clusters behave the same way for client certificates.
- A static cluster using SDS needs an SDS cluster defined (unless Google gRPC is used), and that SDS cluster itself must be static (no SDS inside it).
- The SDS connection must be secure: run the SDS server on the same host over a unix domain socket, or use mTLS (whose client certificate for the SDS link must be static) or AWS IAM SigV4.
- An SDS server implements `SecretDiscoveryService` and follows the xDS protocol; SPIRE can be the SDS server for SPIFFE identities.

Verify with `GET /certs` and `GET /listeners`.

## Checked

2026-11-03. Confirmed against: secret.rst (SDS behaviour, listener warming, secure connection rules) and tls.proto (tls_certificate_sds_secret_configs). Removed or corrected: the 'no obvious error' and warming stats claim.

Method: documentation only; no commands were run.
