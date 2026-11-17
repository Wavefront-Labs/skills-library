---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-vm-extension-certificate-distribution
name: key-vault-vm-extension-certificate-distribution
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-extensions, key-vault-vm-extension, certificate-rotation, tls-certificates, managed-identity]
level: practitioner
status: docs-checked
description: "Push and auto-refresh Key Vault certificates onto Windows and Linux VMs with the Key Vault VM extension: settings, identity, polling, store locations and troubleshooting."
sources: ["https://learn.microsoft.com/azure/virtual-machines/extensions/key-vault-windows", "https://learn.microsoft.com/azure/virtual-machines/extensions/key-vault-linux"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key Vault VM extension

**Goal:** TLS certificates renewed in Key Vault appear on IIS/nginx hosts automatically - no manual PFX copying.

## Prerequisites
- VM (or VMSS) managed identity with **Key Vault Secrets User** on the vault (the role retrieves the secret portion of a
  certificate, which includes the private key).
- Network path to the vault (private endpoint or firewall rule).

## Windows (extension version 4.x)
```json
{
  "secretsManagementSettings": {
    "pollingIntervalInS": "3600",
    "observedCertificates": [
      { "url": "https://kv-web.vault.azure.net/secrets/www-contoso-com",
        "certificateStoreName": "MY", "certificateStoreLocation": "LocalMachine",
        "accounts": ["Network Service"] } ]
  },
  "authenticationSettings": { "msiClientId": "<uami-client-id>" }
}
```
```bash
az vm extension set --name KeyVaultForWindows --publisher Microsoft.Azure.KeyVault \
  -g <rg> --vm-name web01 --settings @kv-ext.json --version 4.0
```
`certificateStoreLocation` is `LocalMachine` or `CurrentUser` (case sensitive); `accounts` optionally lists accounts
with read access to private keys (Administrators and SYSTEM get Full Control by default). An optional per-certificate
`authenticationOverride` (`{"msiClientId": ...}`) uses a different managed identity for one certificate.

## Linux
Extension `KeyVaultForLinux`. Certificates download to `certificateStoreLocation`, or by default to
`/var/lib/waagent/Microsoft.Azure.KeyVault.Store/`, as a full-chain `.pem` and a separate `.keyid` private-key file,
each versioned, with a stable symbolic link to the latest version. Point nginx at the link and reload on change.

## Behaviour
- Polls every `pollingIntervalInS`; in 4.x the value is limited to 5-60 minutes and defaults to one hour.
- Downloads the newest version of each observed certificate (versionless URL); 4.x installs the two newest versions.
- Windows 4.x: the extension reports success only if it installs all configured certificates (so sequence app
  extensions after it); chain validation runs before installing certificates with the Server Authentication EKU and a
  failure fails provisioning; linking to the latest version always occurs; private keys use CNG and are not exportable.
- Upgrading from 3.0: `linkOnRenewal`, `keyExportable` and `requireInitialSync` are removed, and you can no longer pin a
  certificate version.

## Troubleshooting
- Windows logs: `WindowsAzure\Logs\Plugins\Microsoft.Azure.KeyVault.KeyVaultForWindows\<version>\` on the system drive
  (download status) and `WaAppAgent.log` in `WindowsAzure\Logs` (update events). Certificates land in the MY store.
- 403: identity/RBAC or firewall. With any user-assigned identity on the VM, `msiClientId` is required.

## Verify
- [ ] Renew the cert in Key Vault; within one polling interval the host serves the new certificate (check expiry with openssl s_client).

## Checked
2026-10-27. Confirmed against Learn "Key Vault VM extension for Windows" and "...for Linux": version 4.0, 3.0-to-4.x
changes, 5-60 minute polling, Secrets User role, settings names, Linux default path and file layout, Windows log
folders, `az vm extension set` form. Fixed: the skill described v3 settings (`requireInitialSync`, `keyExportable`,
`linkOnRenewal`, `--version 3.0`), now removed in 4.x. Removed: `--enable-auto-upgrade`, Linux log path and the v1/v3
schema note (not in fetched pages).
Method: documentation only; no commands were run.
