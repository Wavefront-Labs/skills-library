---
id: computing-software.cloud-infrastructure-engineering.cert-manager.troubleshooting-webhook
name: troubleshooting-webhook
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [troubleshooting, webhook, connection-refused, i-o-timeout, secureport, hostnetwork, timeoutseconds]
level: practitioner
status: docs-checked
description: "Diagnose cert-manager webhook errors by message: connection refused, i/o timeout, x509 failures, context deadline exceeded, and platform-specific port fixes."
sources:
  - https://cert-manager.io/docs/troubleshooting/webhook/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `connect: connection refused`: nothing listens. `kubectl get endpoints -n cert-manager cert-manager-webhook` showing `<none>` means the readiness probe fails; compare the probe port with `--healthz-port` (one case: 6081 vs 6080). Test: port-forward `deploy/cert-manager-webhook 6080`, `curl -sS --dump-header - 127.0.0.1:6080/healthz` should return 200.
- `i/o timeout`: connectivity. GKE private cluster: `containerPort` must be 10250 or 443 (`webhook.securePort`), or add a firewall rule. EKS with custom CNI (Weave, Calico): `--set webhook.hostNetwork=true --set webhook.securePort=10260`; with the default `securePort` (10250), also allow TCP 10250 from the control plane to workers in security groups and network policies.
- `x509: certificate is valid for ...internal, not cert-manager-webhook...` on EKS Fargate: port 10250 collides with the kubelet; install with `--set webhook.securePort=10260`.
- `x509: certificate has expired or is not yet valid`: suspend or VM live migration on cert-manager 1.20 or earlier; upgrade to 1.21 or restart the webhook pod.
- `x509: certificate signed by unknown authority`: with cert-manager 0.14 or older via Helm in a namespace other than `cert-manager`, the CRD annotation hardcodes the namespace (fixed in 0.15); on 1.6 or earlier check cainjector logs and compare `caBundle` with the CA in Secret `cert-manager-webhook-ca`.
- `context deadline exceeded`: default `timeoutSeconds` is 10; patch the mutating and validating `cert-manager-webhook` configurations to 30 via `kubectl patch ... --type=json` replacing `/webhooks/0/timeoutSeconds`. `i/o timeout` is network; `TLS handshake timeout` points at the webhook.
- `no endpoints available for service "cert-manager-webhook"` on OVHCloud: etcd quota exceeded; delete resources such as CertificateRequests.
- GKE Autopilot `kube-system` managed namespace: `--set global.leaderElection.namespace=cert-manager`.

## Checked

2026-11-03: Confirmed against the webhook troubleshooting page: connection refused with empty endpoints and the `--healthz-port` mismatch, port-forward `/healthz` test, GKE private cluster ports 10250 and 443, EKS custom CNI values (`webhook.hostNetwork=true`, `webhook.securePort=10260`), the EKS Fargate x509 case and `securePort=10260`, the expired-certificate case (1.20 or earlier, fixed in 1.21, restart workaround), the default `timeoutSeconds` of 10 and the `kubectl patch` to 30, the OVHcloud etcd quota case, and the GKE Autopilot `global.leaderElection.namespace=cert-manager` fix. Fixed: the chart/version wording for the unknown-authority case (page says cert-manager 0.14 and below, fixed in 0.15) and removed the `ca.crt` key name (the page compares `caBundle` with the CA in `cert-manager-webhook-ca` without naming a key). Qualified the TCP 10250 firewall advice as applying to the default securePort.

Method: documentation only; no commands were run.
