---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-snapshot-backup
name: consul-snapshot-backup
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-snapshot, snapshot-save, backup]
level: practitioner
status: docs-checked
description: "Save and inspect Consul snapshots with consul snapshot save and inspect, choose consistency mode, and know the Enterprise snapshot agent."
sources: ["https://developer.hashicorp.com/consul/commands/snapshot", "https://developer.hashicorp.com/consul/commands/snapshot/save", "https://developer.hashicorp.com/consul/commands/snapshot/inspect", "https://developer.hashicorp.com/consul/commands/snapshot/agent", "https://developer.hashicorp.com/consul/docs/reference/acl/rule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A snapshot is an atomic, point-in-time copy of server state: key/value entries, service catalog, prepared queries, sessions and ACLs. With ACLs enabled, `snapshot save` needs a management token.

```sh
consul snapshot save backup.snap
consul snapshot save -append-filename version,dc backup.snap   # adds version and datacenter to the name
consul snapshot save -stale backup.snap                        # any server, may be stale
consul snapshot inspect backup.snap
```

- By default the request goes to the leader, which verifies it is still in power before taking the snapshot. The file is read back and verified after writing. `-stale` suits a degraded cluster with no leader; to target a specific server, run the command on that server.
- `inspect` shows ID, Size, Index, Term and Version, plus the size and count of each data type.
- `consul snapshot agent` (Enterprise only) periodically saves snapshots locally or to remote storage, runs as a daemon or one-shot job, and elects a leader among multiple instances.

Gotchas:
- The server writes the snapshot to a temporary file (typically under `/tmp`) before sending it to the CLI and removes it afterwards. Change the location with `TMPDIR` set on the server process, not on the CLI client. Consul also saves one snapshot file at `data_dir/raft/snapshots`.
- The snapshot includes ACL data (token secrets are in it), so restrict access to the files.
- Scheduling and off-host copies are your job in community Consul.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/snapshot (index, save, inspect, agent), and reference/acl/rule (token secrets are contained in the snapshot). Removed: `sha256sum` and cron/systemd advice, the "clear form" and encrypt-at-rest claims (the pages do not say how secrets are stored), and the Verify step.
Method: documentation only; no commands were run.
