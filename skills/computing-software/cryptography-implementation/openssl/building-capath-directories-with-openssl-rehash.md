---
id: computing-software.cryptography-implementation.openssl.building-capath-directories-with-openssl-rehash
name: building-capath-directories-with-openssl-rehash
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-rehash, capath, c-rehash, subject-hash, trust-store, update-ca-certificates, crl]
level: practitioner
status: verified
description: "Create and maintain OpenSSL CApath trust directories with openssl rehash: subject-hash symlinks, CRL links, hash collisions and distro update tools."
sources: ["https://docs.openssl.org/3.0/man1/openssl-rehash/", "https://docs.openssl.org/3.0/man1/openssl-verification-options/", "https://manpages.debian.org/stable/ca-certificates/update-ca-certificates.8.en.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CApath directories and openssl rehash

`-CApath dir` (and `SSL_CTX_load_verify_locations(ctx, NULL, dir)`) looks up issuers by **subject name hash**
filenames, not by reading every file.

## Build a directory
```
mkdir -p /etc/app/ca.d && cp root1.pem root2.pem /etc/app/ca.d/
openssl rehash /etc/app/ca.d          # creates links like 5ad8a5d6.0 -> root1.pem
ls -l /etc/app/ca.d
openssl x509 -in root1.pem -noout -subject_hash    # the hash used for the filename
```
- `.0`, `.1` suffixes handle two CAs with the same subject hash (e.g. renewed root with the same name).
- CRLs get `.r0`, `.r1` links; with `-crl_check` OpenSSL loads them from the directory.
- `c_rehash` is the older Perl script; `openssl rehash` is the built-in equivalent. The manual says it scans `.pem`, `.crt`,
  `.cer` and `.crl` files and makes a copy where symlinks are unsupported.
- Not every build includes it: the Windows OpenSSL 3.2.3 build tested prints `Not available; use c_rehash script`.
  Copying a CA file to `<subject_hash>.0` by hand gives the same lookup (tested: `openssl verify -CApath` succeeded).

## Using it
```
openssl verify -CApath /etc/app/ca.d leaf.pem
openssl s_client -connect host:443 -CApath /etc/app/ca.d -verify_return_error
curl --capath /etc/app/ca.d https://host/
```

## System stores
- Debian/Ubuntu: drop `.crt` into `/usr/local/share/ca-certificates/`, run `update-ca-certificates` (rebuilds
  `/etc/ssl/certs` links and the bundle).
- RHEL/Fedora: copy the PEM or DER file to `/etc/pki/ca-trust/source/anchors/`, then run `update-ca-trust` (Fedora
  shared system certificates guide).
- Alpine: the `ca-certificates` package provides `update-ca-certificates` (pkgs.alpinelinux.org).

## Gotchas
- Copying files into a CApath without rehashing: OpenSSL silently cannot find them ("unable to get local issuer").
- OpenSSL before 1.0.0 used an older name hash (`openssl x509 -subject_hash_old` prints it, a different value from
  `-subject_hash`); mixed old/new tooling breaks lookups.
- Symlinks are lost when copying with tools that do not preserve them; run the rehash step after the copy, at
  image or package build time.

## Verify
- [ ] Every CA file has a matching hash link (`openssl rehash -v` lists what it did).
- [ ] `openssl verify -CApath` succeeds without `-CAfile`.
