---
id: computing-software.cryptography-implementation.openssl.subject-dn-encoding-with-subj
name: subject-dn-encoding-with-subj
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, subject-dn, openssl-req, distinguished-name, utf8, x509]
level: practitioner
status: verified
description: "Write certificate subject DNs with openssl -subj correctly: RDN order, escaping slashes and plus signs, UTF-8 with -utf8, multi-valued RDNs and how to inspect results."
sources: ["https://docs.openssl.org/3.0/man1/openssl-req/", "https://docs.openssl.org/3.0/man1/openssl-namedisplay-options/", "https://www.rfc-editor.org/rfc/rfc4514"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subject DN encoding with -subj

```sh
openssl req -new -key k.pem -subj "/C=US/ST=CA/O=Example Inc/CN=api.example.com" -out r.csr
openssl req -new -key k.pem -utf8 -subj "/C=DE/O=Müller GmbH/CN=müller.example" -out r.csr
openssl req -new -key k.pem -subj "/O=A\/B Corp/CN=x" -out r.csr        # escaped slash in a value
openssl req -new -key k.pem -subj "/DC=com/DC=example/CN=a+UID=42" -out r.csr  # multi-valued RDN with +
```
- Order in `-subj` is the order written into the certificate (most significant first, `C` before `CN`).
- MSYS/Git Bash on Windows rewrites a leading `/` (tested: `-subj "/C=US/CN=x"` was rewritten to a Git install path followed by `C=US/CN=x`
  and was rejected); use `-subj "//C=US\CN=x"` or set `MSYS_NO_PATHCONV=1` (both tested).
- Use `-utf8` for non-ASCII; the manual says the default interprets values as ASCII. Strings are encoded per
  `string_mask` (default `utf8only`), producing UTF8String (confirmed with a UTF-8 config file: the organisation was a
  UTF8STRING and the country code a PRINTABLESTRING).
- On Windows, passing non-ASCII text on the command line failed in our test (`invalid utf8string`) because of the ANSI
  code page; put such values in a config file with `utf8 = yes` instead.

## Inspect
```sh
openssl req -in r.csr -noout -subject -nameopt RFC2253
openssl x509 -in c.pem -noout -subject -nameopt multiline,utf8,-esc_msb
```
RFC 2253/4514 display reverses order (CN first).

## Pitfalls
- Putting hostnames only in CN: browsers ignore CN; add SAN via `-addext "subjectAltName=DNS:api.example.com"`.
- Name chaining: issuer DN in a child must match the CA's subject byte-for-byte after canonicalisation;
  changing string types between CA and child confuses some validators.
- Country must be a 2-letter code, otherwise `req` errors.

## Verify
- [ ] `-nameopt RFC2253` output matches the intended DN; CA policy (`policy_match`) accepts it.
