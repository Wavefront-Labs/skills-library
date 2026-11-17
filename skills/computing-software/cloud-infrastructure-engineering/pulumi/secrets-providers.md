---
id: computing-software.cloud-infrastructure-engineering.pulumi.secrets-providers
name: secrets-providers
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, secrets-provider, change-secrets-provider, awskms, passphrase]
level: practitioner
status: docs-checked
description: "Choose a Pulumi secrets provider (passphrase, awskms, azurekeyvault, gcpkms, hashivault) and change it with change-secrets-provider."
sources:
  - https://www.pulumi.com/docs/iac/concepts/secrets/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_change-secrets-provider/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets providers

Pick the provider when creating a stack:
```bash
pulumi stack init prod --secrets-provider="awskms://alias/ExampleAlias?region=us-east-1"
pulumi stack init prod --secrets-provider="azurekeyvault://mykeyvaultname.vault.azure.net/keys/mykeyname"
pulumi stack init prod --secrets-provider="gcpkms://projects/MYPROJECT/locations/MYLOCATION/keyRings/MYKEYRING/cryptoKeys/MYKEY"
pulumi stack init prod --secrets-provider="hashivault://mykey"
pulumi stack init prod --secrets-provider=passphrase
```
Providers: `default` (Pulumi Cloud), `passphrase`, `awskms` (key by alias, ID or ARN), `azurekeyvault`, `gcpkms` (key purpose ENCRYPT_DECRYPT), `hashivault` (needs `VAULT_SERVER_URL` and `VAULT_SERVER_TOKEN`).

Passphrase: set `PULUMI_CONFIG_PASSPHRASE` or `PULUMI_CONFIG_PASSPHRASE_FILE`.

Switch later (re-encrypts config and state):
```bash
pulumi stack change-secrets-provider "awskms://alias/ExampleAlias?region=us-east-1"
pulumi preview      # should show no changes
```

## Gotchas
- `Pulumi.<stack>.yaml` stores `encryptionSalt` for passphrase stacks and `encryptedKey` for the other providers; the Secrets page says these files are safe to commit.
- `pulumi config refresh` rebuilds the stack config file from the backend.
- Losing access to the key or passphrase makes the stack's secrets unreadable.

## Verify
After changing provider, `pulumi preview` shows no changes and the stack file has the new `encryptedKey` or `encryptionSalt`.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Secrets page (provider list and URL formats, environment variables, stack file keys) and the `pulumi stack change-secrets-provider` reference. Fixed: key names are `encryptionSalt` and `encryptedKey`. Removed: IAM action claims, grep verification, a `--show-secrets` claim on `config get`, a rotation recipe and the `secretsprovider` key name.
Method: documentation only; no commands were run.
