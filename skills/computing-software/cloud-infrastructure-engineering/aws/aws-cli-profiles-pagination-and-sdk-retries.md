---
id: computing-software.cloud-infrastructure-engineering.aws.aws-cli-profiles-pagination-and-sdk-retries
name: aws-cli-profiles-pagination-and-sdk-retries
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, cli-profiles, sdk, exponential-backoff, retries, pagination, jmespath, sso-login, credential-provider-chain, assume-role, boto3, aws-sdk, retry-mode, adaptive-retry, throttling, cli-v2, aws-vault, environment-variables]
level: practitioner
status: docs-checked
description: "Use the AWS CLI v2 and SDKs correctly: credential chain and named profiles (SSO, role chaining), pagination and JMESPath queries, retry modes and exponential backoff for throttling, and timeouts."
sources: ["https://github.com/aws/aws-cli/blob/v2/awscli/topics/config-vars.rst", "https://github.com/aws/aws-cli/blob/v2/awscli/topics/s3-config.rst", "https://github.com/aws/aws-cli/blob/v2/awscli/data/cli.json", "https://github.com/boto/botocore/blob/develop/botocore/retries/standard.py", "https://github.com/boto/botocore/blob/develop/botocore/config.py", "https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CLI and SDKs — credentials, pagination and retries done the way the tools expect

**Goal:** scripts and services that find the right credentials without hard-coding keys,
read every page of a result, and survive throttling without hammering the API.

## 1. Credential provider chain (order matters)
Each SDK and tool checks a series of sources in order and stops at the first valid credentials. Settings given in code take precedence; the environment and the shared `config`/`credentials` files follow. Typical sources: access keys (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`), web identity or OIDC federation, IAM Identity Center, assume-role profiles, container credentials (ECS and EKS), a `credential_process`, and **IMDS** (EC2 instance profile). The exact order differs between SDKs, so check your SDK's or tool's credential-chain page rather than assuming one order.
On AWS compute, prefer container, instance-profile or web-identity credentials; never ship static keys in images or user data.

## 2. Profiles
```ini
# ~/.aws/config
[sso-session corp]
sso_start_url = https://corp.awsapps.com/start
sso_region = eu-west-1
sso_registration_scopes = sso:account:access

[profile dev]
sso_session = corp
sso_account_id = 111111111111
sso_role_name = Developer
region = eu-west-1
output = json

[profile prod-admin]
role_arn = arn:aws:iam::222222222222:role/Admin
source_profile = dev          # role chaining from an SSO profile
mfa_serial = arn:aws:iam::111111111111:mfa/me
duration_seconds = 3600
```
- `aws sso login --sso-session corp` once; all profiles under the session share the token.
- `aws sts get-caller-identity --profile prod-admin` is the universal "who am I" check.
- `credential_process` in the config file lets the CLI call an external command that prints JSON credentials to stdout.
- Keys for an assumed-role profile include `role_arn`, `source_profile`, `mfa_serial` and `duration_seconds`; precedence of settings is command-line options, then environment variables, then the config file.

## 3. Pagination
- The CLI paginates automatically for operations that support it; `--page-size` sets the size of each service call without changing the number of items output (smaller pages mean more calls, which can help avoid timeouts); `--max-items` caps the total returned and, when more exist, the output contains a `NextToken` to pass to `--starting-token`; `--no-paginate` makes a single call for the first page.
- SDK clients return one page per call; use the SDK's paginators (boto3 shown).
  ```python
  paginator = s3.get_paginator('list_objects_v2')
  for page in paginator.paginate(Bucket=b, PaginationConfig={'PageSize': 1000}):
      for obj in page.get('Contents', []): ...
  ```
- Ignoring the continuation token or truncation flag in a response means you only see the first page.

## 4. Output and filtering
- `--query` is **JMESPath**, applied client-side:
  `aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,Tags[?Key==`Name`].Value|[0]]' --output table`.
- `--filters Name=tag:env,Values=prod` is server-side where supported — use it first to cut data.
- `--output` accepts `json`, `table`, `text`, `yaml`, `yaml-stream` and `off`.
- `--cli-read-timeout` and `--cli-connect-timeout` (seconds; `0` means blocking, no timeout) control socket timeouts; `--debug` enables debug logging.

## 5. Retries and backoff
| Mode | Behaviour |
|---|---|
| `legacy` | The pre-existing botocore behaviour; the service model typically allows four retries (5 attempts). Not a documented CLI v2 option |
| `standard` | Standardized retry rules and a retry quota; defaults to 3 attempts in total unless `max_attempts` is set; exponential backoff with jitter capped at 20 s. The AWS CLI v2 default |
| `adaptive` | `standard` plus automatic client-side throttling; documented by the CLI as experimental and subject to change |
```ini
[profile dev]
retry_mode = adaptive
max_attempts = 10
```
`max_attempts` counts all attempts including the first (5 means up to 4 retries). Env: `AWS_RETRY_MODE`, `AWS_MAX_ATTEMPTS`. Boto3: `Config(retries={'mode':'adaptive','max_attempts':10}, connect_timeout=5, read_timeout=60)`.
- Standard mode retries a defined set of throttling error codes (for example `Throttling`, `ThrottlingException`, `TooManyRequestsException`, `RequestLimitExceeded`), transient errors (`RequestTimeout`) and HTTP 500, 502, 503 and 504, plus connection errors. Validation and authorization errors are not retried; fix the request.
- botocore's backoff is truncated binary exponential backoff with jitter: `rand(0, 1) * min(base * 2**attempt, 20 s)`.
- Parallel scripts: limit concurrency yourself rather than relying on retries.

## 6. Useful CLI settings
- `cli_pager=` (empty), `AWS_PAGER=""` or `--no-cli-pager` disable the pager in scripts.
- S3 transfer settings go under an `s3` key in the profile (`max_concurrent_requests`, `max_queue_size`, `multipart_threshold`, `multipart_chunksize`, among others); see `aws help topics s3-config`.
- `aws configure export-credentials --profile dev --format env` for tools without profile support.
- `--endpoint-url` overrides a command's endpoint; `AWS_ENDPOINT_URL` sets a global endpoint override.
- `aws <svc> wait <condition>` (e.g. `ec2 wait instance-running`) instead of sleep loops.

## Gotchas
- `AWS_PROFILE` env silently overrides `--profile` in some third-party tools; check `get-caller-identity`.
- SSO tokens expire; unattended CI should use federation (OIDC) or role-based credentials rather than cached SSO logins.
- Default retry settings differ between SDKs; check each SDK's reference for its defaults.

## Verify
- [ ] `aws sts get-caller-identity --profile <each>` returns the expected account/role.
- [ ] A listing of > 1 000 objects returns the full count via paginator.
- [ ] With `retry_mode=adaptive` and `--debug`, a throttled bulk run shows backoff and completes.
- [ ] No long-lived access keys in repos or images.
- [ ] Scripts run with `AWS_PAGER=""` and do not hang waiting for `less`.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch (config-vars and s3-config topics, data/cli.json, botocore fork config provider), botocore develop branch (retries/standard.py, config.py), AWS SDKs and Tools Reference Guide page on standardized credential providers.
Confirmed: CLI v2 defaults retry_mode standard and max_attempts 3, max_attempts counts the initial attempt, adaptive described as experimental, backoff cap 20 s with jitter, retried error codes and HTTP statuses, CLI pagination flags and NextToken behaviour, output formats, --cli-read-timeout/--cli-connect-timeout semantics, pager precedence and disable options, credential_process, assume-role keys, S3 config keys, AWS_ENDPOINT_URL, export-credentials, boto3 Config retries and timeouts.
Corrected: the credential provider chain order differs per SDK (the single fixed order in the earlier text was removed); standard backoff is capped at 20 s with jitter and the base scale is not a fixed 1 s; legacy is not a documented CLI v2 mode.
Removed as unconfirmed: JS and Go paginator names, IMDS hop-limit advice, SSO token lifetime, aws-vault reference, query-versus-max-items ordering claim.
Method: documentation only; no commands were run.
