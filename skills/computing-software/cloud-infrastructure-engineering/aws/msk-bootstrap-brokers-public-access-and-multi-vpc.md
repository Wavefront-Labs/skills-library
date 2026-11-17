---
id: computing-software.cloud-infrastructure-engineering.aws.msk-bootstrap-brokers-public-access-and-multi-vpc
name: msk-bootstrap-brokers-public-access-and-multi-vpc
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, msk, kafka, bootstrap-brokers, multi-vpc-connectivity, msk-public-access, privatelink, msk-ports]
level: practitioner
status: docs-checked
description: "Connect clients to MSK: bootstrap broker strings and ports per auth method, enabling public access safely, and multi-VPC private connectivity across accounts with PrivateLink."
sources: ["https://docs.aws.amazon.com/msk/latest/developerguide/port-info.html", "https://docs.aws.amazon.com/msk/latest/developerguide/public-access.html", "https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html", "https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html", "https://docs.aws.amazon.com/msk/latest/developerguide/configure-clients-for-iam-access-control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSK bootstrap brokers, public access and multi-VPC connectivity

## Bootstrap strings and ports
```bash
aws kafka get-bootstrap-brokers --cluster-arn "$C"
```
| Auth | Private port | Public port | Field |
|---|---|---|---|
| Plaintext | 9092 | n/a | `BootstrapBrokerString` |
| TLS | 9094 | 9194 | `BootstrapBrokerStringTls` |
| SASL/SCRAM | 9096 | 9196 | `BootstrapBrokerStringSaslScram` |
| IAM | 9098 | 9198 | `BootstrapBrokerStringSaslIam` |
| Multi-VPC (PrivateLink) | see the bootstrap string | n/a | `BootstrapBrokerStringVpcConnectivityTls`, `...SaslScram`, `...SaslIam` |
Public strings are `BootstrapBrokerStringPublicTls`, `...PublicSaslScram` and `...PublicSaslIam`.
IPv6 (dual-stack clusters) uses ports 20092, 20094, 20096 and 20098 and the `...Ipv6` fields.
Use the whole string; the list may not include every broker and the client discovers the rest.
Security groups must allow the port from client SGs.

## IAM auth client
```properties
security.protocol=SASL_SSL
sasl.mechanism=AWS_MSK_IAM
sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
```
Needs the `aws-msk-iam-auth` jar (Java) and IAM permissions such as `kafka-cluster:Connect`,
`kafka-cluster:DescribeTopic`, `kafka-cluster:ReadData` and `kafka-cluster:WriteData` on the
cluster and topic resources. Non-Java clients use the `SASL_OAUTHBEARER` mechanism with the AWS
MSK IAM SASL signer libraries.

## Public access (provisioned clusters)
Supported on Apache Kafka 2.6.0 or later; it cannot be turned on while creating a cluster, only by
updating an existing one. Prerequisites: public subnets (route table with an internet gateway),
unauthenticated access off with at least one of IAM, SCRAM or mTLS on, encryption within the
cluster on (it cannot be enabled later, so a cluster created without it can never be made
public), plaintext client traffic off, and for SCRAM/mTLS `allow.everyone.if.no.acl.found=false`
with ACLs set first.
```bash
aws kafka update-connectivity --cluster-arn "$C" --current-version "$V" \
  --connectivity-info '{"PublicAccess":{"Type":"SERVICE_PROVIDED_EIPS"}}'
```
Restrict SG inbound to known IP ranges; public bootstrap strings appear as `...Public...` fields.
Turn it off with `{"PublicAccess":{"Type":"DISABLED"}}`; check progress with
`aws kafka describe-cluster-operation`.

## Multi-VPC private connectivity (other VPCs or accounts)
1. Cluster owner turns on `VpcConnectivity` for the auth methods and attaches a cluster policy:
```json
{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::444455556666:root"},
 "Action":["kafka:CreateVpcConnection","kafka:GetBootstrapBrokers","kafka:DescribeCluster","kafka:DescribeClusterV2"],
 "Resource":"<cluster-arn>"}
```
2. Client account creates a managed VPC connection:
   `aws kafka create-vpc-connection --target-cluster-arn ... --authentication <scheme> --vpc-id ... --client-subnets ... --security-groups ...`
   (`--authentication` must name a scheme enabled for multi-VPC on the cluster; see the CreateVpcConnection reference for the accepted strings).
3. Client uses the VPC connectivity bootstrap string. Works with overlapping CIDRs; no peering needed.

Requirements: Apache Kafka 2.7.1 or later, not the `t3.small` broker type, same Region only
(accounts may differ), IAM, TLS or SASL/SCRAM auth, the same number of client subnets as cluster
subnets with matching Availability Zone IDs, and no multi-VPC access to ZooKeeper nodes.

## Gotchas
- Unauthenticated access cannot be used with public or multi-VPC connectivity.
- Use the bootstrap field that matches the client's connectivity path and auth method; a mismatched string or blocked port shows up as metadata timeouts.

## Verify
- [ ] `kafka-topics.sh --list --bootstrap-server <string> --command-config client.properties` works from each client network.
- [ ] Public SG inbound limited to approved CIDRs; plaintext disabled.

## Checked

2026-10-27, AWS documentation (current release as read on that date). MSK Developer Guide port information, public access, multi-VPC connectivity and cluster policy, IAM client configuration and IAM action pages; botocore kafka 2018-11-14 model (GetBootstrapBrokers fields, UpdateConnectivity, CreateVpcConnection). Fixed: removed the unsourced multi-VPC port range 14001-14100 and the 2-AZ broker claim; public access needs Kafka 2.6.0 or later, cannot be set at creation, and needs encryption within the cluster; multi-VPC needs Kafka 2.7.1 or later, same Region, matching AZ IDs and is not supported on t3.small; added DescribeCluster to the cluster policy actions; the --authentication value is no longer stated because the docs do not list it. Confirmed: ports 9092/9094/9194/9096/9196/9098/9198, bootstrap field names, SERVICE_PROVIDED_EIPS and DISABLED, aws-msk-iam-auth with AWS_MSK_IAM jaas class names, kafka-cluster action names.
Method: documentation only; no commands were run.
