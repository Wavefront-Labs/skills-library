---
id: computing-software.cloud-infrastructure-engineering.terraform.checkov-custom-policies
name: checkov-custom-policies
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, checkov-custom-policy, checkov, iac-scanning, policy-as-code, yaml-policy, skip-check]
level: practitioner
status: docs-checked
description: "Write custom Checkov policies for Terraform in YAML or Python: attribute and connection checks, scanning plans vs HCL, suppressions with justification, and CI integration."
sources:
  - https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html
  - https://www.checkov.io/3.Custom%20Policies/Python%20Custom%20Policies.html
  - https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html
  - https://www.checkov.io/7.Scan%20Examples/Terraform%20Plan%20Scanning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# checkov custom policies

## YAML policy (attribute + connection checks)
```yaml
# policies/acme_s3_tags.yaml
metadata:
  id: "CKV2_ACME_1"
  name: "S3 buckets must have Owner and DataClass tags"
  category: "GENERAL_SECURITY"
  severity: "HIGH"
definition:
  and:
    - cond_type: attribute
      resource_types: [aws_s3_bucket]
      attribute: tags.Owner
      operator: exists
    - cond_type: attribute
      resource_types: [aws_s3_bucket]
      attribute: tags.DataClass
      operator: within
      value: [public, internal, confidential]
```
Connection check (graph): every `aws_db_instance` must be connected to a security group without `0.0.0.0/0` ingress:
```yaml
definition:
  and:
    - cond_type: connection
      resource_types: [aws_db_instance]
      connected_resource_types: [aws_security_group]
      operator: exists
    - cond_type: attribute
      resource_types: [aws_security_group]
      attribute: ingress.*.cidr_blocks
      operator: not_contains
      value: 0.0.0.0/0
```
Checkov's YAML docs give the ID form `CKV2_<provider>_<number>`; pick an org-specific infix. Category must be one of the documented values (for example `GENERAL_SECURITY`, `BACKUP_AND_RECOVERY`) and severity is optional (`INFO` to `CRITICAL`). The definition's top level must be a single object (a block or an `and`/`or`/`not` operator).

## Python policy
```python
# policies/acme_rds_backup.py
from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class RdsBackupRetention(BaseResourceCheck):
    def __init__(self):
        super().__init__(name="RDS backup retention >= 14 days", id="CKV_ACME_2",
                         categories=[CheckCategories.BACKUP_AND_RECOVERY], supported_resources=["aws_db_instance"])
    def scan_resource_conf(self, conf):
        days = conf.get("backup_retention_period", [0])[0]
        return CheckResult.PASSED if isinstance(days, int) and days >= 14 else CheckResult.FAILED

check = RdsBackupRetention()
```
HCL values arrive as lists (`conf["x"][0]`), as in Checkov's own `CKV_AWS_16` example. Native checks follow the ID form `CKV_<providerType>_<serialNumber>`; custom ones can use their own infix.

## Run
```bash
checkov -d . --external-checks-dir policies --framework terraform
checkov -d . --external-checks-dir policies --check CKV2_ACME_1,CKV_ACME_2     # only these
terraform show -json tfplan > tfplan.json && checkov -f tfplan.json --external-checks-dir policies --repo-root-for-plan-enrichment .
```
Plan scanning gives Checkov additional dependencies and context that HCL scanning lacks. `--repo-root-for-plan-enrichment <dir>` takes code blocks and skip comments from the Terraform files; plan scans can also read `__change_actions__` to react to deletes.

## Suppressions
```hcl
resource "aws_s3_bucket" "logs" {
  #checkov:skip=CKV2_ACME_1:Log bucket tagged by central account automation
  bucket = "acme-logs"
}
```
The reason after the second colon is optional in Checkov, but require one in review. Global skips via `--skip-check` or a config file (`--config-file`) should be rare and documented.

## CI
Run the same command in CI, adding `-o cli -o sarif --output-file-path console,results.sarif` to print to the console and write a SARIF file. Pin checkov's version in CI so that upgrades are deliberate.

## Verify
- [ ] Fixture directories with passing and failing Terraform show the custom IDs pass/fail as expected (`checkov -d tests/fixtures/fail` exits 1).
- [ ] Suppressions all carry justifications.

## Checked
- 2026-10-28. Confirmed against Checkov's YAML custom policy page (ID form `CKV2_<provider>_<number>`, categories, severities, single top-level object, `attribute` and `connection` blocks, `exists`, `within`, `not_contains` operators, `connected_resource_types`), the Python custom policy page (`BaseResourceCheck`, `CheckCategories`, `CheckResult`, `supported_resources`, `scan_resource_conf(conf)` with list values, `CKV_<providerType>_<serial>`), the CLI reference (`--external-checks-dir`, `--check`, `-o`, `--output-file-path`, `--repo-root-for-plan-enrichment`, `--config-file`), the Terraform plan scanning page and the suppression page (`checkov:skip=<id>:<comment>`).
- Removed: `CheckResult.UNKNOWN` handling, the `checkov-action@v12` inputs, SARIF code-scanning annotation claim and the "credentials needed for plan" claim (not in the fetched pages). The example IDs, tags and the connection-policy semantics are illustrative and should be tested against fixtures.
Method: documentation only; no commands were run.
