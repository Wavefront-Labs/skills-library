---
id: computing-software.cryptography-implementation.openssl.openssl-verify-with-untrusted-intermediates
name: openssl-verify-with-untrusted-intermediates
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, chain-verification, openssl-verify, untrusted-intermediates, cafile, partial-chain, show-chain, x509]
level: practitioner
status: verified
description: "Verify certificate chains with openssl verify: -CAfile vs -untrusted, why intermediates should not go in the trust store, -partial_chain, -show_chain, and fullchain files."
sources: ["https://docs.openssl.org/master/man1/openssl-verify/", "https://docs.openssl.org/master/man1/openssl-verification-options/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# openssl verify with untrusted intermediates

```bash
openssl verify -CAfile root.pem -untrusted intermediates.pem -show_chain leaf.pem
```
`-show_chain` displays the chain that was built and flags certificates that came from the untrusted list as "untrusted".

## Trusted vs untrusted

- `-CAfile` / `-CApath` / `-CAstore`: **trust anchors**. Anything here is
  trusted to end a chain.
- `-untrusted`: intermediates used to build the path but not trusted by
  themselves; the chain must still end at a trust anchor.

Intermediates placed in `-CAfile` are part of the trust store, so they are no longer tested as "untrusted" path
elements and the result no longer shows whether the server supplies them. By default a trust-store certificate that is not
self-signed does not end a chain; `-partial_chain` changes that, and then trusts whatever that intermediate issues.

## Common tasks

```bash
# verify a server's fullchain file: put the leaf in leaf.pem and the other certificates in inter.pem, then
openssl verify -CAfile root.pem -untrusted inter.pem leaf.pem
# use a trust directory (hashed layout) instead of a single file
openssl verify -CApath /path/to/hashed/certs -untrusted inter.pem leaf.pem

# trust an intermediate as anchor deliberately (pinned intermediate, private PKI)
openssl verify -partial_chain -CAfile issuing-ca.pem leaf.pem

# check at a specific time (seconds since the Unix epoch; 1798761600 is 2027-01-01 00:00 UTC)
openssl verify -attime 1798761600 -CAfile root.pem -untrusted inter.pem leaf.pem
```

`-partial_chain` allows verification to succeed when the chain ends in a certificate from the trust store that is not
self-signed and has no matching positive trust attributes (self-issued or an intermediate CA); use it only when you
intentionally anchor at an intermediate.

## Gotchas

- `openssl verify` checks the chain, not a hostname or purpose, unless you
  add options (see purpose/hostname skill).
- `-no-CAfile`, `-no-CApath` and `-no-CAstore` stop the default trust locations from being used, so only your explicit
  anchors count; this avoids accidental success from the system bundle.

## Verify

- [ ] Intermediates passed with `-untrusted`, anchors only in `-CAfile`.
- [ ] Removing the intermediate makes verification fail (error 20), proving the path is real.
- [ ] Default stores disabled when testing private PKI chains.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-verify(1) and openssl-verification-options(1): `-untrusted` is for chain building only, `-show_chain` flags untrusted certificates, `-trusted`/`-CAfile`/`-CApath`/`-CAstore`, `-partial_chain` semantics, `-attime` as Unix epoch seconds, and `-no-CAfile`/`-no-CApath`/`-no-CAstore`. Corrected the claim that an intermediate in `-CAfile` becomes an anchor by default (it needs `-partial_chain`). Removed the sample output and the awk and `date -d` pipelines.

2026-11-01, run with OpenSSL 3.2.3 against a throwaway root, intermediate and leaf in a temp directory. Confirmed: the `-show_chain` example prints `(untrusted)` for the leaf and the intermediate; without `-untrusted` the result is error 20; an intermediate placed in `-CAfile` next to the root verifies; an intermediate alone as `-CAfile` fails with error 2 unless `-partial_chain` is given, which then succeeds; a hashed `-CApath` directory with `-no-CAfile` works; `-attime 1798761600` is 2027-01-01 and makes the 30-day test chain fail with error 10 (expired); `-no-CAfile -no-CApath -no-CAstore` with only `-untrusted` fails with error 20.

Method: documentation checked, then the commands were run as above (OpenSSL 3.2.3, local files only).
