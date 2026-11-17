---
id: computing-software.cryptography-implementation.crypto-libraries.tink-keysets-and-primitives
name: tink-keysets-and-primitives
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, tink, keysets, keyset-handle, key-rotation, tinkey, output-prefix, kms-envelope, tink-keyset, tink-primitives]
level: advanced
status: docs-checked
description: "Use Google Tink keysets: primary key and rotation order, KMS-encrypted keyset storage, the 5-byte output prefix, and the tinkey commands."
sources: ["https://developers.google.com/tink/design/keysets", "https://developers.google.com/tink/key-management-overview", "https://developers.google.com/tink/tinkey-overview", "https://developers.google.com/tink/wire-format"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Tink keysets and primitives

The unit of key management in Tink is a **keyset**: a non-empty list of keys with one designated primary (used for
new sign and encrypt operations). Each key has a unique ID and a status that lets you disable it without removing
it. You reach keys through a `KeysetHandle`, so your code always handles several keys at once.

For AEAD, the keyset encrypts with the primary key and decrypts by trying keys; the key-ID prefix (below) lets
Tink try only one.

## Store keysets encrypted

A keyset serialises to the `Keyset` proto (binary or JSON). An encrypted keyset is the `EncryptedKeyset` proto,
holding an encrypted binary keyset and optionally some unencrypted `KeysetInfo` metadata. Encrypt keysets with a
key held in a KMS (Tink has built-in AWS KMS and Google Cloud KMS support) and never keep cleartext keyset files in
repositories. For the exact API in your language, read the Tink docs for that language; this skill's earlier code
samples were not verified and were removed.

## Rotation

Order matters (Tink keysets page):
1. Add a new key to the keyset but do not make it primary.
2. Roll the new keyset out to every binary that uses it.
3. Only then promote the new key to primary and distribute the keyset again.

`tinkey` commands: `create-keyset`, `add-key`, `promote-key`, `disable-key`, `enable-key`, `delete-key`,
`list-keyset`, `list-key-templates`, `convert-keyset`, `create-public-keyset`. Run `tinkey <command>` with no
arguments to see its arguments. `rotate-keyset` is deprecated (add with `add-key`, then `promote-key` once the key
is on every server) and `destroy-key` is deprecated because Tink's behaviour with destroyed keys may depend on the
version; prefer `disable-key`, and `delete-key` only when sure (deleting key material makes its ciphertexts
unreadable). Tinkey has built-in support for AWS KMS and Google Cloud KMS.

## Output prefix

Most primitives support a 5-byte output prefix: version byte `0x01` plus a 4-byte key hint (the key ID); some
legacy keys use `0x00`. Tink uses it to find the key without trying all of them. The prefix is not authenticated,
so never rely on it for security. Keys without the prefix (for example for interop with non-Tink data) require
trying each key, and some primitives, such as PRF sets, never add one.
General AEAD ciphertext format: `prefix || IV || ciphertext || tag`, the prefix being empty or the 5-byte Tink
prefix. Envelope encryption output: a 4-byte big-endian encrypted-DEK length, the encrypted DEK, then the
ciphertext in the DEK's AEAD format.

## Verify

- [ ] Keysets stored only KMS-encrypted; no cleartext keyset files in repos.
- [ ] Rotation follows add -> roll out -> promote -> later disable.
- [ ] Tink primitive wrappers used; no extraction of raw key bytes for custom crypto.

## Checked

2026-10-28. Confirmed against the Tink pages Keysets, Wire format and Tinkey (Google developer docs): keyset
definition, rotation order, output prefix layout and its lack of authentication, encrypted keyset proto, AEAD and
envelope formats, tinkey command list and deprecations, built-in AWS and Google Cloud KMS support. Removed: all Python and tinkey flag samples, template
names, the `CleartextKeysetHandle` name and the `TINK`/`RAW` template-name wording (not on these pages).
Method: documentation only; no commands were run.
