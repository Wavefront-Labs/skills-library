---
id: computing-software.cloud-infrastructure-engineering.keda.operator-managed-and-custom-tls-certificates
name: operator-managed-and-custom-tls-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [kedaorg-certs, enable-cert-rotation, cert-dir, enable-webhook-patching, k8s-cluster-domain, tls-certificates]
level: sme
status: docs-checked
description: "Replace KEDA's self-signed operator-managed certificates with your own CA-issued ones using --enable-cert-rotation, the kedaorg-certs secret and --cert-dir."
sources:
  - https://keda.sh/docs/2.17/operate/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KEDA components talk to each other over TLS using self-signed certificates that the operator generates and rotates. They are stored in the Kubernetes secret `kedaorg-certs`, mounted into every KEDA component at `/certs`, with files `tls.crt`, `tls.key`, `ca.crt` and `ca.key`. The operator also patches Kubernetes resources with the `caBundle` so Kubernetes trusts the CA. Certificates are issued for `<KEDA_OPERATOR_SERVICE>`, `<KEDA_OPERATOR_SERVICE>.svc` and `<KEDA_OPERATOR_SERVICE>.svc.<CLUSTER_DOMAIN>` for the operator service, for example `keda-operator.svc.cluster.local`. Change the default `cluster.local` with the operator argument `--k8s-cluster-domain="my-domain"`; the Helm chart sets it from the `clusterDomain` value.

To use certificates from your own CA:
1. Disable generation by removing the `--enable-cert-rotation=true` argument or setting it to `false`.
2. Put your certificates into the `kedaorg-certs` secret, or patch the components (or Helm values) to mount a different secret.
3. Optionally point `--cert-dir` at another folder; all components inspect `/certs` by default.

Your CA must also be registered as trusted inside the KEDA components because these certificates secure internal communication.

The `--enable-webhook-patching` flag (default `true`) controls whether the operator patches webhook resources. Set it to `false` when you keep operator-managed certificates but disabled webhooks, to avoid errors about missing webhook resources.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Security page: kedaorg-certs, /certs, file names, DNS names, --k8s-cluster-domain, --enable-cert-rotation, --cert-dir, --enable-webhook-patching. Fixed placeholder names to match the page.

Method: documentation only; no commands were run.
