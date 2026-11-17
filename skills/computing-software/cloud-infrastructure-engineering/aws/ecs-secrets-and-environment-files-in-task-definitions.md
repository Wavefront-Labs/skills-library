---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-secrets-and-environment-files-in-task-definitions
name: ecs-secrets-and-environment-files-in-task-definitions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, ecs-secrets, environment-files, valuefrom, secrets-manager, ssm-parameter-store, fargate]
level: practitioner
status: docs-checked
description: "Inject Secrets Manager and SSM Parameter Store values and S3 env files into ECS containers with valueFrom, including JSON keys, version stages and platform version limits."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-secrets-manager.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/use-environment-file.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS secrets and environment files

**Goal:** containers receive secrets as environment variables without them appearing in the task definition.

## secrets with valueFrom
```json
"secrets": [
  {"name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:region:aws_account_id:secret:appauthexample-AbCdEf:username1::"},
  {"name": "API_URL", "valueFrom": "arn:aws:ssm:region:aws_account_id:parameter/parameter_name"}
]
```
- Secrets Manager form: `arn:aws:secretsmanager:region:aws_account_id:secret:secret-name:json-key:version-stage:version-id`. The three trailing parts are optional, but you must keep the colons to take defaults.
- `json-key`: only JSON values are supported; with no key the full secret contents are used.
- `version-stage` and `version-id` are mutually exclusive; with neither, `AWSCURRENT` is retrieved. Examples from the page: `...:appauthexample-AbCdEf::AWSPREVIOUS:` (stage) and `...:appauthexample-AbCdEf:::<version-id>` (version ID).
- Parameter Store: a parameter in the same Region as the task can be given by full ARN or by name; one in another Region needs the full ARN.
- Both services are managed key-value stores using AWS KMS. Secrets Manager adds automatic rotation, random secret generation and cross-account sharing; otherwise use encrypted Parameter Store parameters.

## Platform and agent requirements
- Fargate: full secret contents need platform version 1.3.0 or later; a specific JSON key or version needs 1.4.0 or later (Linux) or 1.0.0 (Windows).
- EC2: a specific JSON key or version needs container agent 1.37.0 or later; full contents need 1.22.0 or later.
- The task definition needs a task execution role with the additional permissions for Secrets Manager or Parameter Store (see the Amazon ECS task execution IAM role page for the exact statements).
- Interface VPC endpoints are recommended for private subnets; you must create them for Secrets Manager and for Systems Manager.

## Environment files
```json
"environmentFiles": [{"value": "arn:aws:s3:::amzn-s3-demo-bucket/envfile_object_name.env", "type": "s3"}]
```
- File must have the `.env` extension and UTF-8 encoding; maximum 10 files per task definition.
- One `VARIABLE=VALUE` per line; spaces and quotation marks become part of the value; lines starting `#` are comments.
- Needs the task execution role with additional S3 permissions. EC2 needs agent 1.39.0 or later; Fargate needs platform version 1.4.0 or later (Linux). Not available on Windows containers.
- Variables in the container definition `environment` parameter take precedence over the file. With duplicate names across several files, the first value wins. A container override file replaces the definition's files.
- The file is downloaded to disk for each task and removed at task cleanup; ECS sets no size limit, but a large file can fill the disk.
- AWS recommends Secrets Manager or Parameter Store for sensitive data; env files are S3 objects, so S3 security applies.

## Behaviour
- Values are injected when the container starts. If a secret is updated or rotated, running containers do not get it: launch a new task, or for a service use Force new deployment.
- The environment variables are visible to the application, container logs and debugging tools. AWS suggests, for higher assurance, an encrypted S3 bucket read via the task role, or a sidecar that writes the secret to a shared task-scoped volume (the app then reads a file).

## Method
Rewritten from the four cited ECS pages; claims not stated there were dropped.

## Checked
Checked 2026-11-08 against the four cited ECS Developer Guide pages. Removed as unconfirmed: the specific IAM action names, `ResourceInitializationError` text, `aws ecs execute-command` verification, and the NAT/endpoint requirement for Fargate beyond what the pages say.
Method: docs-only read of cited pages, 2026-11-08
