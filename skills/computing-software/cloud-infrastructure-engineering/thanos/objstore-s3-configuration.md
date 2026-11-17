---
id: computing-software.cloud-infrastructure-engineering.thanos.objstore-s3-configuration
name: objstore-s3-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-objstore, s3, aws-sdk-auth, signature-version]
level: practitioner
status: docs-checked
description: "Configure the Thanos S3 client for AWS or S3-compatible storage, including signature version and SDK auth."
sources: ["https://thanos.io/tip/thanos/storage.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3 object store configuration

```yaml
type: S3
config:
  bucket: "my-bucket"
  endpoint: "s3.eu-west-1.amazonaws.com"
  region: ""
  access_key: ""
  secret_key: ""
  insecure: false
  signature_version2: false
  put_user_metadata: {}
  list_objects_version: ""
  bucket_lookup_type: auto
  send_content_md5: true
  part_size: 67108864
  sse_config:
    type: ""
prefix: ""
```

The client uses the minio library and works with other S3-compatible stores such as Ceph. At minimum provide `bucket`, `endpoint`, `access_key` and `secret_key`.

With `aws_sdk_auth: true`, Thanos uses the default AWS SDK for Go credential chain (environment variables such as `AWS_PROFILE` and `AWS_WEB_IDENTITY_TOKEN_FILE`, and AWS config files); then only `bucket` and `endpoint` are required.

**Signature.** AWS requires v4, so keep `signature_version2: false`; if omitted wrongly you get Access Denied. Several S3-compatible APIs need `signature_version2: true`.

**Timeouts.** For `timeout awaiting response headers`, increase `http_config.response_header_timeout` (default 2m); `idle_conn_timeout` defaults to 1m30s.

`part_size` (bytes) is the minimum file size for multipart uploads.

## Checked

2026-11-08. Read the S3 section of the raw Thanos docs page behind the cited URL (docs/storage.md, lines 1-142): the config block, required keys, aws_sdk_auth, signature_version2 and Access Denied, http_config timeouts and defaults, part_size, and the minio client note. The S3 server-side encryption, credentials and policy subsections were not read. Nothing removed.

Method: documentation only; no commands were run.
