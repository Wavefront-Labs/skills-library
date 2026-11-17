---
id: computing-software.cybersecurity-defensive.cloud-security.imdsv2-enforcement
name: imdsv2-enforcement
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-network-security, imdsv2, instance-metadata-service, ssrf-mitigation, credential-theft, hop-limit, aws-ec2, metadata-protection]
level: practitioner
status: docs-checked
description: "Enforce IMDSv2 on EC2 to stop SSRF-based credential theft: account defaults, launch templates, hop limits and monitoring."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IMDSv2 enforcement

**Goal:** an SSRF bug or a compromised container cannot simply GET the instance metadata URL and
steal the instance role's credentials.

## Why
IMDSv1 calls do not require a token; IMDSv2 calls require one, fetched from `/latest/api/token`. An SSRF bug in a
web app that can only issue simple GETs then cannot reach role credentials, and the hop limit (the number of
network hops the PUT response may make, 1 to 64) limits how far the token reply travels, for example into containers.

## Enforce
Account-level default for new launches (per Region; does not affect existing instances):
```
aws ec2 modify-instance-metadata-defaults --http-tokens required --http-put-response-hop-limit 2
```
Existing instances:
```
aws ec2 modify-instance-metadata-options --instance-id i-0abc --http-tokens required --http-put-response-hop-limit 1
```
- Precedence at launch: instance or launch template values first, then account defaults, then the AMI. Each option
  is evaluated separately. `HttpTokens` and `HttpPutResponseHopLimit` can come from the AMI.
- AMIs: register or modify with `imds-support` `v2.0`; launches from it get IMDSv2 and a hop limit of 2.
- Account-level enforcement (`HttpTokensEnforced`) makes launches with `HttpTokens` optional fail, so it also
  blocks IMDSv1 launches; see "Enforce IMDSv2 at the account level" in the EC2 User Guide.
- A hop limit of 1 can cause problems in container environments; see "Instance metadata access considerations" in
  the EC2 User Guide before choosing it for container hosts.
- Use IAM condition keys in an IAM policy or SCP to allow launches only when IMDSv2 is required, to limit hops,
  or to turn off metadata access. Look up the exact key names in the EC2 User Guide.

## Find v1 usage before enforcing
Enforcing IMDSv2 breaks applications and agents that use IMDSv1. Find and update old SDKs and agents first
(CloudWatch metrics for EC2 metadata calls without a token; look up the current metric name in AWS docs).

## Gotchas
- Old agents that only speak IMDSv1 break once tokens are required.
- Disabling the IMDS entirely breaks anything that relies on instance metadata.
- On Windows, PowerShell earlier than 4.0 must be updated (Windows Management Framework 4.0) to require IMDSv2.
- Other clouds have their own metadata protections; read the provider documentation rather than assuming parity.

## Verify
- [ ] `aws ec2 describe-instances` shows `HttpTokens: required` in `MetadataOptions` for every instance.
- [ ] Applications still work after enforcement; no IMDSv1 callers remain.

## Checked
2026-10-31. Confirmed against the EC2 User Guide page "Configure the Instance Metadata Service options": token
behaviour, hop limit range, levels and precedence, `imds-support` v2.0 giving hop limit 2, `HttpTokensEnforced`,
`/latest/api/token`, breakage notes, PowerShell note; `check_commands.py` reports the two aws commands valid.
Removed unconfirmed: the Capital One reference, TTL-1 statement, SCP JSON and condition key name, the
`MetadataNoToken` metric name, Security Hub control id, Azure and GCP header claims, IRSA, 401 response check.
Method: documentation only; no commands were run.
