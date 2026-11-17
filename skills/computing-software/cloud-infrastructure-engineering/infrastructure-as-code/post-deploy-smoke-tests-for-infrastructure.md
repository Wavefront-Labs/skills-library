---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.post-deploy-smoke-tests-for-infrastructure
name: post-deploy-smoke-tests-for-infrastructure
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, iac-testing, smoke-tests, post-deploy-tests, ansible-assert, terraform-check-blocks, goss, pipeline-gates]
level: practitioner
status: docs-checked
description: "Run fast post-deploy smoke tests after every infrastructure apply: Terraform check blocks, Ansible uri/wait_for, goss, and gating promotion on the result."
sources: ["https://developer.hashicorp.com/terraform/language/checks", "https://developer.hashicorp.com/terraform/internals/json-format", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html", "https://github.com/goss-org/goss"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-deploy smoke tests for infrastructure

Goal: a successful `apply` or playbook run only proves the tool did what it was told. A smoke test
proves the result works (DNS resolves, the endpoint answers, the port is open, the service is
healthy) shortly after the change, and blocks promotion if not.

## What to test (keep it short)
- Reachability: load balancer DNS resolves; TLS handshake succeeds with the expected cert.
- Health: the health endpoint returns 200 within a bounded time.
- Critical paths only: DB reachable from the app subnet, not from the internet.
- Negative checks: SSH closed from outside, bucket not public.
Full functional tests belong to the application pipeline; smoke tests must be fast and stable.

## Terraform: check blocks (1.5+)
```hcl
check "api_health" {
  data "http" "health" {
    url = "https://${aws_lb.api.dns_name}/healthz"
  }
  assert {
    condition     = data.http.health.status_code == 200
    error_message = "API health endpoint returned ${data.http.health.status_code}"
  }
}
```
- `check` blocks need Terraform v1.5.0 or later. They run as the last step of a plan or apply
  (after postconditions), and a failed assertion reports a **warning** and the operation continues.
- Unlike variable validation, preconditions and postconditions, a failing check does not block anything,
  so CI must look at the result itself: the JSON plan/state representation carries a checks list whose
  per-object `status` is one of pass, fail, error or unknown. The docs mark the JSON representation of
  checks as experimental, so verify the shape on your Terraform version.
- With health checks enabled on a workspace, HCP Terraform re-validates check blocks, preconditions and postconditions on each health assessment.

## Ansible: a smoke playbook after deploy
```yaml
- hosts: web
  gather_facts: false
  tasks:
    - ansible.builtin.wait_for: {port: 443, timeout: 60}
    - ansible.builtin.uri:
        url: "https://{{ inventory_hostname }}/healthz"
        status_code: 200
        validate_certs: true
- hosts: localhost
  tasks:
    - name: SSH must be closed from outside
      ansible.builtin.wait_for: {host: "{{ public_ip }}", port: 22, state: stopped, timeout: 5}
```
`wait_for` with `state: started` (the default) waits for a port to be open; `state: stopped` checks that it is closed.
`uri` accepts a `status_code` value (a single code or a list) and `validate_certs`.

## Host-level: goss
A goss file declares expected port, service and http state, and `goss validate` checks it.
Goss is a single self-contained binary, can keep retrying until the system is valid or a timeout
passes (`--retry-timeout`, `--sleep`), and can print JUnit-style output.

## Pipeline gating
apply, then smoke tests; on pass promote to the next environment; on fail alert and stop the
pipeline for a human (or roll back where that is safe). Publish JUnit results so failures are readable in CI.

## Gotchas
- Eventual consistency: DNS, LB target registration and IAM take time; use retries with a total timeout, not sleeps.
- Smoke tests from the CI runner test the runner's network path too; run negative/positive tests from the right vantage point.
- Flaky smoke tests get ignored; delete or fix any test that fails without a real problem.

## Verify
- [ ] Breaking the health endpoint in stage makes the pipeline stop before prod.

## Checked
Method: docs-checked 2026-11-09 against the Terraform validation (checks) page, Terraform JSON output format page (checks representation), Ansible wait_for and uri module pages, and the goss README.
Removed as unconfirmed: the http data source `retry` block, the testinfra command and source (page not read), the uri retries/until loop, the 2-minute duration target, and the goss.yaml sample with allow-insecure and exact http fields.
