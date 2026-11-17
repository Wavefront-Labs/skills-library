---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-secrets-section
name: swanctl-secrets-section
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, secrets, psk, eap-secret, ntlm, ppk]
level: practitioner
status: docs-checked
description: "Define IKE preshared keys, EAP and XAuth secrets, NTLM hashes, post-quantum PPKs and key passphrases in the swanctl.conf secrets section, with encodings and id matching."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl secrets section
Subsections are typed by prefix: `ike`, `eap`, `xauth` (alias for `eap`; both used for EAP and XAuth), `ntlm`, `ppk`, `private`, `rsa`, `ecdsa`, `pkcs8`, `pkcs12`, `token`. Each holds `secret` plus `id` (or several `id<suffix>` if shared).

A `secret` may be an ASCII string, hex with a `0x` prefix, or Base64 with a `0s` prefix.

```
secrets {
    ike-sun-moon {
        id-sun = sun.strongswan.org
        id-moon = moon.strongswan.org
        secret = 0sv+NkxY9LLZvwj4qCC2o/gGrWDF2d21jL
    }
    ike { secret = ... }     # fallback for any identity
    eap-carol { id = carol@strongswan.org
                secret = ... }
}
```

For PSKs, a section applies if one of its identities matches the local or remote identity; an `ike` section with no id is used when there is no better match.

`ntlm` secrets are only for EAP-MSCHAPv2 and hold the NT Hash, MD4(UTF-16LE(secret)), as 16 bytes in `0x` hex or `0s` Base64.

`ppk` holds a Postquantum Preshared Key (RFC 8784); it should have at least 256 bits of entropy for 128-bit security. Pair it with `ppk_id` and `ppk_required` on the connection.

`private`/`rsa` etc. take `file` and `secret` for decrypting a key in that folder. The page recommends against passphrases: store keys unencrypted or enter the passphrase when loading credentials.

## Checked
2026-11-04. Confirmed against the strongSwan swanctl.conf reference (secrets section): ike, eap, xauth alias, ntlm (16-byte NT hash, EAP-MSCHAPv2 only), ppk (256 bits entropy), private key passphrases and token, secret encodings 0x and 0s, PSK identity matching example. Nothing removed.

Method: documentation only; no commands were run.
