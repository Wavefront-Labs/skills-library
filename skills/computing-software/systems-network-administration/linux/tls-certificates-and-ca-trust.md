---
id: computing-software.systems-network-administration.linux.tls-certificates-and-ca-trust
name: tls-certificates-and-ca-trust
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tls, ssl, certificates, ca-certificates, openssl, lets-encrypt, certbot, acme, update-ca-trust, update-ca-certificates, csr, san, private-ca, internal-ca, pem, pkcs12, chain, fullchain, expiry, renewal-hook, x509, step-ca, lpic-2, security, sysadmin, openssl-x509, self-signed, dns-01]
level: practitioner
status: docs-checked
description: "Manage TLS on Linux: inspect and convert certs with openssl, CSRs with SANs, a small internal CA, adding CAs to system trust, Let's Encrypt renewals with hooks, and chain/expiry diagnosis."
sources:
  - https://docs.openssl.org/master/man1/openssl-req/
  - https://docs.openssl.org/master/man1/openssl-s_client/
  - https://docs.openssl.org/master/man1/openssl-x509/
  - https://docs.openssl.org/master/man3/X509_STORE_CTX_get_error/
  - https://eff-certbot.readthedocs.io/en/stable/using.html
  - https://certbot-dns-cloudflare.readthedocs.io/en/stable/
  - https://letsencrypt.org/docs/rate-limits/
  - https://cabforum.org/working-groups/server/baseline-requirements/requirements/
  - https://manpages.debian.org/unstable/ca-certificates/update-ca-certificates.8.en.html
  - https://src.fedoraproject.org/rpms/ca-certificates/blob/rawhide/f/update-ca-trust.8.txt
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# TLS certificates and CA trust — issue, install, trust, renew, debug

**Goal:** every service presents a valid chain, every client trusts the right CAs (and
only those), renewals happen without humans, and expiry is caught before customers do.

