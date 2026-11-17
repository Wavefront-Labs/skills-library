---
id: computing-software.messaging-and-integration.celery.celery-cloud-object-store-backends
name: celery-cloud-object-store-backends
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-other-backends, celery, s3, azure-blob, gcs, dynamodb, result-backend, object-store]
level: practitioner
status: docs-checked
description: "Configure Celery result backends for S3, Azure Block Blob, Google Cloud Storage and DynamoDB with exact setting names and defaults."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3, Azure Blob, GCS and DynamoDB result backends

Goal: store results in a cloud service.

## S3 (`pip install celery[s3]`)
Settings (all default None): `s3_access_key_id`, `s3_secret_access_key`, `s3_bucket`, `s3_base_path` (e.g. `'/prefix'`), `s3_endpoint_url` (for self-hosted S3-compatible stores such as Ceph or Scality), `s3_region` (e.g. `'us-east-1'`).

```python
s3_access_key_id = 's3-access-key-id'
s3_secret_access_key = 's3-secret-access-key'
s3_bucket = 'mybucket'
s3_base_path = '/celery_result_backend'
s3_endpoint_url = 'https://endpoint_url'
```

## Azure Block Blob
URL is `azureblockblob://` followed by the storage connection string (Azure Portal, Access Keys pane):
`result_backend = 'azureblockblob://DefaultEndpointsProtocol=https;AccountName=somename;AccountKey=...;EndpointSuffix=core.windows.net'`

`azureblockblob_container_name` (default `celery`), `azureblockblob_base_path` (5.1+, e.g. `'prefix/'`), `azureblockblob_retry_initial_backoff_sec` (2; later retries exponential), `azureblockblob_retry_increment_base` (2), `azureblockblob_retry_max_attempts` (3), `azureblockblob_connection_timeout` (20 s), `azureblockblob_read_timeout` (120 s).

## GCS (`pip install celery[gcs]`; needs google-cloud-storage and google-cloud-firestore)
URL form: `result_backend = 'gs://mybucket/some-prefix?gcs_project=myproject&ttl=600'`. Settings: `gcs_bucket`, `gcs_project`, `gcs_base_path` (default None), `gcs_ttl` (default 0; needs a bucket with the Delete Object Lifecycle Management action; e.g. `86400`), `gcs_threadpool_maxsize` (default 10, also the connection pool size), `firestore_project` (default `gcs_project`; used for chord reference counting).

## DynamoDB (`pip install celery[dynamodb]`, needs boto3)
URL: `dynamodb://aws_access_key_id:aws_secret_access_key@region:port/table?read=n&write=m`
```python
result_backend = 'dynamodb://@us-east-1/celery_results'
result_backend = 'dynamodb://@/?read=5&write=5'     # default table celery
result_backend = 'dynamodb://@localhost:8000'        # downloadable DynamoDB
result_backend = 'dynamodb://@us-east-1'
dynamodb_endpoint_url = 'http://192.168.0.40:8000'
```
- Credentials can also be resolved by boto3. `port` has no effect unless region is `localhost`.
- Table default `celery`; read/write capacity units default 1.
- `ttl_seconds`: unset leaves table TTL untouched; positive expires results; negative means never expire and actively disables the table TTL. Changing a table TTL repeatedly in quick succession causes a throttling error.
- Warning: tables with a sort key are not supported; use a global secondary index to query by other fields.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
