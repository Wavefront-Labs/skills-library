---
id: computing-software.networking-hardware-and-wireless.tailscale.ssh-access-rule-fields
name: ssh-access-rule-fields
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [ssh-rule, check-period, accept-env]
level: advanced
status: docs-checked
description: "Use action, src, dst, users, checkPeriod and acceptEnv correctly in the ssh policy section."
sources: ["https://tailscale.com/kb/1193"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSH access rule fields

Goal: write correct `ssh` rules in the tailnet policy file.

```
{
  "action": "check",
  "src": ["group:sre"],
  "dst": ["tag:prod"],
  "users": ["root", "autogroup:nonroot"],
  "checkPeriod": "20h",
  "acceptEnv": ["GIT_EDITOR", "GIT_COMMITTER_*", "CUSTOM_VAR_V?"]
}
```

**Fields**

- `action`: `accept` allows users already authenticated in the tailnet; `check` makes them reauthenticate with the identity provider.
- `src`: user, group, tag, `user:*@<domain>` or autogroup. A bare `*` is not allowed. `autogroup:member` also covers external invited users if the destination is shared with them.
- `dst`: user, tag or autogroup, no port. Only port 22 is allowed and it is implied. A bare `*` is not allowed.
- `users`: usernames on the host. `autogroup:nonroot` allows any user except root. `localpart:*@<domain>` maps the login email local-part to the host user, only if the email is in that domain.
- `checkPeriod`: for `check` only; minimum one minute, maximum 168 hours, default 12 hours. `always` requires a check on every connection, which can break tools such as Ansible that open many connections quickly.
- `acceptEnv`: allowlist of environment variables forwarded from client; the host needs v1.76.0 or later. Wildcards `*` and `?` are shown in the example.

**Checklist**

1. No bare wildcards.
2. Usernames exist on the host.
3. checkPeriod within 1 minute to 168 hours.
4. acceptEnv host version checked.

## Checked

2026-11-03. Read Tailscale SSH (kb/1193) and confirmed action, src, dst, users, checkPeriod (1 minute to 168 hours, default 12 hours, `always`) and acceptEnv (v1.76.0) rules; changed the example group to the page's `group:sre`. Nothing else was removed.

Method: documentation only; no commands were run.
