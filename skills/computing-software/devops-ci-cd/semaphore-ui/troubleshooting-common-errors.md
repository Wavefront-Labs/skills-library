---
id: computing-software.devops-ci-cd.semaphore-ui.troubleshooting-common-errors
name: troubleshooting-common-errors
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [troubleshooting, ldap-error, git-error, gathering-facts, runner-404, semaphore-ui]
level: practitioner
status: docs-checked
description: "Fix frequent Semaphore errors: Gathering Facts on localhost, Postgres SSL, git auth prompt, flaky git, LDAP errors."
sources:
  - https://semaphoreui.com/docs/faq/troubleshooting
  - https://semaphoreui.com/docs/admin-guide/logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting common errors

Goal: map symptom to fix.

- Gathering Facts fails for localhost (Docker or snap): Ansible runs in an isolated container. Use `gather_facts: False` in the play, or set an SSH connection in the inventory: `127.0.0.1 ansible_connection=ssh ansible_ssh_user=your_localhost_user`.
- `panic: pq: SSL is not enabled on the server`: add `"options": {"sslmode": "disable"}` to the `postgres` block.
- `fatal: bad numeric config value '0' for 'GIT_TERMINAL_PROMPT': invalid unit`: an HTTPS repo needs credentials. In the Key Store create a `Login with password` key (login plus personal access token), then select it on the Repository.
- Git clone or pull fails intermittently: retries use exponential backoff; raise `git_attempts` (default 4). If failures are immediate and constant, fix credentials or URL.
- Bash output missing or incomplete: very short scripts may finish before buffered output is read; upgrade server and runners.
- `unable to read LDAP response packet: unexpected EOF`: likely a plain connection to a TLS-only LDAP server; enable TLS in the LDAP config (`ldap_needtls`).
- LDAP Result Code 49 Invalid Credentials: wrong password or `binddn`; test the bind DN with `ldapwhoami`.
- LDAP Result Code 32 No Such Object: almost always a wrong `ldap_searchdn`, less often `ldap_binddn`; check the base with `ldapsearch -s base` (code 32 means the base does not exist, code 0 means look at `ldap_searchfilter`).
- Runner prints 404 or 401: check the server URL and registration token.

Server logs: `journalctl -u semaphore.service -f` for a systemd install, `docker logs -f` for Docker (logs page).

## Checked

2026-11-07. Read in full: faq/troubleshooting.md; read the journalctl and docker logs commands in admin-guide/logs.md (lines 15-23 only, the rest of that page was not read). Confirmed: each listed symptom and fix. Corrected: the full GIT_TERMINAL_PROMPT error text, the Key Store steps, the split of LDAP 49 and 32 with their own checks. Removed: "read the server log first" as a general rule and the invented Verify step.
Method: documentation only; no commands were run.
