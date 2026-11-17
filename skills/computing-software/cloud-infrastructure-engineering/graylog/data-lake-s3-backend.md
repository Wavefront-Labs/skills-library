---
id: computing-software.cloud-infrastructure-engineering.graylog.data-lake-s3-backend
name: data-lake-s3-backend
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [lake-backend, s3-backend, data-lake-journal, object-storage, data-lake]
level: advanced
status: docs-checked
description: "Create an S3 Data Lake backend (Amazon S3, OVH or SysEleven only) and review journal limits before use."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/create_data_lake_backend_on_amazon_s3.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# data lake s3 backend

Amazon S3, OVH Object Storage and SysEleven Object Storage are the only supported S3-compatible backends for a Data Lake. GCS, Azure Blob Storage and local network storage are also available.

Graylog strongly recommends third-party object storage. On a local file store, reaching capacity forces a backend switch.

Before creating the backend, review `data_lake_journal_max_size` and `data_lake_journal_max_age`. Changing them after use can require extra storage or partitions.

Steps: **Data Lake > Internal Data Lake > Backend tab > Create Data Lake Backend**, choose Backend Type S3, then supply Title, Description, optional S3 Endpoint URL and the bucket details and credentials. You need an existing bucket and credentials, and administrator rights.

## Checked

2026-11-04. Confirmed against the Data Lake pages. Nothing removed.

Method: documentation only; no commands were run.
