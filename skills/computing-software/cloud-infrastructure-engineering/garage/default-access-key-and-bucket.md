---
id: computing-software.cloud-infrastructure-engineering.garage.default-access-key-and-bucket
name: default-access-key-and-bucket
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [default-access-key, default-bucket, single-node-flag, environment-variables]
level: intro
status: docs-checked
description: "Bootstrap a Garage test node with an automatic key and bucket using GARAGE_DEFAULT_* variables and the --single-node flags."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Garage v2.3.0 the server can create its own initial credentials, so no manual layout work is needed for a trial. Export three variables before launching:

- `GARAGE_DEFAULT_ACCESS_KEY="GK$(openssl rand -hex 16)"`
- `GARAGE_DEFAULT_SECRET_KEY="$(openssl rand -hex 32)"`
- `GARAGE_DEFAULT_BUCKET="default-bucket"`

You may supply your own key ID and secret instead of random ones. Then start the daemon:

`garage server --single-node --default-bucket`

`--single-node` makes Garage configure a one-node cluster without replication. `--default-bucket` creates the default access key and bucket from the variables, and implies `--default-access-key`.

The Docker equivalent publishes ports 3900 to 3903, mounts the config at `/etc/garage.toml`, passes the three variables with `-e`, uses the `dxflrs/garage` image and runs `/garage server --single-node --default-bucket`. That command creates no volumes, so the cluster is wiped when the container ends. On Linux, `--network host` can replace the four `-p` options. Check with `docker exec garage-container /garage status`.

Versions before v2.3.0 do not have these flags and need the manual layout, bucket and key steps instead.

## Checked

2026-11-04. Read the Quick Start page in full. Confirmed the three variables, the launch command, the meaning of both flags, the Docker command details, the no-volumes warning, the host network option, the status check and the v2.3.0 boundary. Nothing removed.
Method: documentation only; no commands were run.
