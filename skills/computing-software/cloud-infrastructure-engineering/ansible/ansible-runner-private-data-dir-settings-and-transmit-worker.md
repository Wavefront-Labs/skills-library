---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-runner-private-data-dir-settings-and-transmit-worker
name: ansible-runner-private-data-dir-settings-and-transmit-worker
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-runner, runner-settings, runner-passwords, runner-transmit, remote-runner, private-data-dir]
level: advanced
status: docs-checked
description: "Configure ansible-runner via the private data dir env/ files (settings, envvars, extravars, passwords, ssh_key) and run jobs remotely with transmit, worker and process."
sources: ["ansible-runner introduction, input directory hierarchy (https://github.com/ansible/ansible-runner/blob/devel/docs/intro.rst)", "ansible-runner remote job execution (https://github.com/ansible/ansible-runner/blob/devel/docs/remote_jobs.rst)", "ansible-runner Python interface (https://github.com/ansible/ansible-runner/blob/devel/docs/python_interface.rst)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-runner: private data dir settings and transmit/worker

## Private data directory
```
runner-dir/
  env/
    settings          # runner behaviour (YAML)
    envvars           # environment for ansible (YAML dict)
    extravars         # extra vars (YAML/JSON)
    passwords         # regex → response map for interactive prompts
    cmdline           # extra ansible-playbook CLI args, one string (lower priority than runner's own)
    ssh_key           # private key content; runner wraps the Ansible call in ssh-agent
  inventory/hosts
  project/site.yml
  artifacts/          # written by runner: <ident>/{stdout, job_events/, rc, status}
```
`env/settings`:
```yaml
idle_timeout: 600          # default 600: end the run if no output for this many seconds
job_timeout: 3600          # default 3600: maximum run time in seconds
pexpect_timeout: 10
suppress_ansible_output: false
process_isolation: true
process_isolation_executable: podman
container_image: registry.example.com/ee/platform:1.0.0
container_options: ["--network=host"]
```
`env/passwords` answers prompts (vault, become, SSH):
```yaml
"^SSH [pP]assword:\\s*?$": "s3cret"
"^BECOME [pP]assword:\\s*?$": "s3cret"
"^Vault password:\\s*?$": "vaultpw"
```
Each env file may also be a named pipe. These files hold secrets in clear text, so restrict access to the directory and clean it up after runs.

```bash
ansible-runner run runner-dir -p site.yml --ident deploy-42
cat runner-dir/artifacts/deploy-42/rc
```

## Remote execution: transmit / worker / process
Splits a job into a stream so it can run elsewhere; the feature is primarily intended for Receptor:
```bash
# controller side: package the job
ansible-runner transmit runner-dir -p site.yml > job.stream
# execution side: run it, stream results back
ssh exec-node 'ansible-runner worker --private-data-dir /tmp/pd' < job.stream > results.stream   # /tmp/pd is an example path
# controller side: unpack events/artifacts
ansible-runner process runner-dir < results.stream
```
Or piped in one line: `ansible-runner transmit ... | ssh node ansible-runner worker | ansible-runner process runner-dir`.
Without `--private-data-dir`, `worker` extracts the job into a temporary directory that is deleted afterwards. With `--private-data-dir`, the directory persists unless `--delete` is also given (it is then removed before and after the run). `ansible-runner worker cleanup --file-pattern=<glob>` removes old directories out of band (see also `--grace-period`, `--remove-images`, `--image-prune`). `process` writes artifacts under `<dir>/artifacts`, or `<dir>/artifacts/<ident>` with `--ident`. The Python API takes `streamer='transmit'|'worker'|'process'`.

## Python interface
```python
import ansible_runner
r = ansible_runner.run(private_data_dir="runner-dir", playbook="site.yml",
                       extravars={"version": "1.4"}, envvars={"ANSIBLE_FORCE_COLOR": "0"})
print(r.status, r.rc, r.stats)
for ev in r.events: ...
```

## Gotchas
- Only a single ssh key can be provided through `env/ssh_key`.
- `idle_timeout` ends runs that produce no output for that long; raise it for long silent tasks.
- The path-based isolation settings (`process_isolation_hide_paths`, `_show_paths`, `_ro_paths`) apply only to bubblewrap, not to container engines.

## Verify
- [ ] `artifacts/<ident>/status` reports success and `job_events/` contains per-task JSON.

## Checked
Checked 2026-10-23 against the ansible-runner documentation on GitHub (docs/intro.rst, remote_jobs.rst, execution_environments.rst; latest release 2.4.3): the env/ files and their formats, the settings keys and defaults (idle_timeout 600, job_timeout 3600, pexpect_timeout 10, suppress_ansible_output, process_isolation*), the bubblewrap-only scope of the path settings, the transmit | worker | process pipeline, worker `--private-data-dir`/`--delete`, `worker cleanup` options, `process --ident` and the `streamer` argument. Removed the unconfirmed claims about 0700 permissions, mixed-version stream breakage and passphrase handling.
Method: documentation only; no commands were run.
