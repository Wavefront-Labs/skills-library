---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-secret-versions-expiry-and-content-types
name: key-vault-secret-versions-expiry-and-content-types
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, key-vault, secrets, versions, expiry, content-type, rotation]
level: practitioner
status: docs-checked
description: "Key Vault secret lifecycle: versions, expires and not-before attributes, content types, Event Grid expiry events and a two-credential rotation pattern."
sources: ["https://learn.microsoft.com/azure/key-vault/secrets/about-secrets", "https://learn.microsoft.com/azure/key-vault/general/event-grid-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret versions, expiry and content types

**Goal:** secrets carry their lifecycle metadata, old versions can be disabled, and expiry drives rotation.

## Create with metadata
```bash
az keyvault secret set --vault-name kv-orders --name DbPassword --value '<value>' \
  --expires 2027-01-31T00:00:00Z --not-before 2026-11-01T00:00:00Z \
  --content-type "text/plain" --tags owner=team-orders rotation=90d
```
Every `set` creates a **new version**; readers without a version get the latest enabled one.
Maximum secret size is 25 KB. For binary (for example PFX) use `--file` with `--encoding base64` and set a
`--content-type` such as `application/x-pkcs12` so consumers know how to decode.

## Versions
```bash
az keyvault secret list-versions --vault-name kv-orders --name DbPassword \
  --query "[].{v:id,enabled:attributes.enabled,created:attributes.created,exp:attributes.expires}" -o table
az keyvault secret set-attributes --vault-name kv-orders --name DbPassword --version <ver> --enabled false
az keyvault secret show --vault-name kv-orders --name DbPassword --version <ver>
```
The `enabled` attribute controls whether secret data can be retrieved (default true). To retire a compromised version,
disable it and rotate the credential at the target system.

## What expiry does
- `exp` and `nbf` on **secrets** are documented as informational: a secret's get operation still works for
  not-yet-valid and expired secrets (so expired values can be used for recovery). Use them for alerts, policy and
  rotation automation; they don't break apps.
- Event Grid can notify on a secret about to expire (30 days before expiration), a secret that expires, and a new
  version. You must subscribe on the vault first; events fire only on new versions. Use them to trigger a rotation
  Function or a ticket.
- Azure Policy has built-in Key Vault definitions for expiration hygiene; find them in the policy definitions list.

## Rotation pattern (two-credential)
Keep two valid credentials at the target system (A and B). Rotation: regenerate the inactive one, write it as a new
secret version, apps pick it up (versionless reference / cache refresh), then retire the old one next cycle.

## Gotchas
- Pinned version URIs in app settings never see rotation - use versionless.
- Content type is free text; agree conventions (`text/plain`, `application/json`, `application/x-pkcs12`).

## Verify
- [ ] All secrets have `expires` set; a test Event Grid near-expiry event reaches the rotation handler.

## Checked
2026-10-27. Confirmed against Learn "About Azure Key Vault secrets" (25 KB maximum, exp/nbf informational, get works
outside the window, enabled attribute) and "Azure Key Vault as Event Grid source" (30 days before expiration, new
version, subscribe first). Removed: exact Event Grid event type names, exact Azure Policy definition names, "blocks
reads immediately", and the secret-name character rule (not found in fetched pages).
Method: documentation only; no commands were run.
