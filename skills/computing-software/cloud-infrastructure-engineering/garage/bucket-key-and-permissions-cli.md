---
id: computing-software.cloud-infrastructure-engineering.garage.bucket-key-and-permissions-cli
name: bucket-key-and-permissions-cli
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-bucket-create, garage-key-create, bucket-allow, api-keys]
level: intro
status: docs-checked
description: "Create a bucket and an API key, then grant read, write and owner permissions with garage bucket allow."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
  - https://garagehq.deuxfleurs.fr/documentation/cookbook/exposing-websites/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Buckets and keys are separate objects in Garage. A key can access many buckets and a bucket can be accessed by many keys, so nothing is usable until you link them.

The guide's example prepares storage for NextCloud:

1. `garage bucket create nextcloud-bucket`
2. `garage bucket list` and `garage bucket info nextcloud-bucket` to confirm it exists.
3. `garage key create nextcloud-app-key`. The output shows the key name, a key ID beginning with `GK`, and the secret key.
4. `garage key list` and `garage key info nextcloud-app-key` to check the key.
5. Grant access:

`garage bucket allow --read --write --owner nextcloud-bucket --key nextcloud-app-key`

The `--owner` bit matters later: the website guide notes that the `PutBucketWebsite` S3 call is allowed for keys that have the owner permission.

Use `garage bucket info nextcloud-bucket` at any time to see which keys are allowed on it. A new key shows an empty "Authorized buckets" list until you run the allow command.

## Checked

2026-11-04. Read the Quick Start page in full and the website page for the owner rule. Confirmed every command, the key output fields and the independence of keys and buckets. Removed the closing sentence about S3 clients, which the page does not state in that form.
Method: documentation only; no commands were run.
