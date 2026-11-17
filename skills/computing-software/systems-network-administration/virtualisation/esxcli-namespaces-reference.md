---
id: computing-software.systems-network-administration.virtualisation.esxcli-namespaces-reference
name: esxcli-namespaces-reference
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxcli, esxcli-namespaces, esxcli-network, esxcli-storage, esxcli-system, esxcli-hardware, vim-cmd, esxi-shell, vmware, esxi]
level: practitioner
status: docs-checked
description: "Find your way around esxcli: the network, storage, system, hardware, software and vm namespaces, formatter options for scripts, and when vim-cmd or localcli is needed instead."
sources:
  - https://developer.broadcom.com/xapis/esxcli-command-reference/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esxcli namespaces: a working map

**Goal:** get any host fact or make any host change from the shell quickly, and script it
with parseable output.

## Discover
`esxcli esxcli command list | grep <word>` lists every command; `esxcli <ns> --help` at
any level shows children.

## The namespaces you use weekly
| Namespace | Common commands |
|---|---|
| `network nic` | `list`, `get -n vmnic0` (driver, firmware, link), `stats get -n vmnic0` |
| `network ip interface` | `list`, `ipv4 get`, `tag get -i vmk1` (services on vmk) |
| `network vswitch standard / dvs vmware` | port groups, uplinks, `lacp status get` |
| `network firewall` | `ruleset list`, `ruleset allowedip add` |
| `storage core` | `device list`, `path list`, `adapter rescan --all` |
| `storage nmp / hpp` | path policies |
| `storage vmfs` | `extent list`, `snapshot list` (resignature unresolved volumes), `reclaim config` |
| `storage filesystem` | `list`, `unmount -l <ds>` |
| `system` | `version get`, `maintenanceMode set`, `syslog`, `ntp`, `settings advanced`, `coredump` |
| `hardware` | `cpu list`, `memory get`, `pci list`, `ipmi sel list` |
| `software` | `vib list`, `component list`, `profile get/update` |
| `vm process` | `list`, `kill` |
| `vsan` | `cluster get`, `network list`, `debug object health summary get` |

## Script-friendly output
```sh
esxcli --formatter=csv network nic list
esxcli --formatter=keyvalue system version get
esxcli --formatter=xml storage core device list
```
Remote: `esxcli --server <host> --username root ...` via ESXCLI on a workstation (deprecated
standalone; use PowerCLI `Get-EsxCli -V2` for remote automation).

## When esxcli is not enough
- `vim-cmd` (the hostd CLI) covers VM inventory, host services and host config backup
  where esxcli stops; check its help on the host for the exact subcommands.
- `localcli` bypasses hostd when hostd is hung (support-guided; changes made this way may
  not be reflected in hostd until restart).
- `vmkfstools` for disk files (clone, inflate, lock owner with `-D`).

## Verify
For any change, re-run the matching `get`/`list` command and compare to the intended
value; record commands in the change ticket.

## Checked
2026-10-31: Confirmed the namespace set and the network, storage, system, iscsi, hardware,
software, vm and vsan namespaces against the ESXCLI Command Reference namespace pages,
including `network vswitch dvs vmware lacp status get`, `storage hpp` and the --formatter
options. Genericised the vim-cmd subcommand names (not covered by the ESXCLI reference).
Method: documentation only; no commands were run.
