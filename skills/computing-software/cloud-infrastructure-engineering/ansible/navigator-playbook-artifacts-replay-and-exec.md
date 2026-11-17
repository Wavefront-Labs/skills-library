---
id: computing-software.cloud-infrastructure-engineering.ansible.navigator-playbook-artifacts-replay-and-exec
name: navigator-playbook-artifacts-replay-and-exec
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-navigator, playbook-artifacts, navigator-replay, navigator-exec, troubleshooting]
level: practitioner
status: docs-checked
description: "Save ansible-navigator playbook artifacts, replay a past run to inspect every task result, share artifacts safely, and run ad hoc commands inside the EE with navigator exec."
sources: ["ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)", "ansible-navigator settings schema (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/data/ansible-navigator.json)", "ansible-navigator subcommands (https://github.com/ansible/ansible-navigator/blob/main/docs/subcommands.md)", "ansible-navigator FAQ (https://github.com/ansible/ansible-navigator/blob/main/docs/faq.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Navigator playbook artifacts, replay and exec

## Artifacts
By default `ansible-navigator run` writes a JSON artifact with every event of the run
(`<playbook>-artifact-<timestamp>.json` next to the playbook).
```yaml
ansible-navigator:
  playbook-artifact:
    enable: true
    save-as: "{playbook_dir}/artifacts/{playbook_name}-{time_stamp}.json"
    replay: ""            # path of an artifact to replay
```
Placeholders for `save-as`: `{playbook_dir}`, `{playbook_name}`, `{playbook_status}`, `{time_stamp}`; the default is `{playbook_dir}/{playbook_name}-artifact-{time_stamp}.json`. CLI: `--pae false` disables artifacts (they are not compatible with `--mode stdout` when playbooks require user input), `--pas <path>` sets save-as.

## Replay
```bash
ansible-navigator replay artifacts/site-2026-10-16T09:12:44.json
```
Opens the run in the TUI: plays → tasks → per-host results with full JSON (stdout, stderr, rc,
module args, timing) — no need to re-run with `-vvv`. Use it to:
- inspect a CI failure: store the artifact as a CI job artifact, download, replay locally;
- compare two runs (open each, check the same task);
- hand a failed run to a colleague.

## Sensitive data
Artifacts record the events of the run, including task results. Treat them like logs: don't commit them (`artifacts/` in `.gitignore`), restrict CI artifact retention, never attach to public tickets.

## exec: commands inside the EE
```bash
ansible-navigator exec -- ansible --version
ansible-navigator exec -- ansible-galaxy collection list
ansible-navigator exec --eei registry.example.com/ee/platform:2.3.0 -- pip freeze
ansible-navigator exec                       # no command: runs the default, /bin/bash, in the EE
```
`exec` runs a command within an execution environment and applies all navigator settings when starting it, so it is the place to debug "module not found" or Python dependency problems. The playbook directory is mounted automatically. The `exec.shell` setting (default true) controls whether the command runs in a shell; `--exshell false` turns it off. The docs map `ansible`, `ansible-galaxy`, `ansible-test` and `ansible-vault` to `ansible-navigator exec -- <tool> ...`.

## Gotchas
- Artifacts grow with the number of events; prune old ones.
- `exec` requires execution environment support (it does not work with the EE disabled).

## Verify
- [ ] A CI job publishes the artifact; `ansible-navigator replay <file>` locally shows the failed task's full result.

## Checked

Checked 2026-10-26 against ansible-navigator main (`navigator_configuration.py`, settings schema, `docs/subcommands.md`, `docs/faq.md`). Confirmed: `playbook-artifact` keys `enable`, `replay`, `save-as` with placeholders and default name, `--pae` and `--pas`, the `exec` subcommand and its `exec.command` default (/bin/bash) and `exec.shell` default (true) with `--exshell`, `exec --` examples for ansible tools, and that exec needs execution environment support. Removed unconfirmed claims about `no_log` filtering, replay in stdout mode, artifact sizes and replay version compatibility.

Method: documentation only; no commands were run.
