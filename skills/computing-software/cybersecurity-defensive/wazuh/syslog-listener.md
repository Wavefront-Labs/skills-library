---
id: computing-software.cybersecurity-defensive.wazuh.syslog-listener
name: syslog-listener
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [syslog, remote, allowed-ips, local-ip, connection-syslog, port-514]
level: practitioner
status: docs-checked
description: "Receive syslog from network devices on the Wazuh server with a remote block of connection syslog, including the mandatory allowed-ips setting."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/syslog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Wazuh server can receive syslog directly. Add a `<remote>` block inside `<ossec_config>` in `/var/ossec/etc/ossec.conf`:

```xml
<remote>
  <connection>syslog</connection>
  <port>514</port>
  <protocol>tcp</protocol>
  <allowed-ips>192.168.2.0/24</allowed-ips>
  <local_ip>192.168.2.10</local_ip>
</remote>
```

Fields:
- `<connection>`: `secure` or `syslog`.
- `<port>`: port for incoming syslog messages.
- `<protocol>`: `tcp` or `udp`.
- `<allowed-ips>`: IP address or network range of the forwarding devices.
- `<local_ip>`: the server IP that listens for messages.

Apply with `systemctl restart wazuh-manager`.

Failure mode: the page states the `allowed-ips` label is mandatory and the configuration will not take effect without it.
Tip from the page: if you already run a central logging server such as Syslog or Logstash, install the Wazuh agent on it to streamline log collection and forward from there to the Wazuh server.

## Checked

2026-11-08: confirmed against the Wazuh docs page Configuring syslog on the Wazuh server (read in full): the remote block, field meanings, tcp/udp and secure/syslog values, restart command, mandatory allowed-ips and the central logging tip. Removed the claims about the default port and one protocol per block, which came from an uncited reference page.
Method: documentation only; no commands were run.
