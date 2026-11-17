---
id: computing-software.ai-ml-engineering.seldon-core-2.tls-control-plane-and-envoy-data-plane
name: tls-control-plane-and-envoy-data-plane
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, security, tls, mtls, cert-manager, control-plane-security-protocol, envoy-security-protocol, helm-security-values, seldon-core-v2-certs, xds, sds]
level: advanced
status: docs-checked
description: "Enable TLS for the Seldon Core 2 control plane and Envoy data plane: security protocol env vars, Helm security values, secret names and cert-manager certs."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/README.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/reference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS for the control plane and Envoy data plane

Three areas can be secured: control plane, Kafka and data plane. Kafka is covered by the Kafka skills.

## Control plane
`CONTROL_PLANE_SECURITY_PROTOCOL` is `PLAINTEXT` or `SSL`. When SSL, certificates are loaded for the gRPC services, and the secrets or folders are watched and reloaded on renewal. With Helm:
```bash
helm install seldon-v2 k8s/helm-charts/seldon-core-v2-setup/ -n seldon-mesh --set security.controlplane.protocol=SSL
```
Server side is the scheduler; clients are the agent, modelgateway, hodometer and CRD controller. Env vars include `CONTROL_PLANE_SERVER_TLS_SECRET_NAME`, `CONTROL_PLANE_CLIENT_TLS_SECRET_NAME` and the `..._KEY_LOCATION`, `..._CRT_LOCATION`, `..._CA_LOCATION` variants.

## Data plane
`ENVOY_SECURITY_PROTOCOL` is `PLAINTEXT` or `SSL`. With SSL, Envoy talks to the xDS server over TLS and certificates are sent to Envoy through SDS for upstream and downstream traffic. Downstream is external access to Seldon; upstream is from Envoy to model servers or the pipeline gateway.
```bash
helm install seldon-v2 k8s/helm-charts/seldon-core-v2-setup/ -n seldon-mesh --set security.envoy.protocol=SSL
```
Default secret names: `seldon-controlplane-server` and `-client`, `seldon-upstream-server` and `-client`, `seldon-downstream-server`. Override them under `security.envoy.ssl.upstream` and `.downstream`, which each have a `server` block (`secret`, `clientValidationSecret`) and a `client` block (`secret`, `serverValidationSecret`); downstream `clientValidationSecret` and client `secret` are empty by default. The sample gives mTLS for internal upstream traffic and plain SSL (non-mTLS) for the downstream entrypoint. The Envoy env vars follow the `ENVOY_DOWNSTREAM_*` and `ENVOY_UPSTREAM_*` patterns.

## Seldon CLI against TLS
Use a custom config with `dataplane.tls: true` and `dataplane.skipSSLVerify: true`. Skipping verification suits internal self-signed certificates; in production use the DNS name you expose.

## Certificates
The installer must supply certificates. Seldon ships example cert-manager issuers and certificates:
```sh
helm install seldon-v2-certs k8s/helm-charts/seldon-core-v2-certs/ -n seldon-mesh
```

## Checked

2026-11-09: protocol env vars, Helm flags, default secret names, scheduler/client roles, env var names, CLI config and the certs chart confirmed. Made the secret override description match the documented values layout.

Method: docs-checked 2026-11-09 against the Seldon docs-gb security README.md and reference.md
