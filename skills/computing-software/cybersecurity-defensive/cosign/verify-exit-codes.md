---
id: computing-software.cybersecurity-defensive.cosign.verify-exit-codes
name: verify-exit-codes
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, exit-codes, ci, scripting, verification-failure]
level: practitioner
status: docs-checked
description: "Cosign's documented verification exit codes 10 to 13 and how to branch on them in CI scripts, noting that they may change."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_exit_codes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exit codes

The docs warn: "The following exit codes may be subject to change".

| Code | Meaning |
| 10 | Error verifying image due to no signature |
| 11 | Error verifying image due to non-existent tag |
| 12 | Error verifying image due to no matching signature |
| 13 | Error verifying image due to no certificate found on signature |

Use in a script:

```
cosign verify --key cosign.pub "$IMAGE"
rc=$?
case $rc in
  0) ;;
  10) echo "unsigned" ;;
  12) echo "signed by someone else" ;;
esac
```

Interpretation:
- 10 versus 12: nobody signed it versus signatures exist but none match your key or identity.
- 11: the tag does not exist; check the reference spelling and registry.
- 13: documented only as "no certificate found on signature".

The page lists only these four codes; do not treat any other non-zero code as success. Gate deployments on `rc -eq 0` only.

## Checked

2026-11-04. Confirmed on the cosign exit codes page: the warning that the codes may be subject to change and the four codes 10 to 13 with their meanings. Removed: the claim that other non-zero codes are a generic failure (not stated).

Method: documentation only; no commands were run.
