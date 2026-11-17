---
id: computing-software.data-engineering.polars.io-cloud-credentials-and-retries
name: io-cloud-credentials-and-retries
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, cloud-storage, storage-options, credential-provider, aws, azure, polars-io-cloud, retries]
level: practitioner
status: docs-checked
description: "Authenticate Polars cloud scans with storage_options, CredentialProviderAWS/Azure, custom credential functions or a global default, and tune retry settings."
sources:
  - https://docs.pola.rs/user-guide/io/cloud-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate Polars to cloud storage when default credential loading does not work, and tune retries.

Polars automatically loads default credential configurations for some providers. Otherwise use one of:

1. `storage_options` dict
```python
storage_options = {
    "aws_access_key_id": "<secret>",
    "aws_secret_access_key": "<secret>",
    "aws_region": "us-east-1",
}
pl.scan_parquet("s3://bucket/*.parquet", storage_options=storage_options).collect()
```

2. A `pl.CredentialProvider*` class, e.g. AWS profile and IAM role assumption
```python
lf = pl.scan_parquet(
    "s3://.../...",
    credential_provider=pl.CredentialProviderAWS(
        profile_name="...",
        assume_role={"RoleArn": "...", "RoleSessionName": "..."},
    ),
)
```

3. A custom function returning `(credentials_dict, expiry)` (e.g. for AWS IAM role-chaining)
```python
def get_credentials() -> pl.CredentialProviderFunctionReturn:
    expiry = None
    return {"aws_access_key_id": "...", "aws_secret_access_key": "...", "aws_session_token": "..."}, expiry

pl.scan_parquet("s3://.../...", credential_provider=get_credentials)
```
The Azure variant returns `{"bearer_token": token.token}, token.expires_on`; a shortcut for `abfss://` paths is
`credential_provider=pl.CredentialProviderAzure(credential=DefaultAzureCredential(exclude_managed_identity_credential=True))`.

4. Global default, so it need not be passed to every I/O call
```python
pl.Config.set_default_credential_provider(pl.CredentialProviderAWS(profile_name="...", assume_role={...}))
```

Retry configuration via `storage_options` (keys shown on the page; the values are example numbers):
```python
storage_options={
    "max_retries": 3,
    "retry_timeout_ms": 9873,
    "retry_init_backoff_ms": 9874,
    "retry_max_backoff_ms": 9875,
    "retry_base_multiplier": 3.14159,
}
```

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
