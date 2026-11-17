---
id: computing-software.devops-ci-cd.packer.hcp-packer-environment
name: hcp-packer-environment
category: computing-software
field: devops-ci-cd
product: packer
tags: [hcp-credentials, hcp-client-id, registry, environment, hcp-env]
level: advanced
status: docs-checked
description: "HCP Packer environment variables for credentials, project and organisation, and for turning registry pushing off."
sources:
  - "https://developer.hashicorp.com/packer/docs/hcp/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

HCP Packer behaviour is controlled by environment variables.

Credentials:

- `HCP_CLIENT_ID` and `HCP_CLIENT_SECRET` hold a service principal's key.
- `HCP_CRED_FILE` points to a credential file (Packer 1.14.2 and later); the default location is `~/.config/hcp/cred_file.json`.
- `HCP_ORGANIZATION_ID` is not required and exists for parity with the HCP SDK. `HCP_PROJECT_ID` selects the project (Packer 1.9.1 or newer); it must be set with a project-level service principal, supported from Packer 1.9.3.

Registry settings:

- `HCP_PACKER_BUCKET_NAME` names the bucket, created automatically if missing; it overrides the bucket name in an `hcp_packer_registry` block.
- `HCP_PACKER_BUILD_FINGERPRINT` sets the build fingerprint yourself. Since 1.9.0 the automatic value is a ULID, and before that it came from the Git SHA.
- `HCP_PACKER_REGISTRY` set to `0` or `OFF` stops Packer pushing artifact metadata from an otherwise configured template.

```bash
export HCP_CLIENT_ID=<id>
export HCP_CLIENT_SECRET=<secret>
packer build .
```

## Checked
2026-11-03. Confirmed against the HCP Packer page: client id and secret, `HCP_CRED_FILE` (1.14.2 and later) and its default path, organization and project ids with version notes, bucket name, build fingerprint and the registry switch. Removed unsourced failure-mode and CI advice.
Method: documentation only; no commands were run.
