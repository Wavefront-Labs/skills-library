---
id: computing-software.cryptography-implementation.openssl.encrypting-private-keys-at-rest
name: encrypting-private-keys-at-rest
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-pkey, genpkey, encrypted-private-key, pkcs8, pbes2, scrypt, passphrase-handling]
level: practitioner
status: docs-checked
description: "Encrypt private keys at rest as PKCS#8 PBES2 with a strong KDF and iteration count, pass passphrases safely, and replace legacy MD5-based PEM encryption."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs8/", "https://docs.openssl.org/3.0/man1/openssl-passphrase-options/", "https://www.rfc-editor.org/rfc/rfc8018"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Encrypting private keys at rest

An unencrypted key file is a credential lying on disk and in every backup. Encrypt with
PKCS#8 PBES2, or keep the key in a KMS/HSM and skip files entirely.

## Create or convert with explicit parameters
```
# PBES2: PBKDF2-HMAC-SHA256 + AES-256-CBC with a real iteration count
openssl pkcs8 -topk8 -in key.pem -out key.enc.pem \
  -v2 aes-256-cbc -v2prf hmacWithSHA256 -iter 600000 -passout file:pw.txt
# or scrypt as the KDF
openssl pkcs8 -topk8 -in key.pem -out key.enc.pem -scrypt \
  -scrypt_N 16384 -scrypt_r 8 -scrypt_p 1 -passout file:pw.txt
# a very large N (for example N=1048576, r=8) fails with "memory limit exceeded" on 3.2.3: keep N modest
```
`openssl pkey -aes-256-cbc` also produces PBES2 PKCS#8, but with the default count
(2048 iterations in the 3.2.3 build tested), which is too low for an offline-guessable file. Use `pkcs8 -iter`.

## Inspect what you have
```
openssl asn1parse -in key.enc.pem | head -20
```
Look for `PBES2`, `PBKDF2` (or `scrypt`), the integer iteration count (shown in hex), and `aes-256-cbc`.
A file with `Proc-Type: 4,ENCRYPTED` and `DEK-Info: AES-256-CBC,...` is the legacy OpenSSL PEM
format, not PBES2. Convert it with the `pkcs8 -topk8` command above.

## Passing the passphrase
- `-passin/-passout file:path` (mode 600 file), `env:VAR`, `fd:N` (not supported on Windows), or `stdin`.
- Avoid `pass:secret`: it shows up in `ps`, shell history and CI logs.
- In code: supply the passphrase through a password callback or the decoder passphrase API rather than a
  string literal. Zero the passphrase buffer after use.

## Where an encrypted file is the wrong answer
- Servers that restart unattended need the passphrase somewhere; if it sits next to the key
  you gained nothing. Prefer the OS keystore, a KMS-wrapped key, a TPM or a PKCS#11 HSM.
- Containers: mount the key from a secrets manager at runtime instead of baking it in.

## Interop notes
- `pkcs8 -v1` selects the older PKCS#5 v1.5 ciphers; prefer `-v2`.
- Test that every consumer of the key (Java, Go, Python, HSM tooling) can decrypt a PBES2 file with your chosen
  KDF and parameters before rolling it out; scrypt support in particular varies.

## Verify
- [ ] `asn1parse` shows PBES2 with an iteration count well above the 2048 default (600000 here) or scrypt N >= 2^14 (r=8).
- [ ] No `Proc-Type: 4,ENCRYPTED` keys remain.
- [ ] No passphrase appears on any command line, in history or in logs.

## Checked

2026-10-31. Run locally with OpenSSL 3.2.3: `openssl pkcs8 -topk8 -v2 aes-256-cbc -v2prf hmacWithSHA256 -iter 600000` produced PBES2/PBKDF2/hmacWithSHA256 (asn1parse shows the iteration count 0x0927C0 = 600000); `-scrypt -scrypt_N 16384 -scrypt_r 8 -scrypt_p 1` succeeded and asn1parse shows `scrypt`; `-scrypt_N 1048576` failed with "memory limit exceeded"; `openssl pkey -aes-256-cbc` wrote PBES2/PBKDF2 with iteration count 0x800 (2048); `openssl ec -aes-256-cbc` wrote a `Proc-Type: 4,ENCRYPTED` / `DEK-Info: AES-256-CBC` PEM. Confirmed against the OpenSSL 3.0 pages openssl-pkcs8 (`-v2`, `-v2prf`, `-iter`, `-scrypt_N/r/p`, `-topk8`) and openssl-passphrase-options (`pass:`, `env:`, `file:`, `fd:` not supported on Windows, `stdin`).
Removed: the 32 MiB and 1 GiB scrypt memory figures, the MD5/EVP_BytesToKey explanation, the named C functions, and the Java, Go and Python library claims (not checkable here; the Python `cryptography` package is not installed locally). The 600000 iteration figure is an example count, not a standard cited here.
Method: documentation, plus the local OpenSSL 3.2.3 runs listed above.
