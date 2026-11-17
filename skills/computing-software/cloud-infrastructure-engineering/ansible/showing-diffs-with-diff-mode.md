---
id: computing-software.cloud-infrastructure-engineering.ansible.showing-diffs-with-diff-mode
name: showing-diffs-with-diff-mode
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, idempotency, diff-output, show-diff, diff-mode, check-mode]
level: practitioner
status: docs-checked
description: "Show what a run changes with --diff (alone or with --check), control it per task with the diff keyword, and keep secrets and huge files out of diff output."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Showing diffs with --diff

```bash
ansible-playbook site.yml --check --diff --limit web1     # preview: what would change, line by line
ansible-playbook site.yml --diff                          # apply and show what changed
```
Diff mode is most common in modules that manipulate files, such as `template`, but other modules (for
example `user`) also show before and after information. A module's documentation lists its `diff_mode`
support under attributes (for example `wait_for` declares none).

## Per task control
```yaml
- name: Render secrets file
  ansible.builtin.template: {src: creds.j2, dest: /etc/app/creds, mode: "0600"}
  diff: false               # never print this file's content
  no_log: true
```
`diff: true` on a task forces diff output even without `--diff`. Play-level `diff:` sets default.

Config:
```ini
[diff]
always = False    # ANSIBLE_DIFF_ALWAYS - True makes every run behave like --diff
context = 3       # lines of context
```

## Reading the output
```
--- before: /etc/nginx/nginx.conf
+++ after: <HOME>/.ansible/tmp/.../nginx.conf.j2
@@ -12,7 +12,7 @@
-    worker_connections 768;
+    worker_connections 4096;
```

## Use in change management
- Attach `--check --diff` output to the change request; re-run after approval without `--check`.
- In CI on merge requests: run check+diff against staging and post the output (trim to changed tasks: `ANSIBLE_DISPLAY_OK_HOSTS=false ANSIBLE_DISPLAY_SKIPPED_HOSTS=false`).

## Gotchas
- Diffs print file contents — secrets in templates leak to logs and AWX job output. Use `diff: false` / `no_log` on sensitive tasks.
- Diffs for large files are skipped above `max_diff_size` (`[defaults]` key, env `ANSIBLE_MAX_DIFF_SIZE`, default 104448 bytes).
- Diff in check mode is only as accurate as check mode: tasks depending on skipped commands may show diffs that would not occur, or miss ones that would.
- Line-ending or trailing-whitespace changes appear as full-line diffs; normalise templates.

## Verify
- [ ] `--check --diff` on a converged host prints no `---/+++` blocks.
- [ ] `grep -c 'before:' run.log` on sensitive playbooks is 0 for secret files.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/playbook_guide/playbooks_checkmode.rst: `--diff` alone or with `--check`, template and user as examples, `diff: false` per task (the section covers enforcing or preventing diff on tasks), single-host advice.
- Confirmed in config/base.yml: DIFF_ALWAYS (ini [diff] always, env ANSIBLE_DIFF_ALWAYS, default False), DIFF_CONTEXT (ini [diff] context, default 3), MAX_FILE_SIZE_FOR_DIFF (ini [defaults] max_diff_size, env ANSIBLE_MAX_DIFF_SIZE, default 104448), DISPLAY_OK_HOSTS and DISPLAY_SKIPPED_HOSTS env names; in modules/wait_for.py that diff_mode support is none.
- Removed unconfirmed claims: the per-module support list and the file-mode diff illustration.

Method: documentation only; no commands were run.
