---
id: computing-software.cybersecurity-defensive.cosign.troubleshooting-verify
name: troubleshooting-verify
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, troubleshooting, no-signatures-found, rekor-v2, timestamps, upgrade]
level: practitioner
status: docs-checked
description: "Diagnose common cosign failures from the README: timestamp threshold errors, no signatures found, HTTP errors while signing, and exit-code triage."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_exit_codes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting

First: use a recent release. The project actively supports the most recent release and the last release in the v2 series.

Known issues and remedies (README):

1. `failed to verify timestamps: threshold not met for verified log entry integrated timestamps: 0 < 1`: the signature may need RFC3161 timestamp support. Upgrade cosign, or with Cosign 2.6.x use `--use-signed-timestamps`.
2. `no signatures found`: the signature may need Rekor v2 transparency log support. Upgrade.
3. Signing fails with HTTP errors: signing depends on several Sigstore services; retry. File issues for specific failures.

Triage list:
- Exit code 10, 11, 12 or 13 tells you unsigned, missing tag, no matching signature or no certificate (see verify-exit-codes).
- Run `cosign tree <IMAGE>` to see whether anything is attached (see tree-artifacts).
- Rerun with `-d` for debug output; `-t` raises the 3m0s default timeout.
- For keyless, check the identity and issuer values exactly (see verify-keyless-identity).
- If signatures were stored elsewhere, set `COSIGN_REPOSITORY` (see cosign-repository-env).
- Old-format versus new bundle differences: check `--new-bundle-format` in your version's help.

Help channels: the README points to the project issue tracker and a Slack channel.

## Checked

2026-11-04. Confirmed in the cosign README Troubleshooting section (support policy, the two verification errors and remedies, HTTP errors while signing, issue tracker and Slack pointer), on the cosign exit codes page (10 to 13), the inherited `-d` and `-t` flags (default 3m0s) on the reference pages, and the cosign tree page. Removed nothing material; the triage bullets are cross-references to sibling skills.

Method: documentation only; no commands were run.
