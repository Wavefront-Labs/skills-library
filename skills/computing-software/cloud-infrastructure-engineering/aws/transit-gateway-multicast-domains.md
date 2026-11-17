---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-multicast-domains
name: transit-gateway-multicast-domains
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-multicast, multicast-domain, igmp]
level: advanced
status: docs-checked
description: "Run IP multicast in AWS with a multicast-enabled Transit Gateway: domains, subnet associations, static or IGMPv2 group membership and their constraints."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-multicast-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit Gateway multicast

## 1. Enable and create a domain
```bash
aws ec2 create-transit-gateway --options MulticastSupport=enable,AmazonSideAsn=64512
aws ec2 create-transit-gateway-multicast-domain --transit-gateway-id tgw-0abc \
  --options Igmpv2Support=enable,StaticSourcesSupport=disable,AutoAcceptSharedAssociations=enable
aws ec2 associate-transit-gateway-multicast-domain --transit-gateway-multicast-domain-id tgw-mcast-domain-0abc \
  --transit-gateway-attachment-id tgw-attach-0abc --subnet-ids subnet-a subnet-b
```
You must create a new transit gateway to support multicast. A multicast domain segments the multicast network and makes
the transit gateway act as multiple multicast routers; domain membership is defined per subnet, and a subnet can be in
only one multicast domain. Group membership is defined per elastic network interface (ENI) attached to EC2 instances.

## 2. Membership
- **IGMPv2:** AWS supports IGMPv2. Hosts join and leave dynamically; in an IGMP group members can both send and
  receive. The transit gateway sends an IGMPv2 query to all members every two minutes and removes a member that fails
  to answer three consecutive queries from joined groups (it keeps querying that member for up to 12 hours; an
  explicit LEAVE removes it immediately and permanently). If every JOIN a host sends at startup is lost, the host is not
  in the group and you must re-trigger the JOIN from the host.
- **Static (API-based):** a static source domain has hosts that do not use IGMP; you use the AWS CLI to add a source
  and group members. Static group members can only receive:
```bash
aws ec2 register-transit-gateway-multicast-group-members --transit-gateway-multicast-domain-id <ID> \
  --group-ip-address 239.1.1.1 --network-interface-ids eni-0rx1 eni-0rx2
aws ec2 register-transit-gateway-multicast-group-sources --transit-gateway-multicast-domain-id <ID> \
  --group-ip-address 239.1.1.1 --network-interface-ids eni-0tx
aws ec2 search-transit-gateway-multicast-groups --transit-gateway-multicast-domain-id <ID>
```
- Only static multicast supports IPv6; dynamic (IGMP) multicast does not.
- Static groups and sources for ENIs that no longer exist are removed automatically, using the Transit Gateway
  service-linked role.

## 3. Security groups and NACLs
Minimum rules for IGMP multicast (security groups and network ACLs both apply):
- Inbound: protocol 2 (IGMP) from `0.0.0.0/32` (the IGMP query), and UDP from the remote host IP address (the sender).
  A security group cannot be the source of the UDP inbound rule.
- Outbound: protocol 2 to `224.0.0.2/32` (leave) and to the multicast group IP address (join), and UDP to the multicast
  group IP address.
- The transit gateway queries from source `0.0.0.0/32` to `224.0.0.1/32`, protocol 2.
- If source and destination are in the same VPC, you cannot reference the source's security group from the destination
  security group.

## Constraints
- A non-Nitro instance cannot be a multicast sender, and must have the Source/Dest check disabled.
- Multicast routing is not supported over Direct Connect, Site-to-Site VPN, peering attachments or transit gateway
  Connect attachments.
- Fragmented multicast packets are dropped.
- Transit gateway multicast may not suit high-frequency trading or other performance-sensitive applications; review
  the Multicast quotas and, for requirements, contact your AWS account team or Solutions Architect.

## Verify
- [ ] `search-transit-gateway-multicast-groups` lists the expected sources and members for the group address.
- [ ] A receiver sees the sender's UDP traffic to the group address, after the rules above are in place.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Multicast in AWS Transit Gateway overview page (concepts, considerations, routing, NACL and
security group rules) and the botocore EC2 model (option names and enum values for the CLI calls). The manage-domain
and working-with-multicast sources returned no readable content and were dropped. Removed: the modify-based enabling
claim, the PIM statement, the RAM sharing statement, the non-Nitro-receive note (not stated beyond "cannot be a
sender"), the `224.0.0.0/4` rule (the page gives specific addresses) and the iperf test.
