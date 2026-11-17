---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-runner-python-interface
name: ansible-runner-python-interface
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-runner, runner-python-interface, python-api, event-callbacks]
level: advanced
status: docs-checked
description: "Drive Ansible from Python with ansible_runner.run and run_async: inputs, event and status handlers, cancel callbacks, reading stats, and running inside containers."
sources: ["ansible-runner Python interface (https://github.com/ansible/ansible-runner/blob/devel/docs/python_interface.rst)", "ansible-runner interface source (https://github.com/ansible/ansible-runner/blob/devel/src/ansible_runner/interface.py)", "ansible-runner introduction, job events (https://github.com/ansible/ansible-runner/blob/devel/docs/intro.rst)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible_runner Python interface

The supported way to embed Ansible in Python (the internal `ansible` Python API is not stable).

```python
import ansible_runner

def on_event(ev):
    if ev.get('event') == 'runner_on_failed':
        d = ev['event_data']
        print(f"FAILED {d['host']}: {d['task']}: {d['res'].get('msg')}")
    return True                       # False drops the event from artifacts

def on_status(status, runner_config):
    print('status:', status['status'])

r = ansible_runner.run(
    private_data_dir='/srv/runs/deploy',
    playbook='site.yml',
    inventory={'web': {'hosts': {'web01': {'ansible_host': '10.0.0.11'}}}},
    extravars={'release': 'v1.4.2'},
    limit='web',
    event_handler=on_event,
    status_handler=on_status,
    quiet=True,                        # disable all output
    rotate_artifacts=10,               # keep at most 10 artifact dirs
)
print(r.status, r.rc)                  # 'successful', 0
print(r.stats)                         # {'ok': {...}, 'changed': {...}, 'failures': {...}, ...}
for ev in r.events:                    # generator reading job_events from disk; live tail while the run is active
    pass
```

## Async and cancel
```python
thread, runner = ansible_runner.run_async(private_data_dir=pdd, playbook='long.yml')
# cancel_callback=lambda: should_stop  -> called each loop iteration; True cancels the Ansible process
thread.join()
```

## Other entry points
- `ansible_runner.run_command(executable_cmd='ansible-galaxy', cmdline_args=['collection','list'])` (returns output, error, rc; `run_command_async` is the asynchronous form)
- `ansible_runner.get_inventory(action='list', inventories=['inv/'])`
- `ansible_runner.get_plugin_docs(...)`, `get_ansible_config(action='dump')`, `get_role_list(...)`, `get_role_argspec(...)`
- Container execution: `process_isolation=True, container_image='my-execution-environment:latest'` (podman is the default engine).
- `streamer='transmit'`, `'worker'` or `'process'` runs one stage of the remote-job pipeline.

## Gotchas
- Inputs such as `envvars`, `extravars`, `passwords`, `settings` and `ssh_key` are also written to the private data dir's `env/` files unless `suppress_env_files=True`; use a separate private data dir per concurrent run.
- `event_handler` returns `True` to keep an event and anything else drops it.
- Status values passed to `status_handler`: `starting`, `running`, `canceled`, `timeout`, `failed`, `successful`.

## Verify
- [ ] The script exits with `r.rc` and logs failed hosts from events.

## Checked
Checked 2026-10-23 against the ansible-runner documentation and interface.py on GitHub (latest release 2.4.3): the `run()` parameter list (inventory as dict, extravars, limit, quiet, rotate_artifacts, event_handler, status_handler, cancel_callback, suppress_env_files, process_isolation, container_image, streamer), `run_async`, `run_command(_async)`, `get_inventory`, `get_plugin_docs`, `get_ansible_config`, `get_role_list`, `get_role_argspec`, the `Runner.events` generator semantics, `stats`, `host_events`, `get_fact_cache` and the status handler values. Removed `tags=` (not a documented `run()` argument) and the unconfirmed thread-context claim.
Method: documentation only; no commands were run.
