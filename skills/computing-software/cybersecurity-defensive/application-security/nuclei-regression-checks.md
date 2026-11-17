---
id: computing-software.cybersecurity-defensive.application-security.nuclei-regression-checks
name: nuclei-regression-checks
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [nuclei, regression-testing, custom-templates, dast, security-regression, projectdiscovery]
level: practitioner
status: docs-checked
description: "Use Nuclei templates to re-check your own fixed vulnerabilities and misconfigurations: target lists, tag and severity filters, variables, headers, validation, rate limits."
sources: ["https://docs.projectdiscovery.io/tools/nuclei/running", "https://docs.projectdiscovery.io/templates/introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nuclei templates for security regression checks

Nuclei (ProjectDiscovery) runs YAML templates against targets. Besides community templates, a defensive use is
to encode every fixed finding as your own template so it can be re-run on each deploy. Only scan assets you
own or are authorised to test.

## Options confirmed in the Nuclei running docs
- Targets: `-u <url>`, or `-l`/`-list` for a file of URLs/hosts, one per line.
- Templates: `-t` path; filter with `-tags` and `-severity` (info, low, medium, high, critical, unknown);
  `-es` excludes severities; `-etags` excludes tags.
- `-validate`: validate the passed templates.
- `-V`/`-var key=value`: custom variables for templates (for a test token or object id).
- `-H`/`-header header:value`: custom header or cookie on all HTTP requests (for authenticated checks).
- `-j`/`-jsonl`: JSONL output.
- `-rl`/`-rate-limit`: maximum requests per second (default 150): lower it for staging and agree it with the
  asset owner.
- `-ni`/`-no-interactsh`: disables the interactsh server for OAST testing and excludes OAST-based templates;
  use it if calling out to an external OAST server is unacceptable.

## Practices
- One template per fixed ticket; name and id reference the ticket; keep them in the application or AppSec
  repository. Read the template introduction for the YAML structure before writing one.
- Matchers should detect the vulnerable state precisely to avoid false alarms.
- Keep scheduled runs non-destructive.
- In CI, run the regression directory against staging after deploy and fail the job on any finding.

## Verify
Temporarily reintroduce a fixed misconfiguration in staging and confirm the pipeline reports the matching
template.

## Checked
2026-11-01. Confirmed against the Nuclei "Running" page (flags and defaults above). Removed: the sample
templates and their endpoints, `-c`, `-o`, the exact CI command, WAF user-agent note, and `{{interactsh-url}}`
syntax (the template introduction page was not read in enough detail to confirm template YAML).
Method: documentation only; no commands were run.
