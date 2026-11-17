---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-runner-cli-run-start-stop
name: ansible-runner-cli-run-start-stop
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-runner, runner-run, runner-role, private-data-dir]
level: practitioner
status: docs-checked
description: "Run playbooks, roles and ad hoc modules with the ansible-runner CLI (run, start, stop, is-alive), read artifacts, and choose foreground vs background modes."
sources: ["ansible-runner standalone usage (https://github.com/ansible/ansible-runner/blob/devel/docs/standalone.rst)", "ansible-runner introduction, input directory hierarchy (https://github.com/ansible/ansible-runner/blob/devel/docs/intro.rst)", "ansible-runner command-line options (https://github.com/ansible/ansible-runner/blob/devel/src/ansible_runner/__main__.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible-runner CLI

```bash
ansible-runner run /srv/runs/deploy -p site.yml               # playbook from <pdd>/project/site.yml
ansible-runner run /srv/runs/deploy -r nginx --role-vars 'nginx_port=8080' --hosts web
ansible-runner run /srv/runs/deploy -m ansible.builtin.ping --hosts all    # ad hoc module
```
`/srv/runs/deploy` is the private data directory (pdd): `project/`, `inventory/`, `env/` (envvars, extravars, passwords, cmdline, settings, ssh_key), `artifacts/`, `roles/`.

## Background control
```bash
ansible-runner start /srv/runs/deploy -p site.yml      # background daemon, writes <pdd>/pid
ansible-runner is-alive /srv/runs/deploy               # checks a process started with start
ansible-runner stop /srv/runs/deploy
```
If a background process is already running for the same private data dir, `start` reports its pid and exits with return code 1. The daemon has no terminal: its stdout is discarded (use `--logfile` or `artifacts/<ident>/stdout`), and stderr goes to `<pdd>/daemon.log`.

## Useful options
| Option | Use |
|---|---|
| `-i` / `--ident ID` | artifact subdirectory name (default: random UUID) |
| `--limit`, `--inventory` | target selection; `--inventory` takes a file under `<pdd>/inventory/` or any path (no effect with process isolation) |
| `--cmdline '--tags x --check'` | pass raw ansible-playbook args |
| `-j` / `--json` | output raw JSON event data instead of normal output |
| `--rotate-artifacts N` | keep at most N artifact dirs (0, the default, disables cleanup) |
| `--process-isolation`, `--container-image` | run inside a container (EE); podman is the default executable |
| `--roles-path`, `--role-vars`, `--role-skip-facts` | role runs |

## Artifacts
```
artifacts/<ident>/
  rc            # exit code
  status        # outcome of the run (for example successful, failed, timeout)
  stdout        # human output
  job_events/   # one JSON per event (task start/ok/failed...)
  fact_cache/
```
Each file in `job_events/` is one JSON event (`event`, `event_data`, `stdout`); the last event of a completed run is `playbook_on_stats`.

## Gotchas
- Role runs need the role on `--roles-path` or in the private data dir's `roles/` directory.
- `env/extravars` is YAML or JSON; `env/cmdline` options have lower priority than runner's own, so they cannot override `inventory` or `limit`.
- `env/passwords` maps prompt regexes to responses and is stored in clear text; treat the directory as secret.

## Verify
- [ ] `artifacts/<ident>/status` is `successful` and `rc` is 0.

## Checked
Checked 2026-10-23 against the ansible-runner documentation and source on GitHub (docs/standalone.rst, docs/intro.rst, __main__.py; latest release 2.4.3): the four modes (run, start, stop, is-alive), pid file, daemon.log and exit code 1 behaviour, option names (--ident/-i, --limit, --inventory, --cmdline, -j/--json, --rotate-artifacts and its default, --process-isolation, --container-image, --roles-path, --role-vars, --role-skip-facts, --hosts, -m), the artifact directory layout and env/ files. Removed the pip install line, the exit-0-while-running claim, the `jq` pipeline and the exhaustive status list.
Method: documentation only; no commands were run.
