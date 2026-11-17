---
id: computing-software.systems-network-administration.pki-tls-administration.cert-manager-issuers
name: cert-manager-issuers
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cert-manager-issuers, pki-cert-manager, cert-manager, clusterissuer, kubernetes, acme-issuer, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Configure cert-manager Issuers for ACME, CA, Vault and self-signed, request Certificate resources, and set renewal timing and key rotation."
sources:
  - https://cert-manager.io/docs/configuration/
  - https://cert-manager.io/docs/configuration/acme/
  - https://cert-manager.io/docs/configuration/ca/
  - https://cert-manager.io/docs/configuration/selfsigned/
  - https://cert-manager.io/docs/configuration/vault/
  - https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/
  - https://cert-manager.io/docs/usage/certificate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cert-manager Issuers and ClusterIssuers
Goal: Kubernetes-native certificate issuance and renewal.

## Issuer types
- ACME: one account registered with an ACME server. Needs `email`, `server` URL, `privateKeySecretRef` (the account key Secret) and one or more `solvers`. Challenges are HTTP01 (cert-manager routes the ingress to a small web server presenting the key) or DNS01 (a TXT record, created automatically with the right provider permissions). Losing the account key Secret means a new account can be created, but certificates from the old account cannot be revoked.
- CA: certificate and key stored in a Secret (`tls.crt`, `tls.key`) in the Issuer's namespace, or the cluster resource namespace (default `cert-manager`, flag `--cluster-resource-namespace`) for a ClusterIssuer. The docs warn CA issuers are for demos or advanced users who can handle rotation, trust distribution and disaster recovery. For an intermediate, `tls.crt` must hold the full chain in order issuer, intermediate(s), root (root optional). Optional `crlDistributionPoints` and OCSP server lists are written into issued certificates.
- SelfSigned: `spec: {selfSigned: {}}`; useful to bootstrap a root for a CA issuer or for quick test certificates.
- Vault: `server`, `path` (must use the `sign` endpoint, for example `pki_int/sign/example-dot-com`), optional base64 `caBundle` (typically needed for https), and an `auth` block.

## Example (ACME ClusterIssuer with Cloudflare DNS01, plus a Certificate)
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: {name: letsencrypt-staging}
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: ops@example.com
    privateKeySecretRef: {name: example-issuer-account-key}
    solvers:
    - dns01:
        cloudflare:
          apiTokenSecretRef: {name: cloudflare-api-token-secret, key: api-token}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: {name: example-com, namespace: sandbox}
spec:
  secretName: example-com-tls
  dnsNames: [example.com]
  issuerRef: {name: letsencrypt-staging, kind: ClusterIssuer}
  privateKey: {rotationPolicy: Always}
```
Swap in your CA's directory URL for production. Cloudflare: API tokens are recommended over global API keys; permissions `Zone - DNS - Edit` and `Zone - Zone - Read`.

## Certificate behaviour
- `issuerRef.kind` defaults to Issuer; set `ClusterIssuer` to use a cluster-wide issuer.
- Result is stored in the named Secret: `tls.crt` is the certificate followed by its chain (roots are intentionally omitted); `ca.crt` appears only when the CA is known (not with ACME). Do not mount `ca.crt` directly into a trust store, since it changes on renewal.
- Default `duration` is 90 days (issuers may override). Minimum duration is 1 hour; it must exceed `renewBefore`. Default renewal is two thirds through the lifetime; `renewBefore` or `renewBeforePercentage` override it. The percentage form is recommended to avoid renewal loops, for example when an issuer backdates `notBefore` (Let's Encrypt, one hour). Durations use Go format (`2160h`), not `90d`.
- `spec.renewal.windows` (cron plus `windowDuration`, optional `timezone`) restricts when renewal may run; `policy: Disabled` turns automatic renewal off. If no window opens before expiry, cert-manager renews at the calculated time anyway.
- Reissue triggers: changes to `commonName`, `dnsNames`, `ipAddresses`, `uris`, `emailAddresses`, `subject`, `isCA`, `usages`, `duration` or `issuerRef`, or `cmctl renew <name>`. Deleting the Secret is not the recommended way to rotate the key.
- Deleting a Certificate leaves its Secret in place (no more renewals) unless the controller runs with `--enable-certificate-owner-ref`.

## Gotchas
- `rotationPolicy` default depends on version: `Never` before v1.18.0 (key reused on renewal), `Always` from v1.18.0. Set it explicitly to `Always` (recommended by the docs) so behaviour does not depend on the version.
- Apps that load the cert once at start need a restart or a reloader after renewal.
- Built-in CA and SelfSigned issuers do not check SANs against name constraints; a certificate can issue and then fail client validation.
- Keep issuer and Certificate manifests in version control (without keys) and review changes like code.

## Verify
- [ ] `kubectl get issuers ca-issuer -n sandbox -o wide` (or `clusterissuers`) shows READY True.
- [ ] The target Secret holds `tls.crt` and `tls.key`.
- [ ] `rotationPolicy` is set explicitly on production Certificates.

## Checked
Method: docs-checked 2026-11-09 against the cert-manager configuration index, ACME, CA, SelfSigned and Vault issuer pages, the Cloudflare DNS01 page and the Certificate resource page.
Removed as unconfirmed: the production Let's Encrypt URL (docs examples use staging), the claim that renewBefore defaults to 30 days (docs say two thirds of lifetime), the claim that rotationPolicy defaults to Never (version dependent), and the `describe certificate` to `certificaterequest`, `order`, `challenge` debugging chain (troubleshooting page not read).
