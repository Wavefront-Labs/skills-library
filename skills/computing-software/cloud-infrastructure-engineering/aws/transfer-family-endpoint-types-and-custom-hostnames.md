---
id: computing-software.cloud-infrastructure-engineering.aws.transfer-family-endpoint-types-and-custom-hostnames
name: transfer-family-endpoint-types-and-custom-hostnames
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transfer-family, transfer-endpoint, vpc-hosted-endpoint, elastic-ip-sftp, custom-hostname, sftp]
level: practitioner
status: docs-checked
description: "Choose Transfer Family endpoints: public vs VPC (internal, or internet-facing with Elastic IPs), security group allowlisting, custom hostnames and FTPS needs."
sources: ["https://docs.aws.amazon.com/transfer/latest/userguide/create-server-in-vpc.html", "https://docs.aws.amazon.com/transfer/latest/userguide/requirements-dns.html", "https://docs.aws.amazon.com/transfer/latest/userguide/create-server-ftps.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer Family endpoint types and custom hostnames

## 1. Endpoint types
| Type | Reachable from | Security groups / static IPs | Notes |
|---|---|---|---|
| `PUBLIC` | internet | see the endpoint docs | no VPC controls to configure |
| `VPC`, internal | VPC, peered VPCs, VPN/DX | VPC security groups | private partners over DX/VPN |
| `VPC`, internet-facing | internet | **Elastic IP addresses** (one per subnet) plus VPC security groups | partners allowlist your IPs; you allowlist theirs in the security group |
Only SFTP and FTPS can be used on an internet-facing VPC endpoint. FTP and FTPS are configured on `VPC` endpoints; the
legacy `VPC_ENDPOINT` type gets no FTP/FTPS support and is no longer offered in the console.

## 2. Create an internet-facing VPC endpoint
```bash
aws ec2 allocate-address --domain vpc   # one per subnet
aws transfer create-server --protocols SFTP --identity-provider-type SERVICE_MANAGED \
  --endpoint-type VPC \
  --endpoint-details 'VpcId=vpc-0abc,SubnetIds=[subnet-pub-a,subnet-pub-b],AddressAllocationIds=[eipalloc-a,eipalloc-b],SecurityGroupIds=[sg-0sftp]' \
  --security-policy-name <SECURITY_POLICY_NAME> \
  --logging-role arn:aws:iam::<ACCOUNT_ID>:role/TransferLogging
```
- FTPS inbound rules: port 21 (control channel) and 8192-8200 (data channel).
- While a VPC server is online only its subnets can be modified (UpdateServer); stop the server to add or change
  Elastic IP addresses.
- Security policies set the allowed algorithms; list the current names with `aws transfer list-security-policies`.
  The console's FIPS Enabled option is only available in North American Regions.

## 3. Custom hostnames
Partners should connect to `sftp.example.com`, not the server's generated endpoint name.
- Tag the server so the console shows the custom hostname: `transfer:customHostname`, plus
  `transfer:route53HostedZoneId` when Route 53 is the DNS provider, then create the DNS record
  (a Route 53 alias record, or a CNAME elsewhere).
```bash
aws transfer tag-resource --arn arn:aws:transfer:<REGION>:<ACCOUNT_ID>:server/s-1234567890abcdef0 \
  --tags Key=transfer:customHostname,Value=sftp.example.com
```
- SFTP host keys: when migrating from an existing SFTP server, supply its host key (RSA, ED25519 or ECDSA private
  key) so partners do not see a host key change warning.

## 4. Switching endpoint types
You must stop the server before you can change its endpoint; wait until the server status is Offline before
updating the endpoint type. Coordinate with partners, since addresses can change. Moving from the legacy
`VPC_ENDPOINT` type to `VPC` is the documented direction.

## 5. Monitoring connectivity
Use structured CloudWatch logging and the `BytesIn`/`BytesOut` metrics per server (`AWS/Transfer`).

## Verify
- [ ] Partners connect via the custom hostname to Elastic IPs they allowlisted; the security group restricts sources.
- [ ] `sftp -v user@sftp.example.com` shows the expected host key and negotiated cipher.
- [ ] Logs show successful sessions.

## Checked

2026-10-28. Confirmed against the Transfer Family User Guide pages create-server-in-vpc, requirements-dns, create-server-ftps, update-endpoint-type-vpc and tf-server-endpoint: internet-facing VPC endpoints use Elastic IPs and security groups and support only SFTP and FTPS, FTPS ports 21 and 8192-8200, stop the server before changing the endpoint or Elastic IPs, the `transfer:customHostname` and `transfer:route53HostedZoneId` tags (set by the user, not the console), the FIPS option, host key import for migrations.
Removed or corrected: tag names (were `aws:transfer:...`), PUBLIC endpoint claims (SFTP only, no source-IP restriction), "FTP only on internal VPC", AS2 VPC claim, SSH port 22 and internet gateway route claims, security policy name and PQ-hybrid variants, A-record option, log event names, and made-up account ID.
Method: documentation only; no commands were run.
