---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-runner-and-embedding-ansible
name: ansible-runner-and-embedding-ansible
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-runner, runner, python-api, embedding-ansible, private-data-dir, event-callbacks, job-events, artifacts, process-isolation, container-runner, execution-environments, awx-internals, runner-cli, status-handler, ansible-runner-worker, programmatic-ansible]
level: advanced
status: docs-checked
description: "Drive Ansible from code with ansible-runner: private_data_dir layout, run() with event/status callbacks, artifacts and job_events, execution-environment isolation."
sources: ["ansible-runner introduction, input directory hierarchy (https://github.com/ansible/ansible-runner/blob/devel/docs/intro.rst)", "ansible-runner Python interface (https://github.com/ansible/ansible-runner/blob/devel/docs/python_interface.rst)", "ansible-runner standalone usage (https://github.com/ansible/ansible-runner/blob/devel/docs/standalone.rst)", "ansible-runner remote jobs (https://github.com/ansible/ansible-runner/blob/devel/docs/remote_jobs.rst)", "ansible-runner execution environments (https://github.com/ansible/ansible-runner/blob/devel/docs/execution_environments.rst)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-runner and embedding Ansible

**Goal:** call playbooks from a service, a bot or a pipeline and get structured
events and status back — the same interface AWX/automation controller uses internally —
without touching Ansible's unstable Python internals.

## 1. Why runner, not `import ansible`
`ansible.executor.PlaybookExecutor` and friends are not a public API; they break between
minor versions and are awkward to isolate. `ansible-runner` wraps the CLI in a stable
contract: an input directory, a JSON event stream, an exit status, and optional container
isolation (execution environments).

## 2. The private data directory
```
job-123/
  inventory/hosts            # or a dynamic inventory script/plugin file
  project/site.yml           # playbooks, roles/, collections/ (or point at a git checkout)
  env/
    envvars                  # YAML dict -> process env (ANSIBLE_*, AWS_*)
    extravars                # YAML dict -> -e
    passwords                # regex -> answer, for prompts (e.g. '^Vault password:\s*?$': 'x')
    ssh_key                  # private key; runner wraps the Ansible call in ssh-agent
    settings                 # runner settings (idle_timeout, job_timeout, pexpect_timeout, process_isolation...)
    cmdline                  # extra ansible-playbook args as one string, e.g. "--tags deploy"
  artifacts/<ident>/         # created by runner: stdout, rc, status, job_events/*.json, fact_cache/
```
Everything under `env/` is optional and can be passed as Python kwargs instead.

## 3. Python API
```python
import ansible_runner

def on_event(e):                      # each job_event dict as it happens
    if e.get('event') == 'runner_on_failed':
        print('FAILED', e['event_data']['host'], e['event_data']['task'])
    return True                       # False drops the event from artifacts

def on_status(s, runner_config):      # starting, running, successful, failed, canceled, timeout
    print('status', s['status'])

r = ansible_runner.run(
    private_data_dir='/srv/jobs/job-123',
    playbook='site.yml',
    inventory='inventory/hosts',          # path, or an INI/YAML string, or a dict
    extravars={'release': 'v1.2.3'},
    envvars={'ANSIBLE_FORCE_COLOR': '0'},
    limit='web',
    verbosity=1,
    quiet=True,                           # disable output
    event_handler=on_event,
    status_handler=on_status,
    cancel_callback=lambda: should_cancel(),   # called each loop iteration; return True to cancel the job
    ident='run-001',
    rotate_artifacts=20,                  # keep at most 20 artifact dirs (0 = no cleanup)
    timeout=3600,
)
print(r.status, r.rc)                    # 'successful', 0
print(r.stats)                           # {'ok': {...}, 'changed': {...}, 'failures': {...}, ...}
for host, data in r.host_events('web01'): ...
print(r.get_fact_cache('web01'))         # gathered facts, if any
```
`ansible_runner.run_async()` returns `(thread, runner)` for non-blocking use. `ansible_runner.run(role='myrole', roles_path=...)` runs a role without a playbook. Ad hoc: `module='ping'`, `module_args=''`, `host_pattern='all'`.

CLI equivalent: `ansible-runner run /srv/jobs/job-123 -p site.yml --limit web`; `ansible-runner transmit`, `worker` and `process` split a job so it can run on another node (used with Receptor).

## 4. Execution environments
```python
ansible_runner.run(private_data_dir=..., playbook='site.yml',
                   process_isolation=True, process_isolation_executable='podman',
                   container_image='hub.example/acme/ee-platform:2.1',
                   container_volume_mounts=['/host/dir:/container/dir:ro'],
                   container_options=['--net=host'])
```
Runner mounts the private data dir into the container at `/runner`; the container is named `ansible_runner_<ident>`. `process_isolation_executable` defaults to podman. Path-based isolation settings (`process_isolation_hide_paths` and similar) apply only to bubblewrap, not to container engines. For a private registry, log in first or supply `container_auth_data` (`host`, `username`, `password`) in `env/settings`.

## 5. Consuming events
`artifacts/<ident>/job_events/N-<uuid>.json` — one per event with `event`, `counter`,
`stdout`, `event_data` (host, task, res, duration...). `playbook_on_stats` carries the recap.
Store them, or stream `stdout` lines (each event has pre-rendered `stdout`) to a UI.
Runner sets `ANSIBLE_STDOUT_CALLBACK` to its own `awx_display` callback and keeps any value you supplied in `ORIGINAL_STDOUT_CALLBACK`, so a stdout callback chosen through `envvars` does not replace it.

## Gotchas
- `private_data_dir` must be writable and ideally unique per job; concurrent runs sharing one dir corrupt artifacts (`ident` separates artifacts but not `env/`).
- Secrets written to `env/passwords`, `env/ssh_key` or `extravars` land on disk; `suppress_env_files=True` disables writing sensitive files into `env`, and the directory should be cleaned after the run.
- `rc` is the Ansible process return code (runner uses 254 for a timeout or cancel); `status` is `successful` only when `rc` is 0 and no timeout occurred.
- Timeouts (`env/settings`): `job_timeout` (default 3600 s) ends the job; `idle_timeout` (default 600 s) ends it when no output arrives, so raise it for long silent tasks.
- Collections/roles: either in `project/collections` and `project/roles` (auto-added to paths) or pre-installed in the EE image.

## Verify
- [ ] `ansible_runner.run(...)` on a trivial playbook returns `status == 'successful'`, `rc == 0`, and `artifacts/<ident>/job_events/` contains a `playbook_on_stats` event.
- [ ] A deliberate `fail` task yields `status == 'failed'`, a non-zero `rc`, and the `runner_on_failed` event reaches `event_handler`.
- [ ] The same run with `process_isolation=True` and a `container_image` executes inside the execution environment image.

## Checked
Checked 2026-10-23 against the ansible-runner documentation and source on GitHub (docs/intro.rst, python_interface.rst, standalone.rst, remote_jobs.rst, execution_environments.rst, interface.py, runner.py, config/_base.py; latest release 2.4.3): env/ file formats and ssh-agent wrapping, `run()` parameters (ident, quiet, rotate_artifacts, suppress_env_files, event_handler, status_handler, cancel_callback, process_isolation_executable default podman, container_* options), status values, the `/runner` mount, container naming, the awx_display stdout callback handling, runner timeouts and defaults, rc 254 on timeout or cancel. Removed `tags=` (not a documented `run()` argument), the `pip install` line, example host paths and the unconfirmed rc table and `ANSIBLE_CALLBACK_PLUGINS` claim.
Method: documentation only; no commands were run.
