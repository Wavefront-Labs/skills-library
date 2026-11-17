---
id: computing-software.devops-ci-cd.spinnaker.storage-backends-overview
name: storage-backends-overview
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [storage, front50, s3, gcs, azure-storage, minio, redis, hal-config-storage]
level: practitioner
status: draft
description: "Choose Spinnaker's persistent storage for applications and pipelines: supported backends, why Redis is unsupported for production, and that storage is independent of the cloud provider."
sources:
  - https://spinnaker.io/docs/setup/install/storage/
  - https://github.com/spinnaker/spinnaker.github.io/blob/master/setup/install/storage/redis.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Spinnaker needs an external storage provider to persist application settings and configured pipelines. The data is sensitive and costly to lose, so the page recommends a hosted store you trust.

**Supported options:** Azure Storage, Google Cloud Storage, Minio, S3, Oracle Object Storage, and Redis. The choice does not constrain your cloud provider: you can store in GCS and deploy to Azure.

**Redis is the exception.** The Redis page says it is unsupported and not recommended for production, calls the implementation untested and unsupported by the community, and recommends Minio for a local persistent store. The stated reason: Redis would mix short-lived cache entries with the pipeline and application data that deploys your infrastructure, so clearing the cache becomes risky. Halyard can currently only use the Redis instance it provisions itself; configure it with:

```bash
hal config storage edit --type redis
```

Each backend is configured under `hal config storage` (see the S3 skill for the S3 flow). After storage is configured the next step is `hal deploy apply`.

If you change storage later, nothing migrates data for you; the configuration page states that migration is your job. Section: Front50 can also use SQL instead of an object store (separate skill).

## Checked

2026-11-04. Backend list, provider independence and Redis warnings were confirmed on the About External Storage and Redis storage pages. The migration note comes from the Configuration page.

Method: documentation only; no commands were run.
