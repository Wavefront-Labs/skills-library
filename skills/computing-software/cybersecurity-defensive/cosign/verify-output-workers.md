---
id: computing-software.cybersecurity-defensive.cosign.verify-output-workers
name: verify-output-workers
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, output-format, max-workers, multiple-images, json-output]
level: practitioner
status: docs-checked
description: "Verify several images in one cosign run, choose json or text output, bound parallelism with --max-workers and log to a file."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output format, multiple images, workers

```
cosign verify --key cosign.pub <IMAGE_1> <IMAGE_2>
cosign verify --key cosign.pub -o text <IMAGE>
cosign verify --key cosign.pub --max-workers 4 <IMAGE_1> <IMAGE_2> <IMAGE_3>
```

- `-o, --output`: `json` (default) or `text` for the signing image information.
- `--max-workers`: maximum workers for parallel executions, default 10.
- `verify` accepts several image arguments (usage line and multiple-images example).
- Inherited flags: `--output-file` logs output to a file, `-t/--timeout` (default 3m0s), `-d/--verbose` for debug.

Failure exit codes are described in verify-exit-codes.

## Checked

2026-11-04. Confirmed on the cosign verify and verify-attestation reference pages: `-o, --output` json or text with default json, `--max-workers` default 10, the multiple-images example, and the inherited `--output-file`, `-t/--timeout` default 3m0s and `-d/--verbose`. Removed: the registry rate-limit advice, the claim that verify-blob takes several arguments and the scripting advice (JSON is an array of payloads) which the pages do not state.

Method: documentation only; no commands were run.
