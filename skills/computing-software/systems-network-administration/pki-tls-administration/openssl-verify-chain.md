---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-verify-chain
name: openssl-verify-chain
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-verify-chain, pki-openssl-tools, openssl, verify, chain-validation, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Validate a leaf against root and intermediates with openssl verify, read its error output, test purpose, revocation and hostname."
sources:
  - https://docs.openssl.org/master/man1/openssl-verify/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify chains with openssl verify
Goal: reproduce what a client would conclude about a chain.
```
openssl verify -CAfile root.pem -untrusted inter.pem leaf.pem
openssl verify -CApath /etc/ssl/certs -verify_hostname app.example.com leaf.pem
openssl verify -CAfile root.pem -untrusted inter.pem -crl_check_all -CRLfile all.crl leaf.pem
openssl verify -x509_strict -purpose sslserver -CAfile root.pem -untrusted inter.pem leaf.pem
```
- `-CAfile`, `-CApath` and `-trusted` supply trust; `-untrusted` supplies extra certificates for chain building only (such as intermediates sent by the peer).
- Error output has the form `error N at D depth lookup:text`; depth 0 is the leaf, 1 the CA that signed it. The full list of codes is in X509_STORE_CTX_get_error(3) and `openssl/x509_vfy.h`. The command ignores many errors on purpose to report all problems in a chain.
- `-show_chain` (added in OpenSSL 1.1.0) prints the chain that was built and marks certificates that came from the untrusted list.
Gotcha: pass intermediates with `-untrusted` and keep only the root in `-CAfile`, so a chain that depends on a missing intermediate fails here the way it would for a client that is not given it.
Verify:
- [ ] `openssl verify` prints `OK` using only the root in `-CAfile`.
- [ ] Failing cases (wrong host, expired) produce the expected errors.

## Checked
2026-11-03. Confirmed in the openssl-verify manual page: `-CAfile`, `-CApath`, `-untrusted`, `-trusted`, `-CRLfile`, `-crl_check`, `-crl_check_all`, `-purpose`, `-verify_hostname`, `-x509_strict`, `-show_chain` and its 1.1.0 history note, and the DIAGNOSTICS format and depth meaning. Removed: the table of numeric error codes and messages (the codes live in x509_vfy.h, not fetched), the `(3.0+)` claim for `-show_chain` (it was wrong), and the claim about intermediates in `-CAfile` becoming trust anchors.
Method: documentation only; no commands were run.
