---
id: computing-software.cloud-infrastructure-engineering.aws.imds-role-credentials-and-exfiltration-protection
name: imds-role-credentials-and-exfiltration-protection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, imds-credentials, credential-exfiltration, imdsv2, ec2instancesourcevpc, guardduty-exfiltration, ssrf]
level: advanced
status: docs-checked
description: "Understand how instances get role credentials from IMDS and stop stolen instance credentials being used elsewhere: IMDSv2, hop limit, source VPC/IP conditions, detection."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IMDS role credentials and exfiltration protection

## 1. How credentials are served
An instance role's temporary credentials are delivered through the instance metadata service (IMDS).
IMDSv2 is session oriented: a PUT request with a TTL header (maximum six hours, 21,600 seconds)
returns a token, which later requests send in a header.
```bash
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
```
By default both IMDSv1 and IMDSv2 work. The AWS SDKs use IMDSv2 by default, and some fall back to
IMDSv1 if IMDSv2 gets no response. Anyone who can make the HTTP request from the instance (any
local process, or a remote attacker via SSRF) can obtain the role's credentials.

## 2. Reduce the chance of theft
- **IMDSv2 only** (`HttpTokens=required`): IMDSv1 requests stop working. Make sure all software on
  the instance supports IMDSv2 first.
- **Hop limit**: the PUT response hop limit is 1 by default. In a container environment the
  container counts as an extra hop, so SDK calls from containers may get no response at hop
  limit 1; raising it to 2 (or passing settings such as the Region directly to the container)
  is the documented mitigation. Keeping it at 1 stops containers reaching the node role.
- Change settings with `aws ec2 modify-instance-metadata-options --instance-id <ID>
  --http-tokens required --http-put-response-hop-limit 1`.
- Least privilege on instance roles; no long-lived keys on disk.

## 3. Make stolen credentials useless outside the instance
IAM global condition keys present when a request is signed with EC2 role credentials:
- `aws:Ec2InstanceSourceVpc`: the VPC the credentials were delivered to.
- `aws:Ec2InstanceSourcePrivateIPv4`: the private IPv4 of the primary network interface they were
  delivered to; always use it together with `aws:Ec2InstanceSourceVpc`, never alone in an Allow.
Compare them with where the request came from (`aws:SourceVpc`, `aws:VpcSourceIp`, which are
present only when the request goes through a VPC endpoint). IAM documents this policy:
```json
{"Sid": "RequireSameVPC", "Effect": "Deny", "Action": "*", "Resource": "*",
 "Condition": {
   "StringNotEquals": {"aws:SourceVpc": "${aws:Ec2InstanceSourceVpc}"},
   "Null": {"ec2:SourceInstanceARN": "false"},
   "BoolIfExists": {"aws:ViaAWSService": "false"}}}
```
The `ec2:SourceInstanceARN` test limits it to EC2 instance roles, and `aws:ViaAWSService` lets AWS
act on your behalf (for example S3 calling KMS). The condition keys work in IAM policies, SCPs,
VPC endpoint policies and resource policies. Because `aws:SourceVpc` exists only for VPC endpoint
traffic, roll this out together with endpoints for the services in use.

## 4. Detect
- GuardDuty `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`: instance
  credentials used from an external IP address (default severity High).
- GuardDuty `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS`: instance
  credentials used from an IP address or VPC endpoint owned by a different AWS account (High, or
  Medium when the account is affiliated with your environment).
- Both can fire for legitimate routing (on-premises egress, hub VPC endpoints); use suppression
  rules with the finding type plus the remote IP or account ID.

## 5. Respond
1. Identify the remote account or IP from the finding, and contact the credential owner.
2. Find the theft vector: SSRF in the web app, compromised container, debug endpoint.
3. Enforce IMDSv2 and hop limit 1 on the instance (`modify-instance-metadata-options`).
4. Follow the GuardDuty guidance for remediating a potentially compromised instance.

## Gotchas
- `HttpEndpoint=disabled` turns off IMDS for the instance; software that reads credentials from
  IMDS then needs another source.

## Verify
- [ ] Fleet reports `HttpTokens=required` and hop limit 1 (2 only where justified).
- [ ] Using copied instance credentials from a laptop is denied (perimeter policy) and raises a GuardDuty finding in a test.

## Checked
2026-10-28. Confirmed against the EC2 User Guide pages on retrieving and configuring instance metadata (token TTL up to six hours, PUT hop limit default 1, SDK IMDSv2 default and fallback, container hop behaviour, httpTokens=required), the IAM condition keys reference (Ec2InstanceSourceVpc and Ec2InstanceSourcePrivateIPv4, availability, the example policy, ViaAWSService) and the GuardDuty IAM finding types page (both exfiltration findings, severities, suppression advice), plus botocore ec2 ModifyInstanceMetadataOptions (HttpTokens, HttpPutResponseHopLimit, HttpEndpoint). Replaced the policy with the documented one (the old example used a Null test on the wrong key). Removed unconfirmed claims: the credential endpoint path and response field names, the 6-hour credential expiry, 2 as a default hop limit for container hosts, the iptables rule, the MetadataNoToken metric, CloudTrail userIdentity patterns, token revocation steps and the AssumeRole gotcha.
Method: documentation only; no commands were run.
