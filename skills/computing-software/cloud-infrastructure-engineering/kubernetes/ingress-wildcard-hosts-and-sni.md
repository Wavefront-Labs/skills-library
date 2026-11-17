---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-wildcard-hosts-and-sni
name: ingress-wildcard-hosts-and-sni
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress, wildcard-host, sni, ingress-tls-cert-manager, tls]
level: practitioner
status: docs-checked
description: "Serve wildcard hosts and many TLS certificates from one ingress via SNI, wildcard certs with DNS-01, default certificates and multi-tenant collision rules."
sources: ["https://kubernetes.io/docs/concepts/services-networking/ingress/#hostname-wildcards", "https://kubernetes.github.io/ingress-nginx/user-guide/tls/", "https://cert-manager.io/docs/configuration/acme/dns01/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Wildcard hosts and SNI

## Wildcard rules
```yaml
spec:
  tls:
  - hosts: ["*.apps.example.com"]
    secretName: wildcard-apps-tls
  rules:
  - host: "*.apps.example.com"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend: {service: {name: router, port: {number: 80}}}
```
A wildcard host matches on a shared suffix and covers a single DNS label: `*.apps.example.com`
matches `a.apps.example.com`, not `a.b.apps.example.com` and not `apps.example.com`.

## Many certificates
With several `tls` entries for different hosts on one listener, the hosts are multiplexed using the
hostname in the SNI TLS extension (when the Ingress controller supports SNI). The TLS Secret must
contain keys named `tls.crt` and `tls.key`.
- For clients that send no SNI the controller serves its default certificate. For ingress-nginx the
  flag `--default-ssl-certificate=<namespace>/<name>` names the Secret used by the default
  HTTPS server.

## Wildcard certificates with cert-manager
cert-manager documents `DNS01` challenge solving for issuing wildcard certificates:
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: {name: wildcard-apps, namespace: ingress-nginx}
spec:
  secretName: wildcard-apps-tls
  dnsNames: ["*.apps.example.com", "apps.example.com"]
  issuerRef: {name: letsencrypt-dns, kind: ClusterIssuer}
```
The issuer (`letsencrypt-dns` here is your own ClusterIssuer with a DNS01 solver) must exist.
A Secret is namespaced, so a wildcard Secret must exist in each namespace whose Ingress
references it, or be configured as the controller's default certificate.

## Verify
Connect with a TLS client that sets the server name to `foo.apps.example.com` and inspect the
certificate subject and subjectAltName returned by the load balancer.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Ingress concept page (wildcard matching table, SNI multiplexing, TLS secret keys), the ingress-nginx CLI arguments reference (--default-ssl-certificate takes namespace/name) and the cert-manager ACME documentation (DNS01 for wildcard certificates). Removed claims about exact-host precedence over wildcards, ingress-nginx merge-by-age behaviour, secret replication tools and the openssl command.

Method: documentation only; no commands were run.
