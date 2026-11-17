---
id: computing-software.cybersecurity-defensive.trivy.trivy-usage-telemetry-and-opt-out
name: trivy-usage-telemetry-and-opt-out
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [telemetry, disable-telemetry, privacy, skip-version-check, check-trivy-dev]
level: intro
status: docs-checked
description: "Know what anonymous usage data Trivy collects, what it deliberately omits, and how to turn telemetry and the update check off."
sources:
  - https://trivy.dev/latest/docs/guide/advanced/telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy collects anonymous usage data to improve the product. Possible data: environment details (an installation identifier, Trivy version, operating system) and non-revealing scan options. The captured flags are listed on the page and include `--scanners`, `--severity`, `--format`, `--exit-code`, `--ignore-unfixed`, `--offline-scan`, `--pkg-types`, `--skip-version-check` and `--timeout`.

Privacy measures: no personal information, scan results or sensitive data is collected. The installation identifier is a one-way hash of a machine fingerprint, producing an opaque ID. Any user-controlled option value, such as file paths or image names, is omitted and never collected. Trivy is an Aqua Security product and follows the company's privacy policy.

Disable it with the `--disable-telemetry` flag, which like other Trivy flags can also be set in the YAML configuration file or by environment variable:

```bash
trivy image --disable-telemetry alpine
```

Important: disabling telemetry does not stop the version check. Trivy still connects to `check.trivy.dev` to check for updates unless `--skip-version-check` is also given. For network-restricted environments use both flags together, as described in the air-gap documentation.

## Checked

2026-11-03. Read and confirmed against the Usage Telemetry page and the Connectivity and Network considerations (air-gap) page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
