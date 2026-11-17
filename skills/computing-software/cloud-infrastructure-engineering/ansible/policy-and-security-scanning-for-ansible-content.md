---
id: computing-software.cloud-infrastructure-engineering.ansible.policy-and-security-scanning-for-ansible-content
name: policy-and-security-scanning-for-ansible-content
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, policy-as-code, playbook-policy, aap-policy-enforcement, playbook-security-scan, security-scanning]
level: practitioner
status: gated
description: "Enforce policy on Ansible content (custom ansible-lint rules, KICS and Checkov playbook scans, OPA via AAP policy enforcement) and scan for risky patterns before merge."
sources: ["ansible-lint custom rules (https://ansible.readthedocs.io/projects/lint/custom-rules/)", "KICS Ansible queries (https://docs.kics.io/latest/queries/ansible-queries/)", "AAP 2.5 - policy enforcement (https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-pac)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policy and security scanning for Ansible content

## Layers
1. **ansible-lint (production profile)** catches risky patterns: `risky-file-permissions`, `risky-shell-pipe`, `command-instead-of-module`, `partial-become` (profiles.yml: `safety` adds the two `risky-*` rules, `basic` the other two; `production` extends them). `no-log-password` is an opt-in rule: enable it with `enable_list: [no-log-password]` in `.ansible-lint`. (ansible-lint could not be run here, it fails on Windows with "No module named 'grp'": gated: unconfirmed, rule ids confirmed from the source repo only.)
2. **Custom ansible-lint rules** for house policy: forbid `validate_certs: false`, `ignore_errors: true` without justification, `hosts: all`, unpinned `git` versions.
3. **KICS / Checkov** for playbooks. KICS has the broad cloud-module query set (`assets/queries/ansible/aws` has 126 queries; also azure, gcp). Checkov's `ansible` framework is much thinner: `checkov --list --framework ansible` (3.3.30) shows TLS/cert validation and package checks (CKV_ANSIBLE_1..6, CKV2_ANSIBLE_1..6), two EC2 instance checks and Palo Alto PAN checks; a playbook with `amazon.aws.ec2_security_group` open to `0.0.0.0/0` on port 22 was NOT flagged, while `uri` with `validate_certs: false` failed `CKV_ANSIBLE_1`. Use KICS for open security groups, unencrypted S3/EBS, public RDS (KICS not run here: gated: unconfirmed, no Docker or Windows binary):
```bash
kics scan -p playbooks/ --type Ansible --report-formats sarif -o results/
checkov -d playbooks/ --framework ansible
```
4. **Secret scanning** (gitleaks) for plaintext passwords outside vault.
5. **Runtime policy in AAP** (2.5 policy enforcement with OPA; OPA API v1 only): enforcement points are configured on a job template, inventory or organization and the job proceeds only if the policies allow it (per the Red Hat 2.5 "Implementing policy enforcement" chapter; not tried here, gated: unconfirmed, no AAP instance). Typical rules: prod inventories only via approved templates, extra vars restrictions.

## Custom rule sketch
```python
from ansiblelint.rules import AnsibleLintRule

class NoValidateCertsFalse(AnsibleLintRule):
    id = "acme-no-validate-certs-false"
    description = "TLS verification must not be disabled"
    severity = "HIGH"
    tags = ["security"]

    def matchtask(self, task, file=None):
        args = task.get("action", {})
        return args.get("validate_certs") in (False, "false", "no")
```
Load with `rulesdir: [rules/]` in `.ansible-lint` (the key exists in ansible-lint's config schema; the custom rule base class and `matchtask` method are in its custom-rules docs; this sketch was not executed).

## Pipeline
```yaml
- run: ansible-lint --profile production -f sarif > lint.sarif   # `-f sarif` exists; ansible-lint also has `--sarif-file`
- run: kics scan -p . --type Ansible --fail-on high
- uses: github/codeql-action/upload-sarif@v3
  with: {sarif_file: lint.sarif}
```

## Waivers
Inline `# noqa: rule-id` at the end of the line (ansible-lint docs: put a comment explaining it) or KICS `# kics-scan ignore-line`; require a reason and review waivers periodically.

## Verify
- [ ] A PR adding `validate_certs: false` fails CI with the custom rule id.
