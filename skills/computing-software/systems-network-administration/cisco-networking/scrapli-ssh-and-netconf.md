---
id: computing-software.systems-network-administration.cisco-networking.scrapli-ssh-and-netconf
name: scrapli-ssh-and-netconf
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, scrapli, scrapli-netconf, python, network-automation, ssh-automation, asyncio, cisco-iosxe-driver, genie-parsing]
level: practitioner
status: draft
description: "Automate Cisco devices with Scrapli: IOSXEDriver send_command/send_configs, system vs asyncssh transports, structured parsing, and scrapli-netconf."
sources:
  - https://carlmontanari.github.io/scrapli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scrapli for fast SSH and NETCONF

## Why Scrapli
Fast SSH/telnet automation with sync and asyncio APIs, platform drivers that handle privilege
levels and prompts, and pluggable transports (system OpenSSH, paramiko, ssh2, asyncssh).
Often several times faster than Netmiko for bulk commands.

## Basic use
```
pip install scrapli scrapli-netconf "scrapli[genie]" "scrapli[textfsm]"
```
```python
from scrapli.driver.core import IOSXEDriver
dev = {"host": "10.0.0.1", "auth_username": "<USER>", "auth_password": "<PW>",
       "auth_strict_key": False, "transport": "system"}
with IOSXEDriver(**dev) as conn:
    r = conn.send_command("show version")
    print(r.result)
    print(r.genie_parse_output())            # or r.textfsm_parse_output()
    rs = conn.send_configs(["interface Loopback99", "description scrapli-test"])
    print(rs.failed)
    conn.send_command("write memory")
```
Core drivers: `IOSXEDriver`, `NXOSDriver`, `IOSXRDriver`, `EOSDriver`, `JunosDriver`; others via
`scrapli_community`.

## Async for many devices
```python
import asyncio
from scrapli.driver.core import AsyncIOSXEDriver
async def run(host):
    async with AsyncIOSXEDriver(host=host, auth_username="<USER>", auth_password="<PW>",
                                auth_strict_key=False, transport="asyncssh") as c:
        return (await c.send_command("show ip int brief")).result
print(asyncio.run(asyncio.gather(*(run(h) for h in ["10.0.0.1", "10.0.0.2"]))))
```

## NETCONF
```python
from scrapli_netconf.driver import NetconfDriver
with NetconfDriver(host="10.0.0.1", auth_username="<USER>", auth_password="<PW>",
                   auth_strict_key=False, port=830) as nc:
    r = nc.get_config(source="running", filter_="<native xmlns='http://cisco.com/ns/yang/Cisco-IOS-XE-native'><hostname/></native>")
    print(r.result)
```

## Gotchas
- `send_configs` returns a MultiResponse; check `.failed`; IOS errors like `% Invalid input` are
  detected via failed_when_contains defaults.
- `auth_strict_key=False` is for labs; supply known_hosts in production.
- Long-running commands: raise `timeout_ops`.

## Verify
- [ ] Bulk show job over the estate completes with no failed responses; configs saved.
