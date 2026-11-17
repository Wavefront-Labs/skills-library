---
id: computing-software.systems-network-administration.pki-tls-administration.acme-eab-and-account-keys
name: acme-eab-and-account-keys
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [acme-eab-and-account-keys, pki-acme-protocol, acme, external-account-binding, account-key, keychange, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Manage ACME accounts: registration, external account binding for CAs that require it, contact addresses, key rollover and deactivation."
sources:
  - https://www.rfc-editor.org/rfc/rfc8555
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACME accounts, EAB and key rollover
Goal: keep issuance tied to a controlled, recoverable account.
- RFC 8555 lets a server require External Account Binding: newAccount requests then carry an `externalAccountBinding` field, and the CA gives you a key id and HMAC key.
```
certbot register --server URL --eab-kid KID --eab-hmac-key HMAC --email ops@example.com --agree-tos
```
- Certbot can also read `eab-kid` and `eab-hmac-key` from its configuration file.
- Back up the account key your client stores (find its location in the client's docs); losing it means a new account.
- Rollover: POST `keyChange` signed by old and new keys. `certbot update_account` updates the account (for example its contact); use the client's docs for key change.
- Deactivate: POST `{"status":"deactivated"}` to the account URL; `certbot unregister` deactivates a certbot account.
- Use a role mailbox for contacts.
Gotcha: `certbot unregister` is permanent for that account; do not run it to "reset" a client.
Verify:
- [ ] `certbot show_account` returns the account URL and contacts.
- [ ] Account key is in your secrets backup.

## Checked
2026-11-03. Confirmed in RFC 8555 (`externalAccountBinding` in newAccount, `keyChange`, deactivation) and the certbot command-line reference (`register`, `unregister` described as deactivate, `update_account`, `show_account`, `--eab-kid`, `--eab-hmac-key`, `eab-kid` in the config file). Removed: the acme.sh EAB command (flags not on the fetched pages), the named commercial CAs, both account key paths, the Let's Encrypt 2025 email claim and the account-per-server gotcha.
Method: documentation only; no commands were run.
