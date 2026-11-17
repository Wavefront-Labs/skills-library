---
id: computing-software.networking-hardware-and-wireless.open-vswitch.vsctl-global-options
name: vsctl-global-options
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, no-wait, may-exist, emer-reset, ovs-vsctl, timeout, db, init]
level: practitioner
status: docs-checked
description: "Use ovs-vsctl global options (--db, --no-wait, --timeout, --retry, --format, --bare), the init and emer-reset commands, and the --may-exist and --if-exists idempotency flags."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vsctl global options
Connection and timing:
- `--db=server` selects the OVSDB server; the page's default is `unix:/usr/local/var/run/openvswitch/db.sock`.
- `--no-wait` skips waiting for ovs-vswitchd to reconfigure; use it if ovs-vswitchd is not running, otherwise ovs-vsctl will not exit until it starts. It has no effect if the commands do not change the database. Exit status 65 means the transaction was committed but ovs-vsctl failed while waiting for ovs-vswitchd to reconfigure.
- `--timeout=secs` (`-t`) limits runtime; the default, or 0, waits forever; on expiry ovs-vsctl exits with a SIGALRM signal.
- `--retry` keeps waiting for a database connection; without it, when connecting outward, ovs-vsctl tries once and exits with an error on failure.
- `--no-syslog` stops logging of arguments and changes to the system log; it is equivalent to `--verbose=vsctl:syslog:warn`.
- `--dry-run` prevents ovs-vsctl from modifying the database; `--oneline` prints each command's output on one line.

Output (for `list` and `find`):
- `--format` (`-f`): `table`, `list` (default), `html`, `csv`, `json`.
- `--data` (`-d`): `string` (default), `bare`, `json`.
- `--no-headings`, `--pretty`, `--max-column-width=n`; `--bare` is equivalent to `--format=list --data=bare --no-headings`.

Idempotency: `--may-exist` makes a repeat `add-br`, `add-port` (and `add-bond`) a no-op; `--if-exists` makes deleting or reading something that does not exist a no-op (`del-br`, `del-port`, `get`, `set`, `destroy`).

Resets:
- `ovs-vsctl init` initialises an empty database; no effect if already initialised (any successful ovs-vsctl command also initialises an empty database).
- `ovs-vsctl emer-reset` deconfigures OpenFlow controllers, OVSDB servers and SSL/TLS, deletes port mirroring, fail_mode, NetFlow, sFlow and IPFIX configuration, and removes all other-config keys from all records (except `other-config:hwaddr` on a Bridge record); other networking configuration is left as-is.

## Checked
2026-11-04. Confirmed against ovs-vsctl(8): Options, Table Formatting Options, `init`, `emer-reset`, `--may-exist`/`--if-exists` entries and the Exit status section. Removed "build prefix dependent" for the default socket, and the Verify line about `get-controller` after `emer-reset`.
Method: documentation only; no commands were run.
