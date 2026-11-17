---
id: computing-software.systems-network-administration.dns-dhcp.kea-config-structure-and-config-test
name: kea-config-structure-and-config-test
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [kea, kea-dhcp4, kea-config-test, kea-dhcp4-conf, include, config-reload, json]
level: practitioner
status: verified
description: "Structure kea-dhcp4.conf (interfaces, lease DB, subnets, options, logging), split it with includes, validate with kea-dhcp4 -t, and reload safely via config-reload or SIGHUP."
sources:
  - https://kea.readthedocs.io/en/latest/arm/config.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea config structure and config test

## Skeleton
```json
{
"Dhcp4": {
  "interfaces-config": { "interfaces": [ "eth0" ], "dhcp-socket-type": "udp" },
  "control-sockets": [ { "socket-type": "unix", "socket-name": "/run/kea/kea4-ctrl-socket" } ],
  "lease-database": { "type": "memfile", "persist": true, "lfc-interval": 3600 },
  "valid-lifetime": 86400,
  "option-data": [
    { "name": "domain-name-servers", "data": "10.0.0.53, 10.0.0.54" },
    { "name": "domain-name", "data": "corp.example.net" }
  ],
  "subnet4": [
    <?include "/etc/kea/subnets-site1.json"?>
  ],
  "loggers": [ { "name": "kea-dhcp4", "output-options": [ { "output": "/var/log/kea/kea-dhcp4.log" } ], "severity": "INFO" } ]
}
}
```
- `dhcp-socket-type: udp` (instead of raw) when the server only serves relayed clients; raw is
  needed for directly connected clients without an IP yet.
- Kea accepts comments (`//`, `/* */`, `#`) and `<?include "file"?>` directives, which plain JSON
  tools do not; validate with Kea itself.
- `control-sockets` (a list) replaced the single `control-socket` map in Kea 2.7.2, which also added
  HTTP/HTTPS control sockets; `control-socket` is still accepted from 2.7.2 to 3.3.0 and is
  deprecated from 3.3.1. Only one `unix` socket is allowed in the list.
- Subnet `id` must be a unique number greater than zero and below 4294967295. It is not mandatory:
  if omitted Kea numbers subnets from 1 in file order, and those ids are not stable across config
  changes, so set explicit ids (strongly recommended when host reservations live in a database).
- Since Kea 2.7.9, control sockets, lease files and log files may only live in the directories
  chosen at build time (`var/run/kea`, `var/lib/kea`, `var/log/kea` under the install prefix), or
  in the directory named by `KEA_CONTROL_SOCKET_DIR`, `KEA_DHCP_DATA_DIR` or `KEA_LOG_FILE_DIR`
  at startup; any other path is refused. Give a bare file name to use the default directory.

## Validate before deploying
```
kea-dhcp4 -t /etc/kea/kea-dhcp4.conf          # parse and sanity-check, exit code 0 = OK, 1 = error
kea-dhcp6 -t /etc/kea/kea-dhcp6.conf
kea-dhcp-ddns -t /etc/kea/kea-dhcp-ddns.conf
```
`-t` is not comprehensive. `-T file` does extra checks: it opens database connections, loads hook
libraries and parses their parameters, but does not open sockets or lock files. Run one of them in
CI and in the deploy script; a bad config prevents the server from starting after a restart.

## Reload without restart
```
echo '{ "command": "config-reload" }' | socat UNIX:/run/kea/kea4-ctrl-socket -,ignoreeof
# or
kill -HUP $(pidof kea-dhcp4)
# or over an HTTP control socket (or the Control Agent, which was removed in Kea 3.1.8)
curl -s -X POST -H 'Content-Type: application/json' -d '{"command":"config-reload"}' http://127.0.0.1:8000/
```
`socat` needs `,ignoreeof` in batch mode so it waits for the reply. With SIGHUP, if the new
configuration is invalid the server keeps its current one (in some cases a fatal error is logged
saying no service is provided until a working config is loaded: check the log).
`config-reload` re-reads the file Kea was started with, so it discards changes made earlier with
`config-set`. The `config-test` command validates a candidate config sent over the API;
`config-get` returns what is running (useful to diff).

## Gotchas
- Changing a subnet's prefix or id with existing leases orphans them; plan renumbering.
- Packaging differs: socket, lease and log directories depend on the build prefix (see the 2.7.9
  note above); keep paths consistent with any HTTP control socket or Control Agent config.

## Verify
- [ ] `kea-dhcp4 -t` passes, `config-reload` returns result 0, and `config-get` shows the new
  subnets.
