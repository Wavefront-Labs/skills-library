---
id: computing-software.digital-privacy-hygiene.password-managers.storing-wifi-licence-and-server-items
name: storing-wifi-licence-and-server-items
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-item-templates, vault-items, secure-notes]
level: practitioner
status: draft
description: "Store Wi-Fi networks, software licences, server and database logins, router admin and bank details as structured vault items instead of loose notes."
sources:
  - "https://support.1password.com/item-categories/"
  - "https://bitwarden.com/help/managing-items/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Storing Wi-Fi, licence and server items

**Goal:** the vault holds everything sensitive in searchable, structured form, so nothing lives in a text file on
the desktop.

## Item types by manager
| Data | 1Password category | Bitwarden | KeePassXC |
|---|---|---|---|
| Wi-Fi | Wireless Router (network name, password, base station, admin) | Login with custom fields `SSID`, `Security` | Entry with attributes |
| Software licence | Software License (key, registered email, version, order no.) | Secure note with custom fields | Entry + attachment |
| Server/SSH | Server or SSH Key | Login + SSH key item type | Entry + attachment/SSH agent |
| Database | Database (type, host, port, db, user) | Login with custom fields | Entry |
| Bank account | Bank Account (routing, account, PIN) | Identity/secure note + hidden fields | Entry |

## Conventions that pay off
- Title pattern `Service - account` (`Router - home admin`, `Postgres - prod read-only`).
- Put the URL/host in the URI field even for non-web items so search works.
- Use **hidden** custom fields for PINs and keys (Bitwarden "Hidden" type; 1Password concealed field).
- Attach licence files or recovery PDFs to the item, not a separate note.
- Folder or tag `infrastructure` vs `personal`.

## Gotchas
- Don't store the vault's own master password or 2FA backup codes for the vault account inside it.
- For SSH keys, use the manager's SSH key item and agent so the private key never sits on disk unencrypted.

## Verify
Search for "wifi", "license", the router IP: each returns one structured item.
