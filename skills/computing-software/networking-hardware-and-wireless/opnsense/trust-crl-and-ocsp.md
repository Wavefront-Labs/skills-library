---
id: computing-software.networking-hardware-and-wireless.opnsense.trust-crl-and-ocsp
name: trust-crl-and-ocsp
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [crl, ocsp, revocation, openssl-verify]
level: advanced
status: docs-checked
description: "Revoke certificates on OPNsense with CRLs and test them with openssl, plus how OCSP signing and the AuthorityInfoAccess extension work."
sources: ["https://docs.opnsense.org/manual/certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Certificate revocation: CRL and OCSP

CRL: in System > Trust > Revocation click [+] for your local CA to create a list, then edit it with the pencil icon to add or remove certificates. A download button exports it for external tools. CRLs scale poorly because every consumer downloads the whole list and lists are only regenerated at intervals, but for a local CA with a limited number of certificates that is rarely a concern.

To check by hand you need the CA chain (export cert from Authorities), the CRL (export crl from Revocation), a revoked certificate and a valid one. Concatenate chain and CRL (cat ca_chain.crt ca_crl.crl > my_chain.pem), then run openssl verify -crl_check -CAfile my_chain.pem revoked_cert.crt. A revoked certificate returns error 23, "certificate revoked"; a valid one prints OK.

OCSP checks status online and answers good, revoked or unknown; only good is valid. The CA certificate should carry the AuthorityInfoAccess extension (the OCSP uri parameter in OPNsense adds it); the info button reveals the uri. The responder needs a special signing certificate, created under System > Trust > Authorities, issued by the same CA. OPNsense does not implement a responder. For testing only, openssl ocsp can run one: openssl ocsp -index index.txt -port 8081 -rsigner ocsp_signer.crt -rkey ocsp_signer.key -CA ca.crt -ignore_err -text, with the index exported from Revocation. Query with openssl ocsp -url http://127.0.0.1:8081 -CAfile ca.crt -issuer ca.crt -serial N.

## Checked

2026-11-03. Confirmed against the OPNsense Trust manual page, section Revoke certificates: CRL creation, scaling note, the openssl verify and openssl ocsp commands with their flags, error 23, OCSP answers, AuthorityInfoAccess, signer certificate, no built-in responder. Nothing removed.

Method: documentation only; no commands were run.
