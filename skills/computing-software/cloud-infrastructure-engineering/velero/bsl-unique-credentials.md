---
id: computing-software.cloud-infrastructure-engineering.velero.bsl-unique-credentials
name: bsl-unique-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [bsl-credential, credential-secret, multiple-credentials, kubectl-create-secret, backup-location-create]
level: advanced
status: docs-checked
description: "Give a BackupStorageLocation its own credentials Secret using --credential=secret=key, and check the Available phase."
sources:
  - https://velero.io/docs/main/locations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Additional BackupStorageLocations can use their own credentials, to write to another provider or another account. Without it, Velero uses the credentials from install time in the `cloud-credentials` secret.

Prerequisites: the object storage provider plugin must support per-location credentials (all plugins maintained by the Velero team do; check third-party plugins), the plugin must be installed, and you need a credentials file in the format that plugin documents.

1. Create a Secret in the Velero namespace:

```shell
kubectl create secret generic -n velero credentials --from-file=bsl=</path/to/credentialsfile>
```

This makes a secret named `credentials` with one key, `bsl`, holding the file contents.

2. Create the location, passing secret name and key to `--credential`:

```bash
velero backup-location create <bsl-name> \
  --provider <provider> \
  --bucket <bucket> \
  --config region=<region> \
  --credential=<secret-name>=<key-within-secret>
```

Velero fetches the data from that key whenever it uses the location.

The location is ready when its phase is `Available`; check it with `velero backup-location get`.

The same multi-credential support applies to `VolumeSnapshotLocations`, again only if the plugin supports it.

## Checked

2026-11-08. Read in full: the Backup Storage Locations and Volume Snapshot Locations page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
