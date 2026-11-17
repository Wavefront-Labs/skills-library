---
id: computing-software.cloud-infrastructure-engineering.aws.image-builder-test-components-and-validation
name: image-builder-test-components-and-validation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, image-builder, image-tests, test-component, image-validation, awstoe, ami, golden-image]
level: practitioner
status: draft
description: "Validate golden images in EC2 Image Builder: AWSTOE test components, build/validate/test phases, AWS-managed tests, local awstoe runs and failing pipelines."
sources: ["https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-component-manager.html", "https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-use-documents.html", "https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-action-modules.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image Builder test components and image validation

**Goal:** an AMI that boots but has a broken agent, open port or missing hardening never
reaches launch templates.

## 1. Phases
Build components run `build` and `validate` phases on the **build instance**; test components
run the `test` phase on a **fresh test instance launched from the new image** — i.e. a real
boot test. A failing step fails the pipeline and the image is not distributed.

## 2. A test component (AWSTOE YAML)
```yaml
name: baseline-tests
description: Post-boot checks for the golden image
schemaVersion: 1.0
phases:
  - name: test
    steps:
      - name: SsmAgentRunning
        action: ExecuteBash
        inputs:
          commands:
            - systemctl is-active amazon-ssm-agent
      - name: NoPasswordSsh
        action: ExecuteBash
        inputs:
          commands:
            - sshd -T | grep -qi '^passwordauthentication no'
      - name: OnlyExpectedListeners
        action: ExecuteBash
        inputs:
          commands:
            - |
              unexpected=$(ss -tlnH | awk '{print $4}' | grep -vE ':(22|323)$' || true)
              [ -z "$unexpected" ] || { echo "unexpected listeners: $unexpected"; exit 1; }
      - name: ImdsV2Default
        action: ExecuteBash
        inputs:
          commands:
            - test "$(curl -s -o /dev/null -w '%{http_code}' http://169.254.169.254/latest/meta-data/)" = "401"
```
```bash
aws imagebuilder create-component --name baseline-tests --semantic-version 1.0.0 --platform Linux \
  --data file://baseline-tests.yml
```
Add it to the recipe's components (tests can also be attached via the image recipe's test
list in the console). AWS-managed tests exist (e.g. `reboot-linux`, `inspector-test`,
`simple-boot-test-linux`) — include a reboot test.

## 3. Run locally before publishing
```bash
awstoe validate --documents baseline-tests.yml
sudo awstoe run --documents baseline-tests.yml --phases test
```
On an instance from the candidate AMI — far faster than iterating through the pipeline.

## 4. Failing usefully
- Logs: S3 bucket from the infrastructure configuration
  (`imagebuilder/<pipeline>/<version>/TOE_*/`), plus `/var/lib/amazon/toe/` on the instance.
- `terminateInstanceOnFailure=false` in infrastructure configuration keeps the instance for
  debugging (remember to clean up).

## Gotchas
- Test instances use the infrastructure configuration's subnet/SG/role — tests needing
  internet or SSM need those paths.
- `ExecuteBash` steps fail on non-zero exit; multi-line scripts need `set -e` semantics explicitly.
- Enable image scanning (Inspector) in the pipeline for CVE gating too.

## Verify
- [ ] Introduce a deliberate defect (e.g. enable password auth): pipeline fails at the test phase and no AMI is distributed.
- [ ] Clean build passes all tests; logs in S3 show each step `success`.
- [ ] `awstoe validate` passes in CI for every component change.
