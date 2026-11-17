---
id: computing-software.cryptography-implementation.openssl.self-signed-certificates-for-development
name: self-signed-certificates-for-development
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, x509, csr, self-signed-certificate, dev-ca, localhost-tls, trust-store, mkcert]
level: practitioner
status: docs-checked
description: "Make development TLS certificates that browsers and tools accept: a local dev CA, localhost SANs, short validity, and adding trust per OS, runtime and browser."
sources: ["https://docs.openssl.org/3.0/man1/openssl-req/", "https://support.apple.com/en-us/103769", "https://github.com/FiloSottile/mkcert", "https://manpages.debian.org/stable/ca-certificates/update-ca-certificates.8.en.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-signed certificates for development

A bare self-signed leaf means every client needs an exception. A small **dev CA** you trust
once, issuing short-lived leaves, is less friction and teaches the same verification path
production uses.

## Quickest acceptable leaf (single host)
```
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc \
  -keyout dev.key -out dev.crt -days 30 -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:::1" \
  -addext "extendedKeyUsage=serverAuth" -addext "keyUsage=critical,digitalSignature"
```
Always include a subjectAltName extension. Keep validity short: Apple's certificate requirements
(support.apple.com 103769) say TLS server certificates need the `serverAuth` EKU and a validity
of 825 days or fewer.

## Better: a local dev CA
```
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc \
  -keyout devca.key -out devca.crt -days 825 -subj "/CN=Dev CA (my laptop)" \
  -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" \
  -addext "nameConstraints=critical,permitted;DNS:localhost,permitted;DNS:test,permitted;IP:127.0.0.0/255.0.0.0"
openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc \
  -keyout app.key -out app.csr -subj "/CN=app.test" -addext "subjectAltName=DNS:app.test,DNS:localhost" \
  -addext "extendedKeyUsage=serverAuth"
openssl x509 -req -in app.csr -CA devca.crt -CAkey devca.key -days 30 \
  -copy_extensions copy -out app.crt
```
The name constraint limits damage if the dev CA key leaks: it cannot mint a cert for your bank.
`mkcert` automates the same idea: `mkcert -install` puts its local CA into the system, Firefox (NSS) and Java (when `JAVA_HOME` is set) trust stores.

## Trust the CA where your tools look
| Consumer | Command / setting |
|---|---|
| Debian/Ubuntu | copy to `/usr/local/share/ca-certificates/devca.crt` then `sudo update-ca-certificates` |
| Node.js | `NODE_EXTRA_CA_CERTS=devca.crt` (Node does not use the system root store) |
| Other OSes, browsers, runtimes | use that platform's documented trust-store procedure, or `mkcert -install` |

## Rules
- Never set `verify=False`, `rejectUnauthorized: false` or `InsecureSkipVerify` to make dev work;
  that code reaches production.
- Never reuse a dev CA or dev key in shared or production environments; never commit `devca.key`.
- Use `.test` or `localhost` names, not real domains you don't control.
- Remove the dev CA from trust stores when the project ends.

## Verify
- [ ] `curl https://app.test:8443` works with no `-k`.
- [ ] `openssl verify -CAfile devca.crt app.crt` returns OK.
- [ ] The dev CA key is on one machine only and the CA is name-constrained.

## Checked

2026-10-31. Run locally with OpenSSL 3.2.3 (MSYS_NO_PATHCONV set so `-subj` is not rewritten): the single-host `openssl req -x509 ... -addext` leaf command and the dev-CA command both succeeded; the CSR with `subjectAltName` and `extendedKeyUsage=serverAuth` signed with `openssl x509 -req -copy_extensions copy` produced a leaf that `openssl verify -CAfile devca.crt` accepts, with SAN and `TLS Web Server Authentication` shown by `openssl x509 -ext`; the CA's name constraints printed as permitted DNS:localhost, DNS:test and IP 127.0.0.0/255.0.0.0; a second leaf for `www.example.com` signed by the same CA failed `openssl verify` with "permitted subtree violation". Without the EKU line in the CSR the leaf had no serverAuth EKU, so it was added. Confirmed against Apple support 103769 (serverAuth EKU, 825 days), the mkcert README (`-install` stores, `NODE_EXTRA_CA_CERTS`) and the Debian update-ca-certificates man page (`.crt` files in /usr/local/share/ca-certificates).
Removed: the Chrome/Go/Python CN claim, the macOS, Windows, RHEL, Firefox, Python and Java trust commands, the Docker row, the claim that mkcert adds no name constraints, and "(reserved)" for `.test` (none were on pages read).
Method: documentation, plus the local OpenSSL 3.2.3 runs listed above.
