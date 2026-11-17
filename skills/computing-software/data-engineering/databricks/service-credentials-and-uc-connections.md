---
id: computing-software.data-engineering.databricks.service-credentials-and-uc-connections
name: service-credentials-and-uc-connections
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, service-credentials, uc-connections, unity-catalog, secrets]
level: advanced
status: docs-checked
description: "Access external cloud services and databases from Databricks via Unity Catalog service credentials and connections instead of keys in code or instance profiles."
sources:
  - https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-services/service-credentials
  - https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-services/use-service-credentials
  - https://docs.databricks.com/aws/en/query-federation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service credentials and UC connections

**Goal:** governed, auditable access to cloud services (SQS, Secrets Manager, Pub/Sub, external APIs) and databases, granted per principal in Unity Catalog.

## Service credentials (cloud service APIs)
Create in Catalog Explorer (External data > Credentials > Service credential) with an IAM role / managed identity / GCP service account, then grant:
```sql
GRANT ACCESS ON SERVICE CREDENTIAL `sqs-orders` TO `etl-sp`;
```
Use in Python (AWS example):
```python
import boto3
session = boto3.Session(botocore_session=dbutils.credentials.getServiceCredentialsProvider("sqs-orders"),
                        region_name="eu-west-1")
sqs = session.client("sqs")
```
Replaces instance profiles and access keys in secrets for service access; works on UC-enabled compute access modes per docs.

## Connections (federation and HTTP)
```sql
CREATE CONNECTION pg_prod TYPE postgresql
OPTIONS (host 'pg.internal', port '5432',
         user secret('pg', 'user'), password secret('pg', 'password'));
CREATE FOREIGN CATALOG pg_prod_cat USING CONNECTION pg_prod OPTIONS (database 'app');
```
Grant connection privileges to the principals that need them (see the connection privileges section of the Databricks documentation).

## vs storage credentials
Storage credentials + external locations are for **files** in cloud storage. Service credentials are for **APIs**. Connections are for **databases/HTTP endpoints**.

## Gotchas
- Grants matter: `ACCESS` on a service credential; connection privileges on a connection; foreign catalogs need their own USE CATALOG/SELECT grants.
- Use secret scopes inside connection options, never plain passwords.

## Verify
As the granted principal, the boto3 call or federated query succeeds; as another principal it fails with a permission error.

## Checked

- 2026-10-28: confirmed on the service credentials and use-service-credentials pages (`dbutils.credentials.getServiceCredentialsProvider`, `ACCESS` privilege) and the PostgreSQL federation and CREATE CONNECTION pages.
- Removed: the `USE CONNECTION` grant, the `http_request` call and audit log claim (not in the fetched pages).

Method: documentation only; no commands were run.
