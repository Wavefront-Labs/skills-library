---
id: computing-software.cybersecurity-defensive.trivy.enable-vex-methods-and-priority
name: enable-vex-methods-and-priority
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [vex, openvex, vex-repo, show-suppressed, experimental, vulnerability-filtering]
level: advanced
status: docs-checked
description: "Enable VEX filtering with --vex using a repository, local file, OCI attestation or SBOM reference, and control priority by the order the flags are given."
sources:
  - https://trivy.dev/latest/docs/guide/supply-chain/vex/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VEX (Vulnerability Exploitability eXchange) is a standardised format for sharing information about vulnerabilities. Trivy can filter detected vulnerabilities by their VEX status. The feature is marked experimental and might change without preserving backwards compatibility.

Trivy supports four methods, all enabled with `--vex`:

| Method | Flag value |
| --- | --- |
| VEX Repository | `--vex repo` |
| Local VEX file | `--vex /path/to/vex-document.json` |
| VEX attestation in an OCI registry | `--vex oci` |
| Remote VEX files referenced in SBOMs | `--vex sbom-ref` |

Example:

```bash
trivy image ghcr.io/aquasecurity/trivy:0.52.0 --vex repo
```

You can enable several methods at once. The order of specification sets priority:

- `--vex repo --vex /path/to/vex-document.json`: the VEX Repository has priority.
- `--vex /path/to/vex-document.json --vex repo`: the local file has priority.

Suppressed findings are hidden by default; add `--show-suppressed` to display which vulnerabilities VEX filtered out. Each method has its own page for details, covered by separate skills.

## Checked

2026-11-03. Read and confirmed against the VEX page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
