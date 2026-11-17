---
id: computing-software.email-administration.dovecot.salted-hash-layout-and-nonplain-mechanisms
name: salted-hash-layout-and-nonplain-mechanisms
category: computing-software
field: email-administration
product: dovecot
tags: [salted-hash, ssha256, cram-md5, scram-sha-1, mechanism-specific-scheme, password-storage]
level: advanced
status: docs-checked
description: "How salts are stored in SSHA and crypt-style hashes, and why CRAM-MD5, DIGEST-MD5 and SCRAM need specific stored schemes."
sources:
  - https://doc.dovecot.org/main/core/config/auth/schemes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Salt placement differs by family. For `SHA512-CRYPT`, `SHA256-CRYPT` and `MD5-CRYPT` the salt comes before the hash (`$6$salt$hash`). For bcrypt the salt is part of the hash. For most other salted schemes (SMD5, SSHA, SSHA256, SSHA512) the salt follows the hash and its length can vary. Verification appends the salt to the cleartext, so SSHA256(pass, salt) is SHA256(pass plus salt) followed by the salt.

To inspect one, base64-decode it and measure. SSHA256 has a 32 byte hash, so a 36 byte decoded value means a 4 byte salt after the first 32 bytes. Dovecot detects hex or base64 encoding for some schemes (PLAIN-MD5, SHA), and `.hex`, `.b64` or `.base64` suffixes force one.

Non-cleartext mechanisms constrain storage. The password must be kept either in cleartext or in a scheme made for that mechanism, and the mechanism-specific schemes protect little:
- CRAM-MD5 needs PLAIN or the CRAM-MD5 scheme.
- DIGEST-MD5 needs the DIGEST-MD5 scheme, whose hash includes the username, so it cannot be reused for another name.
- SCRAM-SHA-1 and SCRAM-SHA-1-PLUS use the SCRAM-SHA-1 scheme.
- Allowing both CRAM-MD5 and DIGEST-MD5 requires cleartext storage.

Most installations use only cleartext mechanisms and can skip this. DES-crypt uses only the first 8 characters of the password.

## Checked

2026-11-03. Confirmed on the Password Schemes page: salt placement for SHA512-CRYPT, SHA256-CRYPT, MD5-CRYPT ($6$salt$hash), bcrypt and SMD5/SSHA*, SSHA256(pass, salt) = SHA256(pass + salt) + salt, the 32-byte hash and 36-byte decoded example, hex/base64 detection and the .hex, .b64, .base64 suffixes, the non-cleartext mechanism storage rules (CRAM-MD5, DIGEST-MD5 with username in the hash, SCRAM-SHA-1 and SCRAM-SHA-1-PLUS, both needing cleartext) and DES-crypt using only 8 characters. Nothing removed.

Method: documentation only; no commands were run.
