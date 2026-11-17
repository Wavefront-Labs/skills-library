---
id: computing-software.systems-network-administration.pki-tls-administration.service-mesh-workload-identity
name: service-mesh-workload-identity
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [service-mesh-workload-identity, pki-kubernetes, istio, spiffe, workload-identity, cert-rotation, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Plug an intermediate CA into Istio, understand SPIFFE IDs and SVIDs, and verify workload certificates chain to your root."
sources:
  - https://istio.io/latest/docs/tasks/security/cert-management/plugin-ca-cert/
  - https://istio.io/latest/docs/concepts/security/
  - https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service mesh and SPIFFE workload certificates
Goal: mTLS between workloads with automatically rotated short-lived certificates and a root you control.

## Istio plug-in CA
- By default the Istio CA generates a self-signed root and key and signs workload certificates with them. Istio's guidance: keep the root CA on a secure offline machine and issue an intermediate to the Istio CA in each cluster. Its task page is a demo; for production it recommends a production-ready CA such as HashiCorp Vault.
- Create a secret named `cacerts` in `istio-system` holding `ca-cert.pem` (intermediate), `ca-key.pem`, `root-cert.pem` and `cert-chain.pem`:
```
kubectl create secret generic cacerts -n istio-system \
  --from-file=ca-cert.pem --from-file=ca-key.pem \
  --from-file=root-cert.pem --from-file=cert-chain.pem
```
  Create it before installing Istio; istiod reads the certificates and key from the secret mount.
- Provisioning flow: the Istio agent beside each Envoy proxy creates a private key and CSR and sends it with its credentials to istiod, whose CA validates and signs it; Envoy gets the key and certificate through the SDS API; the agent watches expiry and repeats the process for rotation.
- A PeerAuthentication with `mtls: mode: STRICT` makes a namespace accept only mutual TLS traffic.

## SPIFFE concepts
- A SPIFFE ID is a URI of the form `spiffe://<trust domain>/<workload identifier>`. The trust domain corresponds to a trust root; SPIFFE advises separate trust domains for different locations or for environments with different security practices (for example staging versus production).
- An SVID proves a workload's identity and comes as an X.509 certificate or a JWT. SPIFFE advises X.509-SVIDs where possible because JWTs can be replayed; JWTs may be the only option when an L7 proxy or load balancer sits between workloads.
- The Workload API hands a workload its ID, a key, a short-lived certificate and a trust bundle (CA roots for verifying other workloads). Keys and certificates are short-lived and rotated automatically; trust bundle contents are rotated frequently.

## Verify
- [ ] Inspect the chain a sidecar serves: `kubectl exec <curl pod> -c istio-proxy -n foo -- openssl s_client -showcerts -connect httpbin.foo:8000`, split into files, then `openssl verify -CAfile <(cat ca-cert.pem root-cert.pem) workload-cert.pem` returns OK. With a self-signed demo root, `verify error:num=19:self signed certificate in certificate chain` is expected from s_client.
- [ ] The root and intermediate in the served chain are byte-identical to the files you plugged in.

## Gotchas
- Wait about 20 seconds after applying the STRICT policy before capturing the chain (Istio's own task does).
- Removing the demo material: delete the `cacerts` secret and local key files after the exercise.

## Checked
Method: docs-checked 2026-11-09 against the Istio "Plug in CA Certificates" task, the Istio security concepts page and the SPIFFE concepts page.
Removed as unconfirmed: the 24-hour default workload certificate lifetime and the `SECRET_TTL`/`workloadCertTtl` settings, `spiffe://cluster.local/ns/<ns>/sa/<sa>` as a stated default (the Istio principal format `cluster.local/ns/default/sa/curl` appears only in authorization examples), SPIRE specifics (1 hour SVID TTL, upstream authority plugins), cert-manager `istio-csr`, root rotation sequence, federation by exchanging bundles, and the `istioctl proxy-config secret` and `istioctl x describe` checks. The `spire` tag was removed accordingly.
