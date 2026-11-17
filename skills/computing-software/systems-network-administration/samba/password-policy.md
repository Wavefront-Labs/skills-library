---
id: computing-software.systems-network-administration.samba.password-policy
name: password-policy
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, password-policy, passwordsettings, lockout, complexity, samba-tool]
level: practitioner
status: docs-checked
description: "Show and set the Samba AD domain password policy with samba-tool domain passwordsettings: complexity, history, age, length and account lockout defaults."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# password policy
View: `samba-tool domain passwordsettings show [-H URL]`

Set: `samba-tool domain passwordsettings set [options]`

| Option | Default |
|---|---|
| `--complexity=on\|off\|default` | on |
| `--store-plaintext=on\|off\|default` | off |
| `--history-length=N\|default` | 24 |
| `--min-pwd-length=N\|default` | 7 |
| `--min-pwd-age=DAYS\|default` | 1 |
| `--max-pwd-age=DAYS\|default` | 43 |
| `--account-lockout-duration=MINS\|default` | 30 |
| `--account-lockout-threshold=N\|default` | 0 (never lock) |
| `--reset-account-lockout-after=N\|default` | 30 |

Also `-q|--quiet` and `-H URL`.

Example: `samba-tool domain passwordsettings set --complexity=on --min-pwd-length=12`

Unlock a locked user with `samba-tool user unlock USERNAME`; find them with `samba-tool user list --locked-only`.

Gotcha: a provisioning `--adminpass` must pass complexity or provisioning fails.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: passwordsettings show/set, every option and its default, `-H`/`-q`, user unlock and `user list --locked-only`; and the Samba wiki DC setup page for the `--adminpass` complexity gotcha. Removed the pdbedit -P standalone claim (pdbedit page not read).
Method: documentation only; no commands were run.
