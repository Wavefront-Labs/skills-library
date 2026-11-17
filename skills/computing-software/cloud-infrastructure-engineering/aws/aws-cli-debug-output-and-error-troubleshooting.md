---
id: computing-software.cloud-infrastructure-engineering.aws.aws-cli-debug-output-and-error-troubleshooting
name: aws-cli-debug-output-and-error-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, cli-debug, dry-run, decode-authorization-message, cli-errors, credential-resolution]
level: practitioner
status: docs-checked
description: "Troubleshoot AWS CLI failures: --debug to see credential resolution, endpoints and raw responses, --dry-run checks, decoding encoded authorization messages, and common errors."
sources: ["https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-troubleshooting.html", "https://github.com/aws/aws-cli/blob/v2/awscli/topics/config-vars.rst", "https://github.com/aws/aws-cli/blob/v2/awscli/data/cli.json", "https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CLI debug output and error troubleshooting

## 1. Who am I, where am I
```bash
aws sts get-caller-identity
aws configure list            # which profile and where each value came from
aws configure list-profiles
```
Environment variables (`AWS_ACCESS_KEY_ID`...) override profiles silently; a stale
`AWS_SESSION_TOKEN` in the shell is a classic cause of `ExpiredToken`.

## 2. --debug
```bash
aws s3api head-bucket --bucket b --debug 2> debug.log
```
`--debug` turns on debug logging on stderr, which includes request and response details. Write it to a file and read it there; never paste full debug logs publicly (they can contain signatures and sometimes tokens). `--no-sign-request` sends unsigned requests (no credentials are loaded), which separates credential problems from other failures.

## 3. --dry-run (EC2 and some services)
```bash
aws ec2 run-instances --image-id ami-0abc --instance-type t3.micro --dry-run
```
`DryRunOperation` = you would be allowed; `UnauthorizedOperation` = denied. Useful to test
IAM without creating resources. It is an EC2 operation parameter; other services may not offer it.

## 4. Decode encoded authorization failures
Only certain AWS operations return an encoded authorization message; the operation's documentation says whether it does. Decode it with:
```bash
aws sts decode-authorization-message --encoded-message '<blob>' --query DecodedMessage --output text
```
The caller needs `sts:DecodeAuthorizationMessage` permission. The decoded message says whether the request was denied by an explicit deny or by the absence of an explicit allow, and includes the principal, the requested action and resource, and the condition-key values in the request context.

## 5. Common errors
| Error | Fix |
|---|---|
| `Unable to locate credentials` | no credentials found from the environment, profile or role; check `aws configure list`, `aws sso login --profile x` |
| Expired token errors | refresh SSO (`aws sso login`), unset stale `AWS_SESSION_TOKEN` and other credential environment variables |
| `SignatureDoesNotMatch` / `InvalidClientTokenId` | wrong or deleted access key, wrong secret, or system clock skew |
| `Could not connect to the endpoint URL` | wrong region name, service not offered in the region, no network or proxy, or a custom `--endpoint-url` |
| `AccessDenied` | read the message to see which policy type denied; decode the authorization message where one is returned |
| `Unknown options` / `Invalid choice` | outdated CLI lacking the newer API; check `aws --version` and upgrade |
| `Parameter validation failed` | shorthand or JSON quoting; use `--cli-input-json file://` |
| Output paging stuck in scripts | `--no-cli-pager` or `AWS_PAGER=""` (an empty value disables the pager) |
| Binary/base64 surprises (v2) | `--cli-binary-format raw-in-base64-out` makes binary values be treated literally; the default is base64 |

## Verify
- [ ] `get-caller-identity` returns the intended principal before running changes.
- [ ] `--debug` output confirms the expected credential source and endpoint.
- [ ] Scripts set `AWS_PAGER=""` and explicit `--region`/`--profile`.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch (config-vars topic, cli.json global options), botocore STS service model documentation for DecodeAuthorizationMessage.
Confirmed: --debug, --no-sign-request, --no-cli-pager and AWS_PAGER empty-value behaviour, --cli-binary-format default base64 and raw-in-base64-out, sts decode-authorization-message semantics and the sts:DecodeAuthorizationMessage permission, what the decoded message contains, aws configure list and list-profiles.
Removed as unconfirmed: exact debug log strings, grep filter, jq pipe, EC2-only claim for --dry-run, China/GovCloud partition explanation, IMDS reachability hint.
Method: documentation only; no commands were run.
