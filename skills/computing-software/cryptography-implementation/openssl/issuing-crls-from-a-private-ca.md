---
id: computing-software.cryptography-implementation.openssl.issuing-crls-from-a-private-ca
name: issuing-crls-from-a-private-ca
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, private-ca, openssl-ca, crl-issuance, crl, revocation, crl-distribution-point]
level: advanced
status: verified
description: "Issue and publish CRLs from an openssl ca private CA: revoke with reasons, gencrl schedules, crlNumber, DER publishing at the CDP URL, and verifying with -crl_check."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ca/", "https://docs.openssl.org/3.0/man1/openssl-crl/", "https://www.rfc-editor.org/rfc/rfc5280#section-5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Issuing CRLs from a private CA

A CDP URL in your certificates is a promise. If the CRL behind it expires, clients that
check revocation can fail closed.

## Revoke
```
openssl ca -config ca.cnf -revoke ca/newcerts/4A3F....pem -crl_reason keyCompromise
# reasons: unspecified keyCompromise CACompromise affiliationChanged superseded
#          cessationOfOperation certificateHold removeFromCRL
```
That only updates `index.txt` (status `R`). Nothing changes for clients until you issue a CRL.
Prefer `superseded` for renewals and `keyCompromise` when the key leaked; avoid
`certificateHold` unless you will use `removeFromCRL`, which the manual says is not particularly useful outside delta
CRLs.

## Generate
```
[CA_default]
crlnumber        = $dir/crlnumber
default_crl_days = 7
crl_extensions   = crl_ext
[crl_ext]
authorityKeyIdentifier = keyid:always
```
```
openssl ca -config ca.cnf -gencrl -out ca/crl/issuing.crl.pem      # or -crldays / -crlhours
openssl crl -in ca/crl/issuing.crl.pem -outform DER -out issuing.crl
openssl crl -in ca/crl/issuing.crl.pem -noout -text | head -20     # lastUpdate, nextUpdate, CRL Number
```
`crlnumber` holds the next CRL number **in hex**; the CRL Number extension is only written if the file exists
(tested: `echo 1000 > crlnumber` produced `CRL Number: 4096`). With the config line `crlnumber = ...` but no file,
`openssl ca -gencrl` fails (`No such file or directory`). The extension lets clients detect older CRLs.

## Schedule and publish
- Regenerate well before `nextUpdate`: e.g. 7-day CRLs re-issued daily, so one missed run is harmless.
- Publish the DER file at exactly the CDP URL over **plain HTTP** with
  `Content-Type: application/pkix-crl`. HTTPS CDPs can loop (validating the CRL server's cert
  needs the CRL).
- Offline root: issue a long-lived root CRL (e.g. 6-12 months) during a scheduled ceremony;
  calendar the renewal.
- Monitor the published file: fetch, parse, alert if `nextUpdate` is under 48 hours away.

## Verify revocation works
```
openssl verify -crl_check -CAfile root+issuing.pem -CRLfile issuing.crl.pem leaf.pem
openssl verify -crl_check_all -CAfile root.pem -untrusted issuing.pem \
  -CRLfile root.crl.pem -CRLfile issuing.crl.pem leaf.pem
```
A revoked leaf returns `error 23 at 0 depth lookup: certificate revoked`. `-crl_check_all`
checks every level and fails with `error 3 at 1 depth lookup: unable to get certificate CRL` if the issuer's CRL is
missing (tested; supplying a root CRL as well gave `OK` for an unrevoked leaf).

## Gotchas
- Clients cache CRLs until `nextUpdate`; revocation takes effect only as fast as caches expire.
  Shorter CRL lifetimes or OCSP/short-lived certs give faster revocation.
- CRL size grows with every revocation until those certs expire; short certificate lifetimes
  keep it small.
- The CRL must be signed by the issuing CA key (or a delegated CRL signer with matching AKI). A CRL whose issuer does
  not match is simply not found (tested: error 3, `unable to get certificate CRL`).

## Verify
- [ ] A test certificate revoked today fails `openssl verify -crl_check` after the next CRL run.
- [ ] The published CRL's `nextUpdate` is monitored and never passes.
