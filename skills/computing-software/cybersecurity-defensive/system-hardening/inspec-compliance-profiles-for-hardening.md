---
id: computing-software.cybersecurity-defensive.system-hardening.inspec-compliance-profiles-for-hardening
name: inspec-compliance-profiles-for-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [inspec, compliance-as-code, profiles, hardening, cinc-auditor, audit]
level: practitioner
status: draft
description: "Write and run Chef InSpec (or Cinc Auditor) profiles to test hardening controls over SSH or WinRM, with inputs, waivers and JSON reports."
sources: ["https://docs.chef.io/inspec/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# InSpec compliance profiles

**Goal:** hardening rules as executable tests, run read-only against any host.

## Profile
```bash
inspec init profile baseline-linux
```
`controls/ssh.rb`:
```ruby
control 'ssh-01' do
  impact 1.0
  title 'SSH root login disabled'
  desc 'Direct root login is not allowed.'
  describe sshd_config do
    its('PermitRootLogin') { should cmp 'no' }
  end
end
```
Metadata in `inspec.yml`; reusable inputs in `inputs:` and overridden with `--input-file`.

## Run
```bash
inspec check baseline-linux
inspec exec baseline-linux -t ssh://auditor@host --sudo --reporter cli json:out/host.json
inspec exec baseline-linux -t winrm://admin@win --password "$WINPW" --reporter cli
inspec exec baseline-linux --waiver-file waivers.yml
```
Use key auth, never passwords in shell history. Targets: local, ssh, winrm, docker, aws, azure.

## Practice
- Reuse community baselines (DevSec) as dependencies, then add local controls; CIS-derived content is licensed.
- Tag controls with the benchmark id (`tag cis: '5.2.10'`) for traceability.
- Waivers carry justification and expiry date.
- Run in CI against freshly built images; fail the build on `impact >= 0.7` failures.
- Product licensing for the Chef-distributed binary changed over versions; Cinc Auditor is the open-source distribution. Confirm what your organisation may use.

## Verify
Break a setting deliberately: the control turns red; restore it: green; JSON report parses in your dashboard.
