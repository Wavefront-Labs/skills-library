---
id: computing-software.cloud-infrastructure-engineering.ansible.date-time-and-environment-facts
name: date-time-and-environment-facts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, facts, ansible-date-time, ansible-env, timestamps, env-lookup]
level: practitioner
status: docs-checked
description: "Use ansible_date_time and ansible_env facts correctly: timestamp formats, why they are frozen at gather time, remote vs control-node env, and alternatives like now()."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/facts/system/date_time.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/facts/system/env.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/_internal/_templating/_jinja_plugins.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible_date_time and ansible_env facts

## ansible_date_time
Collected by the `date_time` fact collector **on the managed host** at fact-gathering time:
```yaml
ansible_facts['date_time']['date']        # 2026-10-16 (%Y-%m-%d)
ansible_facts['date_time']['time']        # 14:03:22 (%H:%M:%S)
ansible_facts['date_time']['iso8601']     # 2026-10-16T14:03:22Z   (UTC)
ansible_facts['date_time']['iso8601_basic_short']  # 20261016T140322 (host local time)
ansible_facts['date_time']['epoch']       # string; epoch_int is also provided (also a string)
ansible_facts['date_time']['tz'], ['tz_offset'], ['weekday'], ['hour']
```
Typical: a backup name `db-{{ ansible_facts.date_time.iso8601_basic_short }}.sql.gz`.

Pitfalls:
- **Frozen**: the value is taken when facts are gathered and does not advance during the play; with fact caching it can be old.
  For the current time use the `now()` template function.
- Every host has its own clock and timezone, so a run over many hosts gets different timestamps. For one shared release id use `run_once` + `set_fact` with `now(utc=true)`.
- Not available when facts are not gathered (`gather_facts: false`).

Control-node time instead:
```yaml
release_id: "{{ now(utc=true, fmt='%Y%m%dT%H%M%S') }}"   # now(utc=False, fmt=None): returns a datetime, or a strftime string when fmt is given
```

## ansible_env
The environment variables (`os.environ`) of the fact-gathering process on the managed host, at gather time:
```yaml
ansible_facts['env']['HOME']
ansible_facts['env']['PATH']
ansible_facts['env']['SUDO_USER'] | default('')
```
Pitfalls:
- It is captured once, at fact gathering, so it does not change for later tasks that use a different `become_user`. Look up a specific user's home with `ansible.builtin.getent` (`database: passwd`) instead.

Control node environment (where `ansible-playbook` runs):
```yaml
ci_job: "{{ lookup('ansible.builtin.env', 'CI_JOB_ID', default='local') }}"
```
Setting env vars **for tasks**: the `environment:` keyword, not `ansible_env`.

## Verify
- [ ] The `setup` module with `filter=ansible_date_time` and `filter=ansible_env` shows the values you reference.
- [ ] Timestamps used across hosts come from one `run_once` fact when they must match.

## Checked
Checked 2026-10-26 against ansible-core devel `module_utils/facts/system/date_time.py` (keys and formats, UTC `iso8601`,
string `epoch`/`epoch_int`), `facts/system/env.py` (`os.environ`), `_internal/_templating/_jinja_plugins.py` (`now(utc, fmt)`)
and the `setup` module notes (filter works on first-level keys). Removed unconfirmed claims: `min` subset membership, smart
gathering age, `date +%s` alternative, the `to_datetime('%s')` age expression, login-shell, sudo `env_reset` and
non-interactive PATH statements.
Method: documentation only; no commands were run.
