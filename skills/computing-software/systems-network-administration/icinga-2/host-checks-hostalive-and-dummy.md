---
id: computing-software.systems-network-administration.icinga-2.host-checks-hostalive-and-dummy
name: host-checks-hostalive-and-dummy
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, hostalive, dummy, host-object, check-command, icmp, services]
level: intro
status: docs-checked
description: Define Icinga 2 Host and Service objects, use hostalive, ping and icmp host checks, and the dummy CheckCommand for unreachable hosts.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# host checks: hostalive and dummy
A Host object groups services running on the same device. Services reference it by `host_name`:
```
object Host "my-server1" {
  address = "10.0.0.1"
  check_command = "hostalive"
}
object Service "http" {
  host_name = "my-server1"
  check_command = "http"
}
```
The `address` attribute tells check commands which network address belongs to the host.

`hostalive` is a built-in check command that sends ICMP echo requests to `address`. It is the same as `ping` with different default thresholds; both use the `ping` CLI command for sequential checks. For faster ICMP checks, look at the `icmp` CheckCommand.

If the host is not reachable by ICMP or HTTP, use `dummy` to set a fixed state:
```
object Host "dummy-host" {
  check_command = "dummy"
  vars.dummy_state = 0 //Up
  vars.dummy_text = "Everything OK."
}
```
The same method is used when you send external (passive) check results. A more advanced technique is to compute the host state from all its services (see the advanced topics chapter on accessing object attributes at runtime).

Troubleshooting check problems is covered in the troubleshooting chapter.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Hosts and Services, Host and Service Checks and Host Check Alternatives sections of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page). Confirmed the host and service example, the address attribute, hostalive sending ICMP echo requests, the hostalive versus ping tip and the icmp pointer, the dummy example, the external check results note, and the pointers to the runtime-attributes and troubleshooting chapters. Nothing was removed. No commands were run.
