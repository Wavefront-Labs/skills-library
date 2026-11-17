---
id: computing-software.cybersecurity-defensive.wazuh.remote-connection-settings
name: remote-connection-settings
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [remote, queue-size, rids-closing-time, connection-overtake-time, allowed-ips, denied-ips]
level: advanced
status: docs-checked
description: "Wazuh manager remote block: connection type, port and protocol defaults, queue_size, rids_closing_time, connection_overtake_time, IP filters."
sources:
  - https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/remote.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `<remote>` section configures how the manager listens for agent and syslog events.

- `connection`: `secure` or `syslog`. Default `secure`.
- `port`: default 1514 for secure and 514 for syslog; range 1 to 65535.
- `protocol`: `udp` or `tcp`, default `tcp`. Secure connections can use both, comma separated; syslog allows one protocol per block.
- `allowed-ips`: IPs or networks permitted to send syslog. No default, and at least one is required for the syslog connection type.
- `denied-ips`: IPs or networks barred from sending syslog. No default.
- `queue_size`: remote daemon queue capacity in agent events. Default 131072, range 1 to 262144, secure connections only.
- `rids_closing_time`: how long an agent can be silent before its RIDS files close. Default `5m`; needs a number with suffix s, m, h or d.
- `connection_overtake_time`: how long to wait before treating an older TCP connection as down when a new one arrives with the same key. Default 60 seconds, range 0 to 3600, and 0 disables the check.

- `local_ip`: local IP address to listen on; default all interfaces.
- `ipv6`: enables IPv6 support; default `no`.
- `agents` > `allow_higher_versions`: accept agents newer than the manager; default `no`, secure connections only.

Gotchas:
- At least one `allowed-ips` address is required with the syslog connection type.
- `queue_size` covers agent events only, not syslog events.
- `connection_overtake_time` must be higher than the agent notify-time and does not apply to UDP clients.

## Checked

2026-11-08: confirmed against the Wazuh ossec.conf remote reference page (read in full): all options, defaults, ranges and notes above, including the example configuration. Removed the unsupported memory-cost claim about queue_size and the remark about a missing option.
Method: documentation only; no commands were run.
