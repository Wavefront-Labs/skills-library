---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-initiate-terminate-rekey
name: swanctl-initiate-terminate-rekey
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl, initiate, terminate, rekey, install]
level: practitioner
status: docs-checked
description: "Manage strongSwan SAs by hand with swanctl --initiate, --terminate, --rekey (including --reauth) and --install, selecting by name or unique id."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlInitiate.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlTerminate.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlRekey.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlInstall.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl initiate terminate rekey
Assume an IKE SA `home` with CHILD SA `net`.

**Initiate** (`--child`/`-c`, `--ike`/`-i`, `--timeout`/`-t`, `--loglevel`/`-l`):

```
swanctl --initiate --child net     # also creates the parent IKE SA home
swanctl --initiate --ike home      # IKE SA only, no CHILD SA
```

**Terminate** a single CHILD SA or an IKE SA with all its dependent CHILD SAs. Select by name (`--child`, `--ike`) or unique identifier (`--child-id`/`-C`, `--ike-id`/`-I`). `--force` (`-f`) terminates an IKE SA without waiting unless a timeout is set.

```
swanctl --terminate --ike home     # home plus net
swanctl --terminate --child net    # leaves home installed
```

**Rekey** by the same selectors:

```
swanctl --rekey --child net
swanctl --rekey --ike home
swanctl --rekey --ike home --reauth   # reauthenticate an IKEv2 SA from scratch
```

**Install** (`-p`) puts a trap, drop or bypass policy defined by a CHILD SA in place: `swanctl --install --child <name> [--ike <name>]`. `--uninstall` removes it.

All of these accept `--raw` and `--pretty` to dump the response message.

## Checked
2026-11-04. Confirmed against the swanctl --initiate, --terminate, --rekey and --install pages: options with short forms, selectors and examples.

Method: documentation only; no commands were run.
