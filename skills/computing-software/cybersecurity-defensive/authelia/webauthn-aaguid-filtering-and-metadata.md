---
id: computing-software.cybersecurity-defensive.authelia.webauthn-aaguid-filtering-and-metadata
name: webauthn-aaguid-filtering-and-metadata
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, webauthn, aaguid, attestation, metadata, mds3, backup-eligibility]
level: sme
status: docs-checked
description: "Restrict which authenticators users may register in Authelia using permitted or prohibited AAGUIDs, backup eligibility, and the FIDO metadata validation block."
sources:
  - https://www.authelia.com/configuration/second-factor/webauthn/
  - https://www.authelia.com/reference/cli/authelia/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Organisations that mandate certain hardware keys can filter registrations.

```yaml
webauthn:
  attestation_conveyance_preference: 'direct'
  filtering:
    permitted_aaguids: []
    prohibited_aaguids: []
    prohibit_backup_eligibility: false
  metadata:
    enabled: false
    cache_policy: strict
    validate_trust_anchor: true
    validate_entry: true
    validate_status: true
    validate_status_prohibited:
      - 'REVOKED'
      - 'USER_KEY_PHYSICAL_COMPROMISE'
      - 'USER_KEY_REMOTE_COMPROMISE'
      - 'USER_VERIFICATION_BYPASS'
      - 'ATTESTATION_KEY_COMPROMISE'
```

- `permitted_aaguids` is an allow list of Authenticator Attestation GUIDs; `prohibited_aaguids` is a deny list. They are mutually exclusive.
- Conveyance of attestation statements is what exposes the AAGUID to the server, so set `attestation_conveyance_preference` deliberately when you filter.
- `prohibit_backup_eligibility: true` rejects authenticators that can export credentials, which in practice prevents synchronised passkeys.
- The `metadata` block enables validation against FIDO Metadata Service data. The defaults shown validate the trust anchor, the entry and the authenticator status, and prohibit statuses indicating compromise or a bypass.

The CLI has `authelia storage cache mds3` subcommands (`status`, `update`, `dump`, `delete`) for managing the cached metadata, and `authelia storage user webauthn` subcommands (`list`, `verify`, `delete`, `export`, `import`) for credentials.

Check: with a deny list set, attempt to register the denied model and confirm registration fails.

## Checked

2026-11-08. Read the full Authelia WebAuthn page and the CLI command index. Confirmed permitted_aaguids and prohibited_aaguids (mutually exclusive), prohibit_backup_eligibility, the metadata block and its default prohibited statuses, and that the CLI lists storage cache mds3 status, update, dump and delete and storage user webauthn list, verify, delete, export and import. Fixed trailing commas in the sources list.

Method: documentation only; no commands were run.
