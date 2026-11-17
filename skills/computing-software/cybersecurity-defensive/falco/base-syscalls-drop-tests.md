---
id: computing-software.cybersecurity-defensive.falco.base-syscalls-drop-tests
name: base-syscalls-drop-tests
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [base-syscalls, dry-run, dummy-rule, log-level, syscall-tests]
level: advanced
status: docs-checked
description: "Find which syscall groups cause drops by running a never-firing rule with base_syscalls test configs and --dry-run debug output."
sources:
  - https://falco.org/docs/troubleshooting/dropping/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco's metrics lack per-syscall counters, so find the culprit by testing. Use a dummy rule that can never alert:

```yaml
- macro: spawned_process
  condition: (evt.type in (execve, execveat))
- rule: TEST Simple Spawned Process
  desc: "Test base_syscalls config option"
  enabled: true
  condition: spawned_process and proc.name=iShouldNeverAlert
  output: "%evt.type"
  priority: WARNING
```

Print the final syscall set before each test:
`sudo /usr/bin/falco -c /etc/falco/falco.yaml -r falco_rules_dummy.yaml -o "log_level=debug" -o "log_stderr=true" --dry-run`
Then run Falco normally with the same options minus the debug ones.

Tests, each a `base_syscalls` config:
1. Spawned processes only: `custom_set: [clone, clone3, fork, vfork, execve, execveat, procexit]`, `repair: false`.
2. Spawned processes plus minimum state: `custom_set: []`, `repair: true`.
3. Network accept: `custom_set: [clone, clone3, fork, vfork, execve, execveat, getsockopt, socket, bind, accept, accept4, close]`, `repair: false`.
4. Network connect: the same six process syscalls plus `getsockopt, socket, connect, close`, `repair: false`.
5. Open: the same six process syscalls plus `open, openat, openat2, close`, `repair: false`.
Continue with your own tests for other syscalls, aiming for no drops or an acceptable few.

The dry run for Test 2 prints the syscalls in rules (execve, execveat), the extra state-engine syscalls Falco adds, and the final selected set (18 syscalls in the documented example). Base_syscalls control exists since Falco 0.35.0.

Gotcha: if Test 1 already drops after you adjust `buf_size_preset`, Falco may be less usable on that system.

## Checked

2026-11-08. Read the cited dropping troubleshooting page in full. Replaced a wrong 'Test 1 set plus' statement with the explicit syscall sets, since procexit appears only in Test 1.

Method: documentation only; no commands were run.
