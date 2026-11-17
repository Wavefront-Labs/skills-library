---
id: computing-software.cryptography-implementation.openssl.name-constrained-intermediate-cas
name: name-constrained-intermediate-cas
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, private-ca, openssl-ca, name-constraints, intermediate-ca, x509, permitted-subtree]
level: sme
status: docs-checked
description: "Issue name-constrained intermediate CAs: permitted and excluded DNS, IP and email subtrees, closing the IP-SAN loophole, and testing that violations fail verification."
sources: ["https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.10", "https://docs.openssl.org/3.0/man5/x509v3_config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name-constrained intermediate CAs

A name-constrained intermediate can only issue certificates inside the namespaces you list.
It turns "anyone with this CA key can impersonate any site" into "can impersonate hosts under
corp.example.com". Use it for team CAs, dev CAs, partner CAs and service-mesh issuers.

## Extension profile
```
[constrained_ca]
basicConstraints       = critical, CA:TRUE, pathlen:0
keyUsage               = critical, keyCertSign, cRLSign
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always
nameConstraints        = critical, @nc

[nc]
permitted;DNS.0   = corp.example.com
permitted;DNS.1   = svc.cluster.local
permitted;email.0 = corp.example.com
excluded;IP.0     = 0.0.0.0/0.0.0.0
excluded;IP.1     = 0:0:0:0:0:0:0:0/0:0:0:0:0:0:0:0
```
```
openssl x509 -req -in team-ca.csr -CA root.pem -CAkey root.key -days 1095 \
  -extfile nc.cnf -extensions constrained_ca -out team-ca.pem
```

## Semantics to get right (RFC 5280 4.2.1.10)
- A DNS constraint `corp.example.com` permits that name and any name made by adding labels on the left
  (`a.b.corp.example.com`), but not `evilcorp.example.com`.
- An email constraint `corp.example.com` covers addresses at that host only; a leading period
  (`.corp.example.com`) covers mailboxes in the domain but not on the host itself.
- Constraints only apply to name types they list. Permitting DNS alone leaves IP SANs, URIs and
  email addresses unconstrained, so either permit the IP ranges you need or exclude all IPs as
  above. Do the same for URI if you issue SPIFFE IDs (`permitted;URI.0 = spiffe.example.org`; URI
  constraints apply to the host part, and a URI whose host is an IP address or absent is rejected).
- IP constraints are address/mask pairs in the extension (`10.0.0.0/255.0.0.0`); OpenSSL's syntax is
  `IP:address/mask`.
- The extension must be present with a permitted or excluded list, and conforming CAs mark it critical.
- RFC 5280 does not apply name constraints to self-issued certificates unless it is the last in the path.
- Excluded wins over permitted.
- Constraints accumulate down the chain; a sub-CA cannot widen its parent's set.

## Client support
RFC 5280 says clients SHOULD process constraints on DNS, email, URI and IP names, and a client that sees a
critical constraint on a name form present in a certificate must process it or reject the certificate.
Support differs by stack; test each client you care about, and do not make name constraints the only control.

## Test violations (do this before handing the CA out)
```
# leaf for an outside name, signed by the constrained CA
openssl verify -CAfile root.pem -untrusted team-ca.pem outside.pem
# -> expect a permitted subtree violation
openssl verify -CAfile root.pem -untrusted team-ca.pem ip-san-leaf.pem
# -> expect an excluded subtree violation
```
Also test with your real client stack (curl, Go, Java), since verifiers differ in edge cases.

## Gotchas
- Publicly trusted sub-CAs fall under CA/B Forum rules (see its Baseline Requirements); write your own
  rules for a private PKI and keep them.
- Rename risk: if the team later needs `corp.example.net`, you must issue a new intermediate.
- Constraints do not limit EKU; add `extendedKeyUsage = serverAuth, clientAuth` on the
  intermediate to limit purposes as well.

## Verify
- [ ] `openssl x509 -noout -ext nameConstraints` shows the expected subtrees, marked critical.
- [ ] Outside-name and IP-SAN test leaves fail verification with subtree violation errors.

## Checked
2026-11-01. Confirmed against RFC 5280 section 4.2.1.10 (DNS, email, URI and IP matching, excluded precedence, critical marking, self-issued exception) and the OpenSSL 3.0 x509v3_config page (permitted;/excluded; syntax, IP address/mask form). Removed verify error numbers, the CN-fallback and per-vendor client support claims (not in the fetched pages).
Method: documentation only; no commands were run.
