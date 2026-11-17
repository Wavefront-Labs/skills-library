---
id: computing-software.cryptography-implementation.protocol-implementation.cert-manager-issuers-and-certificates
name: cert-manager-issuers-and-certificates
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, cert-manager, kubernetes-pki, acme-issuer, clusterissuer, certificate-renewal, private-key-rotation, cert-manager-issuer]
level: practitioner
status: docs-checked
description: "Issue and renew Kubernetes certificates with cert-manager: Issuer vs ClusterIssuer, the Certificate spec, renewal timing, private key rotation and debugging ACME orders."
sources: ["https://cert-manager.io/docs/concepts/issuer/", "https://cert-manager.io/docs/usage/certificate/", "https://cert-manager.io/docs/troubleshooting/acme/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# cert-manager Issuers and Certificates

cert-manager turns a `Certificate` resource into a private key plus a `CertificateRequest`, obtains a signed
certificate from an `Issuer` or `ClusterIssuer`, stores both in the named Secret, and renews before expiry.

## Issuer scope
A `ClusterIssuer` can be referenced by Certificates in all namespaces: set `issuerRef.kind: ClusterIssuer`.

## Certificate
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: {name: api-tls, namespace: prod}
spec:
  secretName: api-tls
  dnsNames: ["api.example.com"]
  issuerRef: {name: my-issuer, kind: ClusterIssuer}
  duration: 2160h          # 90d
  renewBefore: 720h        # 30d
  privateKey:
    algorithm: ECDSA
    size: 256
    rotationPolicy: Always # new key on every reissue
```
- `duration` and `renewBefore` use Go duration strings (`h`, `m`, `s`); the `d` suffix is not allowed.
- Use `dnsNames`, not `commonName`.
- Without `renewBefore`/`renewBeforePercentage`, renewal is attempted 2/3 through the certificate lifetime; the
  planned time is in `status.renewalTime`.
- `rotationPolicy: Always` is the default from cert-manager v1.18.0; earlier versions default to `Never`.
  Some issuers disallow key re-use, so set `Always` explicitly there.
- Rotate a key by reissuing with `cmctl renew <certificate>`, not by deleting the Secret.

## Debugging ACME issuance
cert-manager creates an Order and Challenge resources per ACME request:
```
kubectl describe certificaterequest <name>
kubectl describe order <name>
kubectl get challenges
kubectl describe challenge <name>
```
Also check `kubectl get issuer` / `kubectl get clusterissuer` for a False Ready status and `describe` it.

## Verify
- [ ] Forced renewal (`cmctl renew`) rotates the key and the app picks it up.

## Checked

2026-11-01. Confirmed against the cert-manager Certificate usage page (fields, Go duration note, renewal default,
`status.renewalTime`, `rotationPolicy` default change at v1.18.0, `cmctl renew`) and the ACME troubleshooting page (Order,
Challenge, CertificateRequest, issuer status commands). Removed: ACME solver YAML (Route53, `dnsZones`), issuer-type
list, trust-manager, Ingress annotation, rate-limit and HTTP-01/wildcard gotchas, and the `Ready=True` item (not
in these pages).
Method: documentation only; no commands were run.
