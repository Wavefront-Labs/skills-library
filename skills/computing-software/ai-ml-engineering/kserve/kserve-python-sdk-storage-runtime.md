---
id: computing-software.ai-ml-engineering.kserve.kserve-python-sdk-storage-runtime
name: kserve-python-sdk-storage-runtime
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [python-sdk, kserve-storage, storage-class, storage-download, storage-config, storage-override-config, s3-verify-ssl, hdfs, aws-endpoint-url, model-server]
level: practitioner
status: docs-checked
description: "KServe Python runtime SDK (pip install kserve) and the kserve-storage module: Storage.download for gs/s3/azure/http/hdfs/hf/file URIs, env vars, STORAGE_CONFIG overrides."
sources: ["https://github.com/kserve/website/blob/main/docs/reference/python-runtime-sdk/python-runtime-sdk.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Python runtime SDK and kserve-storage

`pip install kserve` (or `uv sync` in the repo's python/kserve) gives a FastAPI-based model-server framework implementing the Open Inference Protocol, V1 and OpenAI protocols, with extensible model server and model APIs, customizable pre-process, predict and post-process handlers, and readiness and liveness handlers. It also encapsulates storage retrieval for models.

## kserve-storage
`pip install kserve-storage` is the module behind the storage initializer. Extracts zip, tar.gz and tgz automatically.
```python
from kserve_storage import Storage
model_dir = Storage.download("gs://your-bucket/model")                 # temp dir
model_dir = Storage.download("s3://your-bucket/model", "/path/to/destination")
Storage.download("hf://org-name/model-name:revision")
```
Schemes: local path or `file://`, `gs://`, `s3://`, `https://<acct>.blob.core.windows.net/...`, `https://<acct>.file.core.windows.net/...`, plain http(s) URLs, `hdfs://`, `webhdfs://`, `hf://`.

## Environment variables
- S3: `AWS_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `AWS_CA_BUNDLE`, `S3_VERIFY_SSL`, `S3_USER_VIRTUAL_BUCKET`, `S3_USE_ACCELERATE`, `awsAnonymousCredential`.
- Azure: `AZURE_STORAGE_ACCESS_KEY`, `AZ_TENANT_ID`, `AZ_CLIENT_ID`, `AZ_CLIENT_SECRET` (also `AZURE_` forms).
- HDFS: `HDFS_SECRET_DIR`, `HDFS_NAMENODE`, `USER_PROXY`, `HDFS_ROOTPATH`, `KERBEROS_PRINCIPAL`, `KERBEROS_KEYTAB`, `TLS_CERT`, `TLS_KEY`, `TLS_CA`, `TLS_SKIP_VERIFY`, `N_THREADS`.
- Hugging Face: handled by the `huggingface_hub` package.
- `STORAGE_CONFIG` (JSON string with storage configuration) and `STORAGE_OVERRIDE_CONFIG` (JSON string that overrides it).

## Checked
Confirmed against the KServe Python Serving Runtime SDK page: install by pip or uv, protocols, handlers, kserve-storage features, supported URI forms, usage snippets and every environment variable listed. Removed the unsupported claim that a control plane client ships in the same package.

Method: docs-only read of cited pages, 2026-11-08
