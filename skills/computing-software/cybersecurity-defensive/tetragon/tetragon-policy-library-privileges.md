---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-library-privileges
name: tetragon-policy-library-privileges
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [policylib-privileges, tetragon, privilege-escalation, suid, capset]
level: practitioner
status: docs-checked
description: "Detect /tmp execs, sudo, SUID, setuid and capset privilege changes with Tetragon observability policy library entries and jq filters."
sources:
  - "https://tetragon.io/docs/policy-library/observability/"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/policylibrary/privileges/privileges-raise.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon policy library: privilege events

Goal: audit privilege-sensitive activity. Four entries need no policy because standard `process_exec` events suffice; three (setuid family, user namespaces, capset) use the `privileges-raise` TracingPolicy.

## No policy needed (filter process_exec)
- Binary in /tmp (monitors violations of mounting /tmp `noexec`):
  `jq 'select(.process_exec != null) | select(.process_exec.process.binary | contains("/tmp/"))'`
- sudo invocation audit log: same shape with `contains("sudo")`.
- SUID/SGID binaries: select `.process_exec.process.binary_properties.setuid != null or ...setgid != null`; output shows `uid`, `euid` and `privileges_changed` such as `PRIVILEGES_RAISED_EXEC_FILE_SETUID`. Requires Process Credentials visibility enabled.
- File capabilities (set with `setcap`): select `binary_properties.privileges_changed != null`; also needs Process Credentials.

## privileges-raise.yaml (policy_name `privileges-raise`)
Apply the `privileges-raise` TracingPolicy from `examples/policylibrary/privileges/privileges-raise.yaml`. It hooks:
- `security_capset` with args `cred` (index 1), `cap_effective` (2), `cap_inheritable` (3), `cap_permitted` (4); one selector per capability arg, `matchArgs` NotEqual "0", action Post with `rateLimit: "1m"`.
- `create_user_ns` with `matchCapabilities` type Effective, operator NotIn `CAP_SYS_ADMIN` (unprivileged user namespace creation).
- `__sys_setuid`, `__sys_setgid`, `__sys_setreuid`, `__sys_setregid`, `__sys_setresuid`, `__sys_setresgid`, `__sys_setfsuid`, `__sys_setfsgid`, each with `matchArgs` Equal "0" (change to root; `__sys_setresuid` and `__sys_setresgid` match args 1 and 2, `__sys_setreuid` and `__sys_setregid` match args 0 and 1), rate-limited to 1m.

Example filters pick `process_kprobe` events whose `policy_name` tests `privileges-raise`:
- setuid family: `function_name | test("__sys_")`
- user namespace: `test("create_user_ns")`
- capset: `test("capset")`, printing `args[3]` and `args[1]`

Sample setuid output: `/usr/bin/sudo id __sys_setresuid [{"int_arg":0},...]`.

## Checked

2026-11-08. Read in full: the Tetragon observability policy library page (raw markdown `docs/content/en/docs/policy-library/observability/_index.md`) and `privileges-raise.yaml`. Confirmed the no-policy entries, Process Credentials requirement, jq filters, `privileges-raise` kprobes, selectors and 1m rate limits. Corrected the count of no-policy entries (four, not three) and capset arg indexes.

Method: documentation only; no commands were run.
