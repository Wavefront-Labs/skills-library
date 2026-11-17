---
id: computing-software.networking-hardware-and-wireless.strongswan.smartcards-pkcs11-and-tpm-keys
name: smartcards-pkcs11-and-tpm-keys
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, smartcards, pkcs11, tpm, opensc]
level: advanced
status: docs-checked
description: "Keep strongSwan private keys on smart cards or a TPM 2.0: pkcs11 module options, secrets token sections with handle, slot and pin, and tpm plugin settings."
sources:
  - https://docs.strongswan.org/docs/latest/howtos/smartcards.html
  - https://docs.strongswan.org/docs/latest/plugins/pkcs11.html
  - https://docs.strongswan.org/docs/latest/plugins/tpm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smartcards pkcs11 and tpm keys
**pkcs11 plugin.** Build with `--enable-pkcs11`. It lets charon and the pki tool use any PKCS#11 library, such as OpenSC (the tutorial uses OpenSC with pcsc-tools and libccid; do not install OpenCT, which is incompatible with pcsc-lite). Check the reader with `opensc-tool -l`. Beware of the transport key: three wrong entries irretrievably block the card.

Set modules in `charon.plugins.pkcs11.modules.<name>`: `path` (shared object), `os_locking` (no), `load_certs` (yes). Further keys: `reload_certs` (no, reload on SIGHUP), `use_dh`, `use_ecc`, `use_hasher`, `use_pubkey`, `use_rng`, all default no.

**Using the card.** Certificates on the card load automatically; CA certificates become trust anchors. The PIN comes from a `secrets` token section:

```
secrets {
  token-gw {
    handle = 45
    pin = "12345678"
  }
}
```

Keys: `handle` (hex CKA_ID or TPM handle), optional `slot`, `module`, `pin`. Omit `pin` on a laptop and `swanctl --load-creds` prompts for it; store it only for unattended gateways. Certificates in a `local` section use `handle`, `slot`, `module` or `file` (not both file and handle).

**tpm plugin.** Build with `--enable-tpm`. It uses persistent RSA and ECDSA keys bound to a TPM 2.0, IKEv2 only. Options: `ek_handle`, `fips_186_4` (no), `tcti.name` (device if the in-kernel resource manager device exists, else tabrmd; mssim is also valid), `tcti.opts`, `use_rng` (no; enable only with an authenticated session).

## Checked
2026-11-04. Confirmed against the Smart Card Configuration, pkcs11 plugin and tpm plugin pages: configure flags, module and plugin options with defaults, secrets token keys, PIN prompt behaviour, certificate loading, and the TPM IKEv2-only note and TCTI defaults.

Method: documentation only; no commands were run.
