---
id: computing-software.cybersecurity-defensive.trivy.vex-sbom-reference-external-documents
name: vex-sbom-reference-external-documents
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [vex-sbom-ref, cyclonedx, external-references, exploitability-statement, remote-vex]
level: advanced
status: docs-checked
description: "Let Trivy fetch VEX documents referenced from a CycloneDX SBOM externalReferences entry of type exploitability-statement using --vex sbom-ref."
sources:
  - https://trivy.dev/latest/docs/guide/supply-chain/vex/sbom-ref/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy can discover and download VEX documents referenced in the `externalReferences` of a scanned CycloneDX SBOM. The reference type must be `exploitability-statement`. The feature is experimental.

Add this top-level content to the CycloneDX SBOM to point at a remotely hosted VEX file:

```
"externalReferences": [
  {
    "type": "exploitability-statement",
    "url": "https://vex.example.com/vex"
  }
]
```

The same mechanism can retrieve VEX files stored on GitHub, for example a `url` pointing at `https://raw.githubusercontent.com/aquasecurity/trivy/refs/heads/main/.vex/trivy.openvex.json`.

This is not enabled by default. Scan the CycloneDX SBOM and explicitly specify `--vex sbom-ref`:

```shell
trivy sbom trivy.cdx.json --vex sbom-ref
```

The log reports retrieving the external VEX document from the host, followed by a notice that some vulnerabilities were ignored or suppressed and that `--show-suppressed` displays them.

All referenced VEX files are retrieved over HTTP or HTTPS and are used in the same way as if they had been specified as a local VEX file with `--vex`. The page marks this feature experimental, like the other VEX methods.

## Checked

2026-11-03. Read and confirmed against the VEX SBOM Reference page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
