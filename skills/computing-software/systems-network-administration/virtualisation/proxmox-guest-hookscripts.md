---
id: computing-software.systems-network-administration.virtualisation.proxmox-guest-hookscripts
name: proxmox-guest-hookscripts
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hookscript, qm, pct, proxmox, automation]
level: advanced
status: docs-checked
description: "Attach hookscripts to Proxmox VE VMs and containers to run actions at pre-start, post-start, pre-stop and post-stop, with snippet storage and failure behaviour."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#qm_hookscripts
  - https://github.com/proxmox/pve-docs/blob/master/examples/guest-example-hookscript.pl
  - https://github.com/proxmox/pve-docs/blob/master/qm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guest hookscripts

**Goal:** run host-side actions automatically when a guest starts or stops (bind a GPU, set CPU affinity, notify monitoring, mount something).

## Setup
1. Enable `snippets` content on a directory-based storage (for example `local`: Datacenter -> Storage -> local -> Content); scripts live in that storage's `snippets/` folder.
2. Create an executable script there:
```bash
cat > <storage-path>/snippets/hook.sh <<'EOF'
#!/bin/bash
vmid="$1"; phase="$2"
case "$phase" in
  pre-start)  logger -t hook "$vmid starting" ;;
  post-start) logger -t hook "$vmid started" ;;
  pre-stop)   logger -t hook "$vmid will be stopped" ;;
  post-stop)  logger -t hook "$vmid stopped" ;;
esac
exit 0
EOF
chmod +x <storage-path>/snippets/hook.sh
```
3. Attach:
```bash
qm set 110 --hookscript local:snippets/hook.sh
pct set 210 --hookscript local:snippets/hook.sh
```
A Perl example ships at `/usr/share/pve-docs/examples/guest-example-hookscript.pl`.

## Behaviour
- Arguments: first the VMID, second the phase (`pre-start`, `post-start`, `pre-stop`, `post-stop`).
- Exiting with a non-zero code in `pre-start` aborts the start.
- `post-start` runs after the guest started successfully.
- `pre-stop` runs before the guest is stopped via the API; it does not run when the guest is stopped from inside (for example `poweroff`).
- `post-stop` runs after the guest stopped and should also run if the guest crashes or stops unexpectedly.
- The script file must be reachable at the volume ID on every node that may run the guest (shared storage or a copy on each node).

## Gotchas
- Keep scripts quick; a slow `pre-start` delays the guest start.
- Use the example script as the reference for the phase semantics; an unknown phase should be handled explicitly (the example dies on it).

## Verify
Start and stop the guest and check `journalctl -t hook` for the expected messages.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc and pct.adoc Hookscripts sections, plus examples/guest-example-hookscript.pl) and confirmed the hookscript option syntax for qm and pct, the argument order, the four phases and their documented semantics (pre-start non-zero aborts, pre-stop not run for in-guest poweroff, post-stop also after a crash). Removed the unconfirmed CPU governor and taskset example, the task-log, root and restore claims; fixed the logger tag so the journalctl -t check works.

Method: documentation only; no commands were run.
