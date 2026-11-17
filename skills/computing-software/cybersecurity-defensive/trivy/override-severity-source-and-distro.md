---
id: computing-software.cybersecurity-defensive.trivy.override-severity-source-and-distro
name: override-severity-source-and-distro
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [vuln-severity-source, distro, os-version, severity-priority, custom-order]
level: practitioner
status: docs-checked
description: "Use --vuln-severity-source to set your own severity source order and --distro to force the OS family and version Trivy uses for vulnerability matching."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/vulnerability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two vulnerability-specific flags override automatic behaviour.

`--distro` overrides the OS version. By default Trivy detects the OS during container image scanning and matches vulnerabilities for that OS. Use the `<family>/<version>` format, for example `alpine/3.20`, to scan an image against a different OS version, or to supply a version when no OS was detected.

`--vuln-severity-source` sets your own source priority. Give a list of sources; Trivy checks them in order until one has a severity. If no source has one, the severity is `UNKNOWN`. To combine the default logic with your sources, include the value `auto`.

The documented example scans an Alpine image whose vendor severities are:

```json
"VendorSeverity": {
  "ghsa": 3,
  "nvd": 4
}
```

- `--vuln-severity-source auto,nvd` gives `CRITICAL`, taken from `auto`.
- `--vuln-severity-source alpine,auto` gives `CRITICAL`, taken from `auto`, because alpine has no entry.
- `--vuln-severity-source alpine,ghsa` gives `HIGH`, taken from `ghsa`.
- `--vuln-severity-source alpine,alma` gives `UNKNOWN`, because neither source has a rating.

Source names are the keys that appear in `VendorSeverity` in the JSON report.

## Checked

2026-11-03. Read and confirmed against the Vulnerability Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
