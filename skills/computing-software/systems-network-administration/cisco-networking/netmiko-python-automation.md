---
id: computing-software.systems-network-administration.cisco-networking.netmiko-python-automation
name: netmiko-python-automation
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, network-automation, netmiko, python, ssh-automation, textfsm, ntc-templates, send-command, send-config-set, connecthandler, concurrent-futures, config-push, show-command-parsing]
level: practitioner
status: draft
description: "Script Cisco CLI over SSH with Netmiko: connecting, parsing show output with TextFSM, pushing config sets safely, running across many devices concurrently and handling failures."
sources:
  - https://github.com/ktbyers/netmiko
  - https://github.com/networktocode/ntc-templates
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Python automation with Netmiko

Netmiko wraps Paramiko SSH with per-platform prompt handling. Use it for devices without
APIs or quick fleet-wide show/config jobs.

## Connect and run
```python
from netmiko import ConnectHandler
dev = {"device_type": "cisco_ios", "host": "10.0.0.5", "username": "netops",
       "password": os.environ["NET_PASS"], "secret": os.environ.get("ENABLE_PASS", ""),
       "fast_cli": False}
with ConnectHandler(**dev) as conn:
    conn.enable()
    out = conn.send_command("show ip interface brief", use_textfsm=True)   # list of dicts
    for i in out:
        if i["status"] == "up" and i["proto"] != "up":
            print(i["interface"])
```
`use_textfsm=True` uses ntc-templates (pip install ntc-templates). Without a template you get
raw text. device_type examples: `cisco_ios`, `cisco_xe`, `cisco_nxos`, `cisco_asa`, `arista_eos`,
`juniper_junos`.

## Push config
```python
cmds = ["ntp server 10.0.0.11", "ntp server 10.0.0.12"]
with ConnectHandler(**dev) as conn:
    out = conn.send_config_set(cmds, cmd_verify=True)
    if "% Invalid" in out or "% Incomplete" in out:
        raise RuntimeError(out)
    conn.save_config()
```
For files: `send_config_from_file("ntp.txt")`. Long-running commands: `send_command(...,
read_timeout=300)`; interactive prompts: `send_command_timing` or `expect_string=r"confirm"`.

## Many devices
```python
from concurrent.futures import ThreadPoolExecutor
def job(host):
    try:
        with ConnectHandler(**{**dev, "host": host}) as c:
            return host, c.send_command("show version | i uptime")
    except Exception as e:
        return host, f"FAILED {type(e).__name__}: {e}"
with ThreadPoolExecutor(max_workers=20) as ex:
    for host, res in ex.map(job, hosts):
        print(host, res)
```
Keep workers moderate (TACACS servers and VTY line limits). Record failures; never let one bad
device stop the run.

## Safety
- Dry-run first: print the commands per device; diff the intended state.
- Check pre-conditions with a show before changing (e.g. interface exists, is not a trunk).
- Use `reload in` / revert timers on changes that can cut management access.
- Credentials from environment/vault, never in the script; set `session_log` only to a
  protected path (it captures passwords typed).

## Verify
- [ ] Script reports per-device success/failure; failures are retried or listed.
- [ ] Post-change show (parsed) confirms the state on every device.
