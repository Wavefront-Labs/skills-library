---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.trivy-and-kics-misconfiguration-scanning
name: trivy-and-kics-misconfiguration-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, security-scanning, trivy-config, trivy-misconfig, kics, kics-ansible, iac-scanning]
level: practitioner
status: gated
description: "Scan Terraform, Kubernetes, Dockerfiles and Ansible playbooks for misconfigurations with trivy config and KICS, tune severity and exclusions, and wire both into CI."
sources: ["Trivy documentation - Misconfiguration scanning (https://trivy.dev/latest/docs/scanner/misconfiguration/)", "KICS documentation - Running KICS and supported platforms incl. Ansible (https://docs.kics.io/latest/)", "KICS - Queries and exclusions (https://docs.kics.io/latest/commands/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trivy and KICS misconfiguration scanning

## Trivy (config scanner, formerly tfsec)
```bash
trivy config --severity HIGH,CRITICAL --exit-code 1 .
trivy config --tf-vars envs/prod/prod.tfvars envs/prod        # evaluate with real variables
trivy config --format sarif --output trivy.sarif .
trivy fs --scanners misconfig,secret,vuln .                   # misconfig + secrets + lockfile vulns in one pass
```
Supports Terraform (HCL and plan JSON), CloudFormation, Kubernetes YAML, Helm charts, Dockerfiles,
Azure ARM. Ignore with justification:
```hcl
#trivy:ignore:AWS-0107 -- access via VPN, SEC-321
resource "aws_security_group" "vpn" { ... }
```
Checked on Trivy 0.76.0: both `#trivy:ignore:AVD-AWS-0107` and `#trivy:ignore:AWS-0107` (with or without a `-- reason` suffix) suppressed the
finding on the next resource while an identical unmarked resource was still reported. Findings are now numbered `AWS-0107` (the old `AVD-` prefix is still accepted).
`--tf-vars prod.tfvars` changed a `0.0.0.0/0` default to `10.0.0.0/8` and the finding disappeared. Exit code is 1 with `--exit-code 1` and findings.
Or `.trivyignore`, or `trivy.yaml` (`scan: {skip-dirs: [...], skip-files: [...]}`: the keys sit under `scan:`, per the Trivy docs).
Custom checks in Rego (`--config-check policies/`, `--check-namespaces`; flags exist in `trivy config --help`, a custom check was not written here).

## KICS (Checkmarx) — includes Ansible
KICS has queries for **Ansible playbooks** (cloud modules: amazon.aws, azure.azcollection,
google.cloud) — e.g. S3 buckets created public, security groups open to the world, unencrypted
disks — plus Terraform, Kubernetes, Docker, CloudFormation, OpenAPI, and more.
```bash   # (gated: unconfirmed, Docker not available and no Windows KICS binary here; flags below were confirmed in the KICS docs/commands.md)
docker run --rm -v "$PWD":/path checkmarx/kics:latest scan \
  -p /path -o /path/kics-results \
  --report-formats json,sarif \
  --fail-on high,critical \
  --type Ansible,Terraform \
  --exclude-paths /path/collections,/path/.cache
```
Exclusions:
- inline: `# kics-scan ignore-line`, `# kics-scan ignore-block`, file-level `# kics-scan ignore` (must be at the top of the file, before any valid line; also `disable=<query_id>`)
- by query: `--exclude-queries <uuid>`; `--exclude-severities info,low`; config file `kics.config` in the project root or `--config file` (`exclude-paths`, etc.). `--fail-on` takes critical,high,medium,low,info; `--report-formats` includes json and sarif; `--type` is case-insensitive (Ansible, Terraform, ...). Ansible Vault files can be decrypted with `ANSIBLE_VAULT_PASSWORD_FILE`.

## Which to use
- Trivy: one binary for images, filesystems, IaC config and secrets; strong Terraform/K8s coverage.
- KICS: broad platform list (docs/platforms.md lists Ansible, Terraform, Kubernetes, Helm, Dockerfile, CloudFormation, OpenAPI, Pulumi...) and has Ansible cloud queries (126 under `assets/queries/ansible/aws` alone).
- Checkov: richest graph checks and custom YAML policies for Terraform.
Many teams run Trivy for images + one IaC scanner; avoid three overlapping gates with conflicting suppressions.

## CI
Upload SARIF from either (`github/codeql-action/upload-sarif`, category per tool), fail on
high/critical for changed files, report the rest.

## Gotchas
- Scanners evaluate code, not deployed state; dynamic values (variables without defaults) may be reported as unknown or false positives — scan plan JSON where possible.
- KICS on Ansible understands only modules it has queries for; generic `command` tasks are invisible to it.
- Pin scanner versions; new releases add checks that suddenly fail builds.

## Verify
- [ ] An intentionally public S3 bucket in an Ansible playbook is flagged by KICS; an open SG in Terraform by Trivy.
