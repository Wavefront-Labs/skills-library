---
id: computing-software.cloud-infrastructure-engineering.aws.imds-ipv6-endpoint-and-disabling-imds
name: imds-ipv6-endpoint-and-disabling-imds
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, imds, imds-ipv6, disable-imds, instance-metadata, ec2-security]
level: advanced
status: docs-checked
description: "Enable the IPv6 IMDS endpoint for IPv6-only instances, and fully disable IMDS where nothing needs it, including the account-level defaults and AMI settings."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-options.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-IMDS-new-instances.html", "https://docs.aws.amazon.com/sdkref/latest/guide/feature-imds-client.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IMDS IPv6 endpoint and disabling IMDS

## 1. IPv6 endpoint
```bash
aws ec2 modify-instance-metadata-options --instance-id i-0abc --http-protocol-ipv6 enabled
TOKEN=$(curl -s -X PUT "http://[fd00:ec2::254]/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "http://[fd00:ec2::254]/latest/meta-data/instance-id"
```
- Supported only on Nitro-based instances in IPv6-supported subnets (dual stack or IPv6 only). It can be
  enabled at launch or later, and the IPv4 endpoint stays enabled when it is on.
- SDKs: the IMDS client `endpoint_mode` setting accepts `IPv4` (default) or `IPv6`; the default IPv6 endpoint
  is `http://[fd00:ec2::254]`.

## 2. Turning IMDS off
```bash
aws ec2 modify-instance-metadata-options --instance-id i-0abc --http-endpoint disabled
```
When disabled, neither you nor any code on the instance can read instance metadata. Anything that depends
on it (for example SDKs that fetch instance profile credentials, or agents that read the Region or instance
identity) stops working, so confirm each dependency first. Disable only on hosts that get everything
elsewhere (appliances, some hardened builds).

## 3. Defaults for new instances
```bash
aws ec2 modify-instance-metadata-defaults --region <REGION> --http-tokens required --http-put-response-hop-limit 2
aws ec2 get-instance-metadata-defaults
```
Account-level defaults are set per Region and apply when the launch request does not specify options (the
API also accepts `--http-endpoint` and `--http-tokens-enforced`). AMIs can set `--imds-support v2.0` so
instances launched from them require IMDSv2. Organizations declarative policies can set the defaults org-wide;
while one is in use you cannot change the settings directly in the account.

## Verify
- [ ] `aws ec2 describe-instances --query 'Reservations[].Instances[].MetadataOptions'` shows the intended endpoint and protocol settings.
- [ ] With IMDS disabled, metadata requests from the instance fail and the workload still functions.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide "Configure the Instance Metadata Service options" and "Configure instance metadata options for new instances"; AWS SDKs and Tools Reference "IMDS client"; botocore EC2 model (ModifyInstanceMetadataOptions HttpProtocolIpv6 and HttpEndpoint, ModifyInstanceMetadataDefaults, GetInstanceMetadataDefaults).
Confirmed: IPv6 endpoint address [fd00:ec2::254], Nitro and IPv6-subnet requirement, IPv4 endpoint stays on, enabling at launch or later, disabling blocks all metadata access, default-setting commands, imds-support v2.0, declarative policy behaviour.
Removed: the AWS_EC2_METADATA_SERVICE_ENDPOINT_MODE variable name (not found in the SDK reference; the documented setting is endpoint_mode), the detailed list of services that break without IMDS, and the timeout behaviour of curl.

Method: documentation only; no commands were run.
