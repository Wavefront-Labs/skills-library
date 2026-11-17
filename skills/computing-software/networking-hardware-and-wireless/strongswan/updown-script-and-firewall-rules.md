---
id: computing-software.networking-hardware-and-wireless.strongswan.updown-script-and-firewall-rules
name: updown-script-and-firewall-rules
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, updown, firewall, iptables, hostaccess, pluto-variables]
level: practitioner
status: docs-checked
description: "Run scripts on CHILD SA up and down events with the strongSwan updown plugin: default _updown iptables rules, hostaccess, and the PLUTO environment variables."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/updown.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# updown script and firewall rules
The updown plugin (enabled by default, `--disable-updown` to remove) calls a script when an IKEv2 CHILD SA or IKEv1 Quick Mode SA is established or deleted. The default `_updown` is installed in IPSECDIR (LIBEXECDIR/ipsec by default).

**Default firewall rules.** Pass the absolute path plus the `iptables` argument in the child:

```
updown = /usr/libexec/ipsec/_updown iptables
```

It installs ACCEPT Netfilter rules via iptables for the established traffic selectors, so default DROP policies can be used. If the local traffic selector is not a single host, `hostaccess = yes` also inserts INPUT and OUTPUT rules (besides FORWARD) that allow reaching the VPN server itself. Any other script with arguments can be set instead, to install custom rules or do other work.

**Interface.** The script follows the pluto-compatible interface (version 1.1) and receives environment variables, including: `PLUTO_VERB` (`up-host`, `up-client`, `down-host`, `down-client`; with a `-v6` suffix for IPv6 gateways), `PLUTO_CONNECTION`, `PLUTO_INTERFACE`, `PLUTO_REQID`, `PLUTO_PROTO` (ah or esp), `PLUTO_IPCOMP`, `PLUTO_UNIQUEID`, `PLUTO_ME`, `PLUTO_MY_ID`, `PLUTO_MY_CLIENT`, `PLUTO_MY_SOURCEIP`, `PLUTO_MY_SOURCEIP4_$i`, `PLUTO_MY_SOURCEIP6_$i`, `PLUTO_MY_PROTOCOL`, `PLUTO_MY_PORT`, `PLUTO_PEER`, `PLUTO_PEER_ID`, and matching peer variables.

The script runs per combination of local and remote traffic selectors, so it can be called several times for one CHILD SA. Rekeying a CHILD SA does not invoke the hooks. The vici `child-updown` event fires once per CHILD_SA.

## Checked
2026-11-04. Confirmed against the updown plugin page: enabled by default, `--disable-updown`, IPSECDIR default, the `iptables` argument, `hostaccess`, the PLUTO variables and verbs, and the per-selector invocation. Removed the claim about non-root charon breaking the iptables variant (not on the page).

Method: documentation only; no commands were run.
