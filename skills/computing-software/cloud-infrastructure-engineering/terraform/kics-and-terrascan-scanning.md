---
id: computing-software.cloud-infrastructure-engineering.terraform.kics-and-terrascan-scanning
name: kics-and-terrascan-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, kics, terrascan, static-analysis, iac-security, sarif, misconfiguration-scanning, suppressions]
level: practitioner
status: docs-checked
description: "Scan Terraform with KICS and Terrascan: CLI and Docker runs, severity thresholds, exit codes, SARIF output, config files and inline suppressions with reasons."
sources: ["https://docs.kics.io/latest/commands/", "https://docs.kics.io/latest/running-kics/", "https://docs.kics.io/latest/results/", "https://runterrascan.io/docs/usage/command_line_mode/", "https://github.com/tenable/terrascan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KICS and Terrascan

Both scan Terraform source for misconfigurations (public buckets, open security
groups, unencrypted volumes). Run one primary scanner as a gate; a second scanner
mostly adds duplicate findings and noise.

## KICS (Checkmarx, open source)
```bash
docker run --rm -v "$PWD":/src checkmarx/kics:latest scan \
  -p /src -t Terraform -o /src/kics-out --report-formats json,sarif \
  --fail-on high,critical --exclude-paths /src/examples
```
- `--fail-on` limits which severities produce a failing exit code; `--ignore-on-exit
  results` reports without failing (warn-only rollout). Exit code encodes the highest
  severity found (60 critical, 50 high, 40 medium, 30 low, 20 info; 126 engine error), so a wrapper can map it.
- Exclusions: `--exclude-queries <query-id>` globally, `--exclude-severities info,low`.
- Inline: `# kics-scan ignore-line` above a line, `# kics-scan ignore-block` above a
  block, `# kics-scan disable=<query-id>` at the top of a file, `# kics-scan ignore`
  to skip a file. Always add a reason comment and a ticket.
- Persist options in `kics.config` (`--config kics.config`) so CI and laptops agree.
- Query IDs are UUIDs; find them in the JSON report (`query_id`) before suppressing.

## Terrascan (Tenable)
```bash
terrascan scan -i terraform -o json > terrascan.json
```
- Exit codes: 0 clean, 3 violations but no errors, 4 errors but no violations, 5 errors and
  violations, 1 invalid input. Treat them differently in CI. `-o` accepts human, json, yaml, xml.
- Inline skip inside the resource block: `#ts:skip=<rule-id> public site bucket, SEC-123`
  (copy rule IDs from the scan output). The comment goes inside the resource.
- A config file (global `-c, --config-path` flag) selects which policies are included or
  excluded for the whole scan; use inline skips for single resources.
- Check the project's maintenance status before adopting it for new pipelines; prefer
  an actively maintained scanner (KICS, Checkov, Trivy) when choosing fresh.

## Rolling out a gate
1. Run report-only for a sprint (`--ignore-on-exit results`) and publish the SARIF report
   to your code-scanning tool so findings show on PR diffs.
2. Triage: fix real issues, suppress accepted ones inline with reasons, exclude
   `examples/` and test fixtures.
3. Fail only on high/critical. Ratchet lower severities later.

## Gotchas
- Source scanning sees `var.x` not its value: a bucket ACL from a variable may pass.
  Pair with a plan-level policy (OPA/Sentinel) for value-dependent rules.
- Suppressions without reasons rot; review them in CODEOWNERS-protected files.

## Verify
- [ ] A known-bad fixture (public S3 bucket) fails the job.
- [ ] SARIF findings appear on the PR.
- [ ] Each suppression has a reason and a ticket reference.

## Checked
2026-10-28. Confirmed against the KICS commands, running and results pages (flags `-p`, `-t`, `-o`, `--report-formats` incl. sarif, `--fail-on`, `--ignore-on-exit`, `--exclude-paths`, `--exclude-queries`, `--exclude-severities`, `--config`, result exit codes, `kics-scan` ignore/ignore-line/ignore-block/disable comments, `query_id` in the JSON report) and the Terrascan README (exit codes, output types, `ts:skip=` comment inside the resource, `-c` global flag, `-i`).
Corrected: Terrascan exit codes (4 and 5 exist; 1 is invalid input); Terrascan `-o sarif` (the README lists human, json, yaml, xml).
Removed: Terrascan `-t`/`-d`/`-f` flags and the `-i tfplan` plan-scan example, the `terrascan.toml` keys, the `AC_AWS_0xxx` ID format, the unverified KICS remote-module claim, and the GitHub upload-sarif action name (not in the fetched pages).
Method: documentation only; no commands were run.
