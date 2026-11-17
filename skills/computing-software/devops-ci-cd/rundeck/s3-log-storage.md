---
id: computing-software.devops-ci-cd.rundeck.s3-log-storage
name: s3-log-storage
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, s3-log-storage, execution-file-storage, aws-credentials, logstore]
level: advanced
status: docs-checked
description: "Store Rundeck execution logs in Amazon S3 or an S3-compatible service with the s3 log plugin: install, credentials, bucket, path and region settings."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/cluster/logstore/s3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install: copy `rundeck-s3-log-plugin-x.y.jar` into `libext/` in the Rundeck installation, then enable the provider in `rundeck-config`:

```properties
rundeck.execution.logs.fileStoragePlugin=org.rundeck.amazon-s3
```

Credentials: by default the AWS credentials provider chain is used (environment variables, Java system properties, credentials file, or EC2 instance profile). Or set `AWSAccessKeyId` with `AWSSecretKey`, or `AWSCredentialsFile`.

Plugin settings: `bucket`; `path` (default `rundeck/project/$PROJECT/logs/$ID`, variables `${job.execid}`, `${job.project}`, `${job.id}`, `${job.group}`, `${job.path}`); `region` (default `us-east-1`); optional `endpoint` and `pathStyle` (default false) for S3-compatible storage; `encodeUserMetadata` (default false).

Prefix the names in `framework.properties` with `framework.plugin.ExecutionFileStorage.org.rundeck.amazon-s3.`, or in `project.properties` with `project.plugin.ExecutionFileStorage.org.rundeck.amazon-s3.`:

```properties
framework.plugin.ExecutionFileStorage.org.rundeck.amazon-s3.bucket=test-rundeck-logs
framework.plugin.ExecutionFileStorage.org.rundeck.amazon-s3.path=logs/${job.project}/${job.execid}.log
```

Gotchas:
- To use `~/.aws/credentials` with role profiles, set none of the three credential properties.
- With a custom SSL truststore, import the S3 certificates into it with `keytool -importcert`.

## Checked

2026-11-04: install step, provider name, credentials chain, property names and defaults, path variables, prefixes, ~/.aws/credentials note and truststore note confirmed against the S3 Log Storage Plugin page. Removed an Enterprise provider name and behaviour the page does not state.
Method: documentation only; no commands were run.
