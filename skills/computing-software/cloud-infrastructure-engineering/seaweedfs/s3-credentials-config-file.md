---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-credentials-config-file
name: s3-credentials-config-file
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [s3-config, identities, sighup-reload, credentials]
level: practitioner
status: docs-checked
description: "Configure S3 access keys with a JSON identities file (-s3.config), filer-stored or Admin UI users, env-var fallback, and reload without restart."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Credentials
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 credentials config file

Two config systems exist: `-s3.config` (access-key identities) and `-s3.iam.config` (OIDC/STS, see the OIDC skill). `-s3.iam.config` does not accept `identities`.

Priority: config file, then filer-stored config (Admin UI users are stored there too, same priority), then env vars as fallback. A higher method completely overrides lower ones; there is no merging.

```json
{"identities":[
 {"name":"admin_user","credentials":[{"accessKey":"AK","secretKey":"SK"}],"actions":["Admin","Read","Write","List","Tagging"]},
 {"name":"read_only_user","credentials":[{"accessKey":"AK2","secretKey":"SK2"}],"actions":["Read"]}
]}
```
```bash
weed s3 -config=/path/to/s3.json -filer=localhost:8888
weed server -s3 -s3.config=/path/to/s3.json
```
Admin UI: `weed admin -masters=localhost:9333`, then Object Store, Users (port 12535). Env fallback: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (used only when nothing else is configured).

Reload: send SIGHUP (for example `systemctl reload`) when using `-config`; filer-based configs reload automatically. Manage with `s3.configure` in `weed shell`.

With no credentials configured the gateway is in Allow-All mode (the default for `weed mini` and `weed s3`). Adding the first identity switches it to authentication-required, permanently, even if credentials are later removed. Zero-config `weed s3` also defaults to effect Allow (open access) with policies held in memory, so define credentials before exposing it.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages S3 Credentials (priority, SIGHUP reload table, port 12535, Object Store Users, Allow-All and one-way switch) and S3 Configuration (zero-config STS, default effect Allow, in-memory policies). Fixed `weed admin -master` to `-masters`; removed the unconfirmed `weed mini -s3.config` line.
Method: documentation only; no commands were run.
