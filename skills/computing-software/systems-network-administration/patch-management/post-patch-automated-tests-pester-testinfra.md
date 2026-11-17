---
id: computing-software.systems-network-administration.patch-management.post-patch-automated-tests-pester-testinfra
name: post-patch-automated-tests-pester-testinfra
category: computing-software
field: systems-network-administration
product: patch-management
tags: [testinfra, pester, patch-testing, smoke-test, post-patch-checks, automation]
level: practitioner
status: docs-checked
description: "Write automated post-patch test suites with Pester (Windows) and testinfra (Linux) that check services, ports, versions and app endpoints, and gate ring promotion on the results."
sources:
  - https://pester.dev/docs/quick-start
  - https://pester.dev/docs/commands/Invoke-Pester
  - https://pester.dev/docs/assertions/
  - https://testinfra.readthedocs.io/en/latest/
  - https://testinfra.readthedocs.io/en/latest/backends.html
  - https://testinfra.readthedocs.io/en/latest/modules.html
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-nettcpconnection
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-hotfix
  - https://learn.microsoft.com/en-us/powershell/module/webadministration/get-webapppoolstate
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated post-patch tests

Manual "looks fine" checks don't scale past a few servers. Encode what "healthy" means per
role and run it after every patch batch; failures halt promotion to the next ring.

## Windows: Pester
Pester files are named `*.Tests.ps1` and use `Describe`, `It` and `Should`; the classic `Should -Be` operators below still work in Pester 6, which also adds `Should-*` assertions.
```powershell
# Tests\WebServer.Tests.ps1
Describe "IIS web role after patching" {
  It "W3SVC running"            { (Get-Service W3SVC).Status | Should -Be 'Running' }
  It "App pool started"         { (Get-WebAppPoolState -Name 'AppPool1').Value | Should -Be 'Started' }
  It "Port 443 listening"       { (Get-NetTCPConnection -LocalPort 443 -State Listen -EA 0) | Should -Not -BeNullOrEmpty }
  It "Health endpoint 200"      { (Invoke-WebRequest https://localhost/health -UseBasicParsing).StatusCode | Should -Be 200 }
  It "Expected LCU installed"   { Get-HotFix -Id $env:EXPECTED_KB -EA 0 | Should -Not -BeNullOrEmpty }
}
```
Run remotely and export results:
```powershell
Invoke-Pester -Path .\Tests -Output Detailed -CI     # -CI enables test result output and exits after the run
```
For build systems, `-CI` enables test result output and fails the process when tests fail; `New-PesterConfiguration` (`TestResult`) controls the result file path and format. `Get-WebAppPoolState` needs the WebAdministration module on the target.

## Linux: testinfra (pytest)
```python
# test_web.py
def test_nginx_running(host):
    s = host.service("nginx"); assert s.is_running and s.is_enabled
def test_port(host):
    assert host.socket("tcp://0.0.0.0:443").is_listening
def test_kernel_reported(host):
    assert host.check_output("uname -r")  # compare with the version your change record expects
def test_health(host):
    assert host.run("curl -fsS https://localhost/health -k").rc == 0
```
```sh
py.test --hosts='ansible://webservers' --ansible-inventory=inventory.ini test_web.py
```
The `ansible://` prefix selects the Ansible backend; without `--ansible-inventory` the default `/etc/ansible/hosts` is used. Add pytest's own result-file options (see the pytest documentation) for CI.

## Wiring into the patch pipeline
- Ansible: `serial` limits how many hosts a play manages at once, and with `serial` the failure scope is the batch; `max_fail_percentage` modifies that. Run the tests as the last step of each batch.
- CI/CD or orchestration tool reads the result file or exit code; green → promote ring, red → page
  owner and pause.
- Keep tests in version control per role; app teams own app-level checks.

## Gotchas
- Tests must run after services settle (wait loops), not seconds after reboot.
- Test what users feel (synthetic transaction), not only service status.

## Verify
A deliberately stopped service in a test VM fails the suite and blocks the next batch.

## Checked
Date: 2026-11-08. Documentation: Pester quick start, Invoke-Pester reference (-CI, -Output Detailed, -Path), Pester assertions page (Should -Be, -BeNullOrEmpty, -BeFalse), Learn pages for Get-NetTCPConnection (-LocalPort, -State Listen), Get-HotFix, Get-WebAppPoolState and Invoke-WebRequest (-UseBasicParsing, StatusCode), testinfra home, backends (ansible:// prefix, --ansible-inventory, default /etc/ansible/hosts) and modules (service is_running/is_enabled, socket tcp://0.0.0.0:port is_listening, check_output, run().rc), Ansible strategies guide (serial, max_fail_percentage). Removed: the NUnit testResults.xml claim for -CI, the RebootPending registry test, the rpm/awk kernel comparison, and the --junitxml flag (pytest option not on the cited pages).
Method: documentation only; no commands were run.
