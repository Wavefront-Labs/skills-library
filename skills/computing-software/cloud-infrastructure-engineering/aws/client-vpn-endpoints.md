---
id: computing-software.cloud-infrastructure-engineering.aws.client-vpn-endpoints
name: client-vpn-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, client-vpn, client-vpn-endpoint, split-tunnel, saml, mutual-authentication, remote-access, vpn]
level: practitioner
status: docs-checked
description: "Stand up AWS Client VPN: mutual-cert or SAML authentication, client CIDR, target network associations, authorization rules, split tunnel, routes and connection logging."
sources: ["https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-working-endpoint-create.html", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authorization.html", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/split-tunnel-vpn.html", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-self-service-portal.html", "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/connection-logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Client VPN endpoints

**Goal:** engineers reach private VPC resources from laptops with SSO identities, only the
networks they are entitled to, and without routing all their internet traffic through AWS.

## 1. Create (SAML + split tunnel)
```bash
aws ec2 create-client-vpn-endpoint \
  --client-cidr-block 172.31.240.0/22 \
  --server-certificate-arn "$ACM_SERVER_CERT" \
  --authentication-options Type=federated-authentication,FederatedAuthentication={SAMLProviderArn=$SAML_ARN} \
  --connection-log-options Enabled=true,CloudwatchLogGroup=/clientvpn/prod \
  --split-tunnel --vpc-id vpc-123 --security-group-ids sg-cvpn \
  --dns-servers 10.0.0.2 --transport-protocol udp --session-timeout-hours 8
```
- Client CIDR: /22 at minimum and no larger than /12; AWS recommends /22. It must not overlap the target network, the VPC or any route on the endpoint, and cannot be changed after creation.
- Authentication: **Active Directory** (directory ID), **SAML** federated (IAM SAML provider ARN; optional self-service SAML provider) or **mutual** certificate authentication (client certificate ARN in ACM).
- The server certificate must be in ACM in the Region where you create the endpoint (provisioned by ACM or imported).
- Optional: connection logging to CloudWatch Logs, a client connect handler (Lambda that allows or denies connections), custom DNS servers (include the VPC DNS server IP to resolve private names).

## 2. Associate, authorise, route
```bash
aws ec2 associate-client-vpn-target-network --client-vpn-endpoint-id cvpn-endpoint-1 --subnet-id subnet-a
aws ec2 associate-client-vpn-target-network --client-vpn-endpoint-id cvpn-endpoint-1 --subnet-id subnet-b
aws ec2 authorize-client-vpn-ingress --client-vpn-endpoint-id cvpn-endpoint-1 \
  --target-network-cidr 10.0.0.0/16 --access-group-id <IDP_GROUP_ID>
aws ec2 create-client-vpn-route --client-vpn-endpoint-id cvpn-endpoint-1 \
  --destination-cidr-block 10.20.0.0/16 --target-vpc-subnet-id subnet-a
```
Two authorization layers: **security groups** (applied to the endpoint's network interfaces; associating a subnet applies the VPC's default security group, change it afterwards; target resources must allow the endpoint's security group) and **network-based authorization rules** per destination CIDR, optionally per identity-provider group.

## 3. Split tunnel
By default all client traffic goes over the tunnel (the client route table is overwritten with 0.0.0.0/0). With split-tunnel, the routes in the endpoint's route table are pushed to the client and only traffic to those networks uses the tunnel. Notes from the docs: adding 0.0.0.0/0 to a split-tunnel endpoint's route table may disrupt connectivity and is not recommended; any change to the endpoint route table resets all client connections.

## 4. Client config
`aws ec2 export-client-vpn-client-configuration --client-vpn-endpoint-id ... --output text > cvpn.ovpn`.
The self-service portal (`https://self-service.clientvpn.amazonaws.com/` or `.../endpoints/<endpoint-id>`) must be enabled on the endpoint; clients sign in with user-based credentials to download the configuration and the AWS provided client. It is not available with mutual authentication. A customised configuration file you must distribute yourself.

## Gotchas
- Connection log fields include `username` (recorded only for AD or SAML), `transport-protocol`, ingress/egress bytes and packets; a denied connection shows `authorization-policy-deny` as the failure reason.
- Check the VPC pricing page for per-association and per-connection charges before leaving non-prod endpoints associated.

## Verify
- [ ] User in the authorised group connects and reaches 10.0.x.x; user outside it connects but cannot reach the CIDR.
- [ ] With split tunnel, the user's public IP is still their own ISP's.
- [ ] Connection logs in CloudWatch show username, connect/disconnect and bytes.

## Checked
2026-10-28. Confirmed on the create-endpoint, client-authorization, split-tunnel, self-service-portal and connection-logging pages: CIDR range rule and immutability, ACM same-Region rule, auth types, optional features, security group behaviour, split-tunnel semantics and warnings, portal URLs and mutual-auth exclusion, log fields. Removed as unconfirmed: client traffic NATed to the ENI IP, combining AD or SAML with mutual authentication, SAML `memberOf` attribute name, full-tunnel route/rule/NAT recipe, billing structure, "self-service works only with SAML/AD" beyond the documented mutual exclusion.
Method: documentation only; no commands were run.
