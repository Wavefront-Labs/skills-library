---
id: computing-software.cryptography-implementation.applied-cryptography.retiring-3des-and-64-bit-block-ciphers
name: retiring-3des-and-64-bit-block-ciphers
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, tdea-retirement, 3des, tdea, triple-des, blowfish, sweet32, cve-2016-2183, sp-800-67, sp-800-131a, legacy-crypto]
level: practitioner
status: docs-checked
description: "Find and remove 3DES/TDEA, Blowfish and other 64-bit block ciphers: NIST status, Sweet32 limits, discovery commands and migration to AES."
sources: ["https://csrc.nist.gov/pubs/sp/800/131/a/r2/final", "https://csrc.nist.gov/pubs/sp/800/67/r2/final", "https://sweet32.info/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Retiring 3DES and 64-bit block ciphers

**Status:** NIST's SP 800-67 Rev 2 (TDEA) page carries a planning note announcing its withdrawal on 1 Jan 2024. For
what SP 800-131A currently allows for TDEA (and any per-key data limits), read the publication itself; this skill does
not restate those dates or limits.

## Why 64-bit blocks fail
Birthday collisions appear after about 2^32 blocks (32 GiB of 8-byte blocks). In CBC a collision leaks the XOR of two
plaintext blocks; Sweet32 (CVE-2016-2183) recovered HTTP cookies from long-lived 3DES TLS connections (about 785 GB of
captured traffic in the authors' demo). Blowfish and every other 64-bit block cipher share the problem regardless of key
size; the Sweet32 authors advise stopping use of 64-bit block ciphers or rekeying frequently.

## Discovery
```
# TLS endpoints still offering 3DES
openssl s_client -connect host:443 -cipher DES-CBC3-SHA -tls1_2 </dev/null   # handshake success = still enabled
# stock OpenSSL 3.x builds omit 3DES suites ("no cipher match" even with ALL:@SECLEVEL=0, seen on 3.2.3): use another TLS scanner unless OpenSSL was built with enable-weak-ssl-ciphers
# Code and configs
rg -i "DESede|TripleDES|3DES|DES-EDE3|des3|Blowfish|bf-cbc|CAST5" .
# Old PKCS#12 / PEM keys encrypted with 3DES
openssl pkcs12 -info -in old.p12 -noout   # look for pbeWithSHA1And3-KeyTripleDES-CBC
```
Also check payment HSM key blocks, SNMPv3 privacy settings, Kerberos enctypes, IPsec proposals and
JCE `Cipher.getInstance("DESede/...")` calls.

## Migration
1. Stop producing: switch encryption to AES-GCM (or AES-256 key wrap for keys) behind a ciphertext version byte.
2. Keep a decrypt-only 3DES path for existing data, flagged and logged.
3. Re-encrypt stored data lazily on read or with a batch job, then delete the 3DES path.
4. For TLS remove 3DES suites (`!3DES` in OpenSSL cipher strings).
5. For payment environments, follow the payment scheme's key-block migration guidance rather than ad-hoc changes.

## Gotchas
- PKCS#12 files from old Windows exports use 3DES for the key bag; re-export with OpenSSL 3 defaults (`openssl pkcs12 -help` shows AES-256 CBC as the default key and certificate PBE).
- Data volume per key matters more than key length for 64-bit ciphers; a longer Blowfish key does not help.

## Verify
- [ ] A TLS scan shows no 3DES suite accepted.
- [ ] Code search returns only the documented decrypt-only path.
- [ ] Metrics show the legacy decrypt path trending to zero before deletion.

## Checked

2026-10-31. Confirmed: the NIST SP 800-67 Rev 2 page's planning note (withdrawal on 1 Jan 2024); the Sweet32 page
(CVE-2016-2183 and CVE-2016-6329, birthday collision after 2^(n/2) blocks reveals the XOR of two plaintext blocks, 32 GB
transferable in under an hour, cookie recovery from about 785 GB of traffic, Blowfish named, advice to stop using or
rekey 64-bit ciphers). Local read-only runs with OpenSSL 3.2.3: `openssl ciphers -v DES-CBC3-SHA` gives "no cipher match"
and `ALL:@SECLEVEL=0` lists no 3DES suite; `openssl pkcs12 -help` shows AES-256 CBC defaults for key and certificate PBE;
`s_client` accepts `-connect`, `-cipher`, `-tls1_2`; `ALL:!3DES` is accepted. Removed (NIST PDFs and SP 800-131A
text unreadable): the 2023 disallow date, the "legacy use" wording, the 2^20-block / 8 MiB cap, the 2015 two-key TDEA
date, the OpenSSL DEFAULT-since-1.1.0 claim, the `-legacy` flag on pkcs12 -info, nmap and testssl.sh invocations, the
Kerberos enctype name and TR-31 reference.
Method: documentation plus the local OpenSSL runs named above.
