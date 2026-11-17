---
id: computing-software.systems-network-administration.pki-tls-administration.chain-verify-errors
name: chain-verify-errors
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [chain-verify-errors, pki-openssl, chain-building, trust-anchor, verification, openssl-verify, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Diagnose chain and trust failures from how OpenSSL builds and validates paths: trust anchors, issuer matching, intermediates, -partial_chain, -untrusted."
sources:
  - https://docs.openssl.org/master/man1/openssl-verification-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixing chain and trust errors
Goal: find the missing or wrong certificate by following OpenSSL's documented chain building and validation.
How OpenSSL builds the chain:
- It starts at the target certificate and looks up an issuer for each certificate in turn, first in the trust store, then in the untrusted (intermediate) list. If an issuer is found in the trust store, the untrusted list is no longer consulted, so the store must hold either only the root or an uninterrupted chain to the root (unless `-partial_chain` is set).
- A candidate issuer must match the subject's issuer DN, agree with any authorityKeyIdentifier fields present, use a supported signature algorithm and, if it has keyUsage, allow `keyCertSign`. If several match, the first with a suitable validity period wins, else the one expiring last; there is no backtracking.
- Subject and authority key identifiers disambiguate issuers sharing a DN. SAN and IAN are not used for chain building.
- Chain construction stops at an apparently self-signed certificate (subject equals issuer, matching algorithms and key identifiers); it must then match a trust anchor exactly, or building fails.
How it validates: well-formedness (stricter with `-x509_strict`), extensions against the purpose (for TLS, `sslserver` or `sslclient` by default), trust settings on the anchor, then validity periods and signatures of every certificate, including the root's dates. `-attime` sets another reference time.
Useful options when testing: `-CAfile`/`-CApath`/`-CAstore` supply the trust store (OpenSSL has no default anchors of its own; distributions usually point it at a system store); `-untrusted FILE` supplies intermediates; `-trusted FILE` makes only those certificates anchors; `-partial_chain` accepts a chain ending at a non-self-signed certificate that is in the store; `-purpose`; `-verify_hostname`; `-verify_depth`; `-crl_check` and `-crl_check_all`.
Typical causes to check:
- Server sends the leaf only, so the intermediate is missing from the untrusted list: serve the full chain, ordered leaf then intermediates.
- Intermediate present in the trust store but the chain above it is not (no `-partial_chain`): complete the chain or add the root.
- An expired intermediate or root anywhere in the path fails the validity step; another chain to a valid anchor may need a different intermediate to be served.
- Private root not in the store: add it to the store the client uses.
- Two intermediates share a subject DN: check that AKI and SKI match.
Verify:
- [ ] `openssl verify` or `openssl s_client` against a clean trust store builds the full chain with the intended anchor.
- [ ] The chain order and subject/issuer links match what the server sends.

## Checked
Confirmed 2026-11-08 against the OpenSSL verification options manual (trust anchors, path building, path validation, option descriptions). Removed (the page does not give them): curl and Java error messages and exit codes, Android and Let's Encrypt cross-sign notes, `-show_chain`, and AIA-fetching claims.
Method: docs-only read of cited pages, 2026-11-08
