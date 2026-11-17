---
id: computing-software.software-engineering.tauri.tauri-windows-signing
name: tauri-windows-signing
category: computing-software
field: software-engineering
product: tauri
tags: [windows-signing, tauri, signcommand]
level: practitioner
status: docs-checked
description: "Sign Tauri Windows installers with an OV certificate, Azure Key Vault via relic, Azure Artifact Signing, or a custom signCommand."
sources:
  - "https://v2.tauri.app/distribute/sign/windows/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Windows code signing

Goal: sign Windows executables to avoid SmartScreen warnings and to list in the Microsoft Store. Signing is not required to run; Windows 11 Smart App Control blocks unknown unsigned apps and can only be turned off entirely. Signing every release with the same certificate lets SmartScreen reputation carry across releases; EV and OV certificates now build reputation the same way.

## OV certificate (acquired before June 1st 2023)

Needs a code signing certificate (not SSL). Convert and import:

```sh
openssl pkcs12 -export -in cert.cer -inkey private-key.key -out certificate.pfx
```

Import the `.pfx` with PowerShell `Import-PfxCertificate`. In `certmgr.msc` read the certificate's Thumbprint and signature hash algorithm, then set in `tauri.conf.json`:

```json
"windows": {
  "certificateThumbprint": "A1B1A2B2A3B3A4B4A5B5A6B6A7B7A8B8A9B9A0B0",
  "digestAlgorithm": "sha256",
  "timestampUrl": "http://timestamp.comodoca.com"
}
```

Run `tauri build`. In GitHub Actions, store the base64 `.pfx` (via `certutil -encode`) and password as secrets, decode with `certutil -decode`, and import before the build on `windows-latest`.

## Custom sign command

`bundle > windows > signCommand` runs any tool that signs Windows executables. It is required when cross compiling Windows installers from Linux or macOS.

- Azure Key Vault with relic: create a `src-tauri/relic.conf` with token and key (`id: https://<KEY_VAULT_NAME>.vault.azure.net/certificates/<CERTIFICATE_NAME>`), then `"signCommand": "relic sign --file %1 --key azure --config relic.conf"`. Set `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET` and grant the app the "Key Vault Certificate User" and "Key Vault Crypto User" roles.
- Azure Artifact Signing: `cargo install artifact-signing-cli`, same three env vars, and `"signCommand": "artifact-signing-cli -e https://wus2.codesigning.azure.net -a MyAccount -c MyProfile -d MyApp %1"`.

## Checked

Checked 2026-11-08 against the Tauri v2 Windows code signing page: Smart App Control and SmartScreen wording, OV-before-June-2023 scope, openssl and Import-PfxCertificate steps, certificateThumbprint, digestAlgorithm and timestampUrl keys, GitHub Actions secrets, relic.conf and signCommand for Azure Key Vault, the three Azure env vars and two roles, and artifact-signing-cli. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
