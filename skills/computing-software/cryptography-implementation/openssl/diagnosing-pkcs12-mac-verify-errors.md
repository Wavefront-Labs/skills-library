---
id: computing-software.cryptography-implementation.openssl.diagnosing-pkcs12-mac-verify-errors
name: diagnosing-pkcs12-mac-verify-errors
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, mac-verify-error, pkcs12, pfx, openssl-pkcs12, legacy-provider, keystore-import, troubleshooting]
level: practitioner
status: docs-checked
description: "Fix 'Mac verify error: invalid password?' and PKCS#12 import failures: wrong or empty passwords, legacy RC2/3DES, MAC algorithms, Java and Windows quirks."
sources: ["https://docs.openssl.org/master/man1/openssl-pkcs12/", "https://docs.openssl.org/master/man1/openssl-passphrase-options/", "https://www.rfc-editor.org/rfc/rfc7292", "https://docs.openssl.org/master/man7/ossl-guide-migration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing PKCS#12 MAC verify and import errors

## Inspect first
```
openssl pkcs12 -in bundle.p12 -info -noout
```
`-info` prints the file structure, the algorithms used and the iteration counts. New OpenSSL 3 exports default to AES-256-CBC
with PBKDF2; old exports typically show RC2-40-CBC or 3DES algorithm names.

## Error causes
| Symptom | Cause | Fix |
|---|---|---|
| `Mac verify error: invalid password?` | Wrong password | Check keyboard layout and trailing newlines in password files |
| Same, password definitely right | Password source is wrong or the MAC itself is the problem | Check the `-passin` source (`pass:`, `env:`, `file:`); `-nomacver` skips the MAC check, to test whether only the MAC fails |
| `unsupported` / `RC2-40-CBC` / `Algorithm (RC2-40-CBC : 0)` | Legacy algorithms, OpenSSL 3 | Add `-legacy` |
| A Java, Windows or appliance importer rejects an OpenSSL 3 file | The consumer may not support the new default encryption or MAC | Re-export with `-legacy`, or choose older algorithms with `-keypbe`, `-certpbe` and `-macalg`; check the consumer's documentation for what it supports |

## Re-export cleanly
```
openssl pkcs12 -in old.p12 -legacy -nodes -out tmp.pem          # decrypt (protect tmp.pem!)
openssl pkcs12 -export -in tmp.pem -out new.p12                 # modern defaults
# then securely delete tmp.pem
```
For a legacy consumer: `openssl pkcs12 -export -legacy -in tmp.pem -out legacy.p12`.

## Gotchas
- `-nodes` is deprecated in favour of `-noenc` in 3.x but still works.
- Passwords given as `pass:` arguments are visible to other users (for example via `ps`); the passphrase-options manual advises caution and offers `env:` and `file:` sources.
- `-nomacver` only skips integrity checking; never ship files that need it.

## Verify
- [ ] `openssl pkcs12 -info -noout` succeeds with the intended password and without `-legacy` for modern consumers.
- [ ] Target platform (Java, Windows, appliance) imports the re-exported file.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-pkcs12(1): default encryption AES-256-CBC with PBKDF2, `-legacy` for RC2-40-CBC style files, `-info`, `-nomacver`, `-keypbe`/`-certpbe`/`-macalg`, `-passin`, `-nodes` deprecated since 3.0 in favour of `-noenc`; and openssl-passphrase-options(1) `pass:`/`env:`/`file:` sources. Removed the sample `-info` output, the empty-versus-no-password explanation, the Java keytool `-srckeypass` and Windows-specific rows, which no OpenSSL page supports.

Method: documentation only; no commands were run.
