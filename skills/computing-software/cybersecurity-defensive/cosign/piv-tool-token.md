---
id: computing-software.cybersecurity-defensive.cosign.piv-tool-token
name: piv-tool-token
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, piv-tool, yubikey, set-pin, pin-policy, touch-policy, security-key, sk]
level: advanced
status: docs-checked
description: "Manage a PIV hardware token with cosign piv-tool: generate-key with PIN and touch policies, set PIN, reset, then sign with --sk and --slot."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_piv-tool.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_piv-tool_generate-key.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_piv-tool_set-pin.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_piv-tool_reset.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# piv-tool

`cosign piv-tool` provides utilities for managing a hardware token. Subcommands: attestation, generate-key, reset, set-management-key, set-pin, set-puk, unblock. The `-f, --no-input` flag skips warnings and confirmations.

```
cosign piv-tool generate-key
cosign piv-tool generate-key --slot 9c --pin-policy once --touch-policy always
cosign piv-tool set-pin --old-pin <old-pin> --new-pin <new-pin>
cosign piv-tool reset
```

generate-key flags:
- `--slot`: the help text lists authentication, signature, card-authentication or key-management. The page's default example is described as slot 9c with an always-touch policy.
- `--pin-policy`: never, once, always.
- `--touch-policy`: never, always, cached.
- `--management-key` (uses default if empty), or `--random-management-key` (generates a new random management key and deletes it after).

set-pin: `--old-pin` and `--new-pin` each "use default if empty". `reset` resets the hardware token completely.

Using the key:
```
cosign sign --sk --slot signature <IMAGE DIGEST>
cosign verify --sk <IMAGE>
```
`--sk` means use a hardware security key; for `cosign sign`, `--slot` defaults to `signature`.

## Checked

2026-11-04. Confirmed against the cosign docs pages cosign_piv-tool, piv-tool generate-key, set-pin and reset, plus the flag lines of cosign_sign and cosign_verify for `--sk` and `--slot`: subcommand list, `--no-input`, generate-key flags and allowed values, examples, set-pin flags, reset description. Removed: advice to change the factory PIN before real use, the claim that reset destroys keys and should not be run casually, and the advice to require touch to resist malware, none of which the pages state.
Method: documentation only; no commands were run.
