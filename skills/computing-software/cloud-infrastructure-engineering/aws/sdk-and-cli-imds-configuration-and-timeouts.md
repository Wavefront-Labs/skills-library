---
id: computing-software.cloud-infrastructure-engineering.aws.sdk-and-cli-imds-configuration-and-timeouts
name: sdk-and-cli-imds-configuration-and-timeouts
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, imds, imds-timeout, aws-ec2-metadata-disabled, sdk-configuration, credential-provider-chain]
level: advanced
status: docs-checked
description: "Tune how AWS SDKs and the CLI use IMDS: disable lookups off EC2, set timeouts and attempts, endpoint mode, and fix slow credential resolution in containers."
sources: ["https://docs.aws.amazon.com/sdkref/latest/guide/feature-imds-client.html", "https://docs.aws.amazon.com/sdkref/latest/guide/feature-imds-credentials.html", "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDK and CLI IMDS configuration

## 1. Settings
| Env var | Config key | Effect |
|---|---|---|
| `AWS_EC2_METADATA_DISABLED=true` | | SDK never calls IMDS (no credentials or Region from it) |
| `AWS_METADATA_SERVICE_TIMEOUT` | | seconds per attempt (default 1 second) |
| `AWS_METADATA_SERVICE_NUM_ATTEMPTS` | | number of attempts |
| `AWS_EC2_METADATA_SERVICE_ENDPOINT_MODE` | `ec2_metadata_service_endpoint_mode` | `IPv4` (default) or `IPv6` |
| `AWS_EC2_METADATA_SERVICE_ENDPOINT` | `ec2_metadata_service_endpoint` | custom endpoint; defaults to `http://169.254.169.254` (IPv4) or `http://[fd00:ec2::254]` (IPv6) |
| `AWS_EC2_METADATA_V1_DISABLED=true` | `ec2_metadata_v1_disabled` | never fall back to IMDSv1 |

## 2. Symptoms and fixes
- **CLI or SDK slow off EC2** (laptop, CI, on-prem): each call waits for IMDS to time out as the last
  credential provider. Set `AWS_EC2_METADATA_DISABLED=true` or supply credentials earlier in the chain.
- **Timeouts in containers on EC2:** the IMDSv2 PUT response hop limit (1 to 64) set to 1 can cause
  issues in container environments (EC2 docs). Raise `HttpPutResponseHopLimit` (the AMI default for IMDSv2-only
  images is 2), or better, use task roles / Pod Identity so containers do not need node IMDS at all.
- **Occasional `Unable to locate credentials` under load:** raise the timeout and attempts settings above.
- **IPv6-only:** set endpoint mode IPv6.

## 3. Verify which provider resolved
```bash
aws configure list            # shows source of credentials (iam-role, env, shared-credentials-file)
aws sts get-caller-identity --debug 2>&1 | grep -i -E 'credential|metadata' | head
```

## Verify
- [ ] CI jobs show no IMDS connection attempts in `--debug` output.
- [ ] Containerised apps get credentials from the task/pod role, not node IMDS.

## Checked

2026-10-28. Confirmed against the SDK reference IMDS client and credentials pages, the CLI environment-variable page and the EC2 instance-metadata options page: variable names, 1-second timeout default, endpoint mode default and endpoint defaults, v1-disabled setting, the IMDSv1 fallback behaviour, hop limit range 1-64 and container issue at hop limit 1. Removed (unconfirmed): config-file keys for timeout and attempts, an attempts default, credential-caching claim, specific retry numbers. Read end to end.

Method: documentation only; no commands were run.
