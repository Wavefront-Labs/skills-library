---
id: computing-software.devops-ci-cd.spinnaker.s3-storage-setup
name: s3-storage-setup
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [storage, s3, aws, hal-config-storage, front50, minio]
level: practitioner
status: docs-checked
description: "Configure S3 as Spinnaker persistent storage with hal config storage s3 edit, including bucket creation behavior, IAM s3 permissions, and secret key entry via stdin."
sources:
  - https://github.com/spinnaker/spinnaker.github.io/blob/master/setup/install/storage/s3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Using S3 means Spinnaker stores all its persistent data in one bucket.

**Prerequisites:** an AWS account and a role or user with `s3` permissions. Both the user and role policies must grant `s3:*`. On EC2, the instance profile of the instance running Spinnaker needs these permissions. Elsewhere (for example inside Kubernetes) you need the access key id and secret access key of a user with `s3` permissions.

**Configure:**

```bash
hal config storage s3 edit \
    --access-key-id $YOUR_ACCESS_KEY_ID \
    --secret-access-key \
    --region $REGION
```

Do not put the secret on the command line: with `--secret-access-key` and no value, Halyard prompts for it on standard input. Then select S3 as the active source:

```bash
hal config storage edit --type s3
```

**Bucket behavior:** if you have no bucket, Halyard creates one, named with `--bucket` if you passed it or otherwise `spin-<uuid>`. You must supply the region (the page uses `us-west-2` as the example). To use an existing bucket or change the root folder, see the additional parameters of `hal config storage s3 edit` in the command reference.

The page also notes Minio as an S3-API-compatible local alternative. Once S3 is set as the storage source you are ready to deploy Spinnaker.

This page comes from the archived (2021) spinnaker.github.io repository; the current docs have moved to SQL databases, so check that the Halyard flow still matches your version.

## Checked

Method: docs-checked 2026-11-09 against the full archived spinnaker.github.io s3.md page. Confirmed permissions, command flags, stdin secret entry, bucket naming and the Minio note. Removed the named `hal deploy apply` step, which that page does not state.