## 1. Inspect anything
```bash
openssl x509 -in cert.pem -noout -subject -issuer -dates -ext subjectAltName
openssl x509 -in cert.pem -noout -fingerprint -sha256
openssl s_client -connect host:443 -servername host </dev/null 2>/dev/null | openssl x509 -noout -dates -subject
openssl s_client -connect host:443 -servername host -showcerts </dev/null   # certificates exactly as the server sent them (not a verified chain); the summary ends with the verify return code (0 = ok)
openssl s_client -connect smtp:587 -starttls smtp; openssl s_client -connect ldap:636
openssl verify -CAfile chain.pem cert.pem
openssl rsa -in key.pem -check -noout; openssl x509 -noout -modulus -in cert.pem | sha256sum; openssl rsa -noout -modulus -in key.pem | sha256sum   # RSA key matches cert?
openssl pkcs12 -in bundle.pfx -noenc -out bundle.pem; openssl pkcs12 -export -inkey key.pem -in cert.pem -certfile chain.pem -out bundle.pfx
openssl x509 -inform der -in cert.cer -out cert.pem         # DER ↔ PEM
```
Verify return code 21 ("unable to verify the first certificate") means no signature could be
verified because the chain holds a single, non-self-signed certificate: the server sent the leaf
without intermediates, so install `fullchain.pem`, not `cert.pem`. Code 20 ("unable to get local
issuer certificate") means the issuer of an untrusted certificate could not be found: a CA or intermediate missing from the client's trust store or the sent chain (OpenSSL X509_STORE_CTX_get_error documentation).

## 2. Keys, CSRs, self-signed
```bash
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out key.pem   # or -algorithm RSA -pkeyopt rsa_keygen_bits:3072
chmod 600 key.pem
openssl req -new -key key.pem -out req.csr -subj "/CN=app.example.com" \
   -addext "subjectAltName=DNS:app.example.com,DNS:www.app.example.com,IP:10.0.0.5"
openssl req -in req.csr -noout -text | grep -A1 'Alternative'
openssl req -x509 -newkey rsa:3072 -noenc -days 365 -keyout key.pem -out cert.pem -subj "/CN=dev.local" -addext "subjectAltName=DNS:dev.local"
```
Always include `subjectAltName` entries for every name the service answers to; clients match host names against SANs, not the CN. Under the CA/Browser Forum Baseline Requirements (section 6.3.2) the maximum validity of public subscriber certificates is 200 days from 15 March 2026, 100 days from 15 March 2027 and 47 days from 15 March 2029; plan for automation.

## 3. Internal CA (for lab/internal services) 
```bash
openssl req -x509 -new -newkey ec -pkeyopt ec_paramgen_curve:P-384 -noenc -days 3650 \
   -keyout ca.key -out ca.crt -subj "/CN=Example Internal CA" \
   -addext "basicConstraints=critical,CA:TRUE" -addext "keyUsage=critical,keyCertSign,cRLSign"
openssl x509 -req -in req.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 397 -out cert.pem \
   -copy_extensions copy -extfile <(printf "basicConstraints=CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth")
```
`-copy_extensions copy` (documented under `openssl x509 -req`; check your release supports it) copies the extensions, including the SANs, from the CSR into the certificate. For anything beyond a
handful of certs use a purpose-built CA service (for example step-ca or Vault PKI, see their documentation);
keep `ca.key` offline or in an HSM, and sign with an intermediate.

## 4. System trust store
```bash
# RHEL/Fedora
cp ca.crt /etc/pki/ca-trust/source/anchors/ && update-ca-trust
# Debian/Ubuntu (must end in .crt)
cp ca.crt /usr/local/share/ca-certificates/example-ca.crt && update-ca-certificates
ls /etc/ssl/certs | grep example             # Debian: a link for the new CA appears here
```
- Bundle paths: RHEL-family `/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem` (the legacy `/etc/pki/tls/certs/ca-bundle.crt` is replaced by it, per update-ca-trust(8)); Debian generates `ca-certificates.crt` under `/etc/ssl/certs`.
  Tools with their own stores ignore it: Java (its own `cacerts`, managed with `keytool`), Python `requests` (`REQUESTS_CA_BUNDLE`),
  Node (`NODE_EXTRA_CA_CERTS`), containers (mount the bundle or bake it in), NSS-based browsers (their own database, managed with `certutil`).
- Distrust a CA: RHEL-family put it in `/etc/pki/ca-trust/source/blocklist/` (the older name was `blacklist`); Debian prefix its line in `/etc/ca-certificates.conf` with `!` (lines starting with `!` are deselected), then run `update-ca-certificates`.
- Keep the `ca-certificates` package updated so root changes reach the machine.

## 5. Let's Encrypt / ACME automation
```bash
certbot certonly --webroot -w /var/www/html -d app.example.com -d www.app.example.com \
   --deploy-hook 'systemctl reload nginx'             # HTTP-01; needs port 80 reachable
certbot certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cf.ini -d '*.example.com' -d example.com   # DNS-01, wildcards
certbot certificates; certbot renew --dry-run
systemctl list-timers                                   # most installs preconfigure a scheduled task that runs `certbot renew` periodically
```
- Certbot saves certificates under `/etc/letsencrypt/live/<name>/` and updates them on renewal; point services at `fullchain.pem`
  + `privkey.pem` there (or symlink to them) instead of copying them.
- Non-root services (haproxy, postgres, dovecot) need the key readable: a `--deploy-hook`
  that `cat`s `fullchain.pem privkey.pem > /etc/haproxy/certs/app.pem; chmod 640; chown root:haproxy; systemctl reload haproxy`.
- Rate limits: up to 50 certificates per registered domain every 7 days (Let's Encrypt rate-limit page); test with `--staging`/`--dry-run`.
- Wildcard certificates need DNS-01 validation. Other ACME clients exist (for example acme.sh and lego); see their documentation.

## 6. Expiry monitoring
```bash
for h in app.example.com mail.example.com:587; do echo | openssl s_client -connect ${h%:*}:${h#*:} -servername ${h%:*} 2>/dev/null | openssl x509 -noout -enddate; done
```
Better: use your monitoring system's TLS certificate expiry probe for endpoints, and a file-based check for certificates on disk. Alert well before expiry (for example 14 days).

## Failure modes
- Private key permissions: `600 root` + service in a group with `640`; never world-readable.
- Mixed chain: cert from new CA, old intermediate still in the bundle → some clients fail
  intermittently. Rebuild `fullchain.pem` from what the CA gave you.
- Clock wrong → "certificate is not yet valid"; fix chrony before chasing the CA.
- Wildcards don't cover the apex or two levels (`*.example.com` ≠ `example.com`, ≠ `a.b.example.com`).

## Verify
- [ ] `openssl s_client … -servername` ends with verify return code 0 (ok) from a client that only has the system bundle.
- [ ] `certbot renew --dry-run` succeeds and the deploy hook reloads the service (check the service's log timestamp).
- [ ] An internal CA host: `curl https://internal.corp.example` works without `-k` after `update-ca-trust`.

## Checked
Checked 2026-10-27 against the OpenSSL documentation source (github.com/openssl/openssl doc/man1 and man3, master), the certbot and certbot-dns-cloudflare documentation, Let's Encrypt rate limits, CA/Browser Forum Baseline Requirements, the Debian update-ca-certificates(8) manual, the Fedora update-ca-trust(8) manual, the Node.js CLI documentation and the requests documentation.
- OpenSSL: `x509 -ext`, `-modulus`, `-req` with `-copy_extensions`, `req -addext`, `-newkey` with `-pkeyopt`, `s_client -starttls/-servername/-showcerts/-status`, `genpkey -pkeyopt ec_paramgen_curve`; `-nodes` is deprecated since 3.0 in favour of `-noenc` (changed in the examples); `-showcerts` is not a verified chain; error 21 and error 20 meanings.
- CA/B Forum Baseline Requirements: maximum subscriber certificate validity 200 days from 2026-03-15, 100 days from 2027-03-15, 47 days from 2029-03-15 (the earlier 398-day statement was out of date).
- update-ca-trust: `anchors/` and `blocklist/` (not `blacklist/`) under `/etc/pki/ca-trust/source/`, extracted bundle at `/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem`; Debian: `.crt` files in `/usr/local/share/ca-certificates`, `!` deselects a CA in `/etc/ca-certificates.conf`.
- certbot: `--deploy-hook`, webroot and HTTP-01 (port 80), DNS-01 for wildcards, `--dns-cloudflare-credentials`, `certbot renew --dry-run`, certificates under `/etc/letsencrypt/live`; Let's Encrypt allows 50 certificates per registered domain per 7 days.
- Node `NODE_EXTRA_CA_CERTS` and requests `REQUESTS_CA_BUNDLE` exist.
- Removed unconfirmed claims: certbot timer frequency and 30-day renewal point, DST Root CA X3 incident, step-ca ACME statement, `trust list`, Java/NSS command lines, SELinux label, blackbox metric name and named exporters.
Method: documentation only; no commands were run.
