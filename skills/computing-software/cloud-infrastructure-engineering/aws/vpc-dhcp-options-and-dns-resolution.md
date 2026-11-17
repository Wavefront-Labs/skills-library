---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-dhcp-options-and-dns-resolution
name: vpc-dhcp-options-and-dns-resolution
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, dhcp-options, amazon-provided-dns, enable-dns-hostnames, enable-dns-support, route53-resolver, dns]
level: practitioner
status: docs-checked
description: "Configure VPC DNS: enableDnsSupport/enableDnsHostnames, the .2 Amazon-provided resolver, DHCP option sets (domain name, custom servers, NTP) and resource-based hostnames."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/AmazonDNS-concepts.html", "https://docs.aws.amazon.com/vpc/latest/userguide/DHCPOptionSetConcepts.html", "https://docs.aws.amazon.com/vpc/latest/userguide/DHCPOptionSet.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/hostname-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC DHCP options and DNS resolution

## 1. The two VPC attributes
| Attribute | Effect | Needed for |
|---|---|---|
| `enableDnsSupport` (default true) | Amazon DNS server answers at VPC base+2, 169.254.169.253 and fd00:ec2::253 | everything DNS-related |
| `enableDnsHostnames` (default false unless the VPC is a default VPC) | instances with public IPs get public DNS names | with `enableDnsSupport`, **private hosted zones and interface endpoint private DNS (both must be true)** |
```bash
aws ec2 modify-vpc-attribute --vpc-id vpc-123 --enable-dns-hostnames '{"Value":true}'
aws ec2 describe-vpc-attribute --vpc-id vpc-123 --attribute enableDnsHostnames
```
Symptom of a missing flag: PHZ records or `com.amazonaws.<REGION>.s3` private DNS do not resolve.

## 2. The Amazon-provided resolver (.2)
- Resolves public DNS, private hosted zones associated with the VPC, endpoint private DNS and
  Resolver rules. Limit: 1024 packets per second per network interface for the aggregate of Resolver queries, IMDS,
  Time Sync (NTP) and Windows licensing requests, and it cannot be increased; high-volume resolvers should cache
  locally (systemd-resolved, nscd, NodeLocal DNSCache on EKS).
- You cannot query the Amazon DNS server in a peer VPC, and private hosted zone names do not resolve from the other side
  of a VPN connection; use Route 53 Resolver endpoints for hybrid DNS. You cannot filter Amazon DNS traffic with
  security groups or network ACLs, and it supports only recursive queries.

## 3. DHCP option sets
```bash
aws ec2 create-dhcp-options --dhcp-configurations \
  "Key=domain-name,Values=corp.example.com" \
  "Key=domain-name-servers,Values=AmazonProvidedDNS" \
  "Key=ntp-servers,Values=169.254.169.123"
aws ec2 associate-dhcp-options --dhcp-options-id dopt-abc --vpc-id vpc-123
```
- Option sets cannot be modified after creation: create a new one and associate it. Instances pick up the change within
  a few hours depending on lease renewal, with no restart needed; you can renew the lease from the operating system.
  A VPC with no option set loses domain name resolution (on Nitro instances AWS configures 169.254.169.253 as the DNS server).
- Give `domain-name-servers` either `AmazonProvidedDNS` or custom servers; using both might cause unexpected behaviour.
  With custom servers, they must resolve instance hostnames and your private zones themselves (for EMR, add a conditional
  forwarder for `<REGION>.compute.internal` to the Amazon DNS server). Up to four IPv4 servers (three plus AmazonProvidedDNS).
- `domain-name` in us-east-1 default is `ec2.internal`; elsewhere `<REGION>.compute.internal`.
- `ipv6-address-preferred-lease-time`, `netbios-name-servers` exist for special cases.

## 4. Hostname type
Subnet setting `--private-dns-hostname-type-on-launch resource-name` gives hostnames like
`i-0abc.<REGION>.compute.internal` (the default for IPv6-only subnets); `ip-name` is the
classic `ip-10-0-1-5`. Enable `EnableResourceNameDnsARecordOnLaunch` for resolvable A records.

## Gotchas
- Changing DHCP options affects every instance in the VPC — schedule it.
- Use only domain names you fully control in the `domain-name` option; only some operating systems accept several names.

## Verify
- [ ] `dig @169.254.169.253 internal.example.com` resolves a PHZ record from an instance.
- [ ] `cat /etc/resolv.conf` shows the expected search domain after lease renewal.
- [ ] Interface endpoint DNS name (e.g. `sqs.<REGION>.amazonaws.com`) resolves to private IPs.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "Understanding Amazon DNS", "DHCP option set concepts", "Work with DHCP option sets" and "Amazon VPC quotas"; EC2 User Guide "Amazon EC2 instance hostname types"; VPC Peering Guide limitations; botocore EC2 model (ModifySubnetAttribute PrivateDnsHostnameTypeOnLaunch ip-name/resource-name and EnableResourceNameDnsARecordOnLaunch).
Confirmed: enableDnsSupport default true and enableDnsHostnames default false for non-default VPCs; both must be true for private hosted zones and interface endpoint private DNS; resolver addresses; 1024 pps link-local limit; option sets immutable and picked up within hours without restart; ec2.internal for us-east-1 and region.compute.internal elsewhere; resource-name default for IPv6-only subnets.
Corrected: the 1024 pps limit covers resolver, IMDS, NTP and Windows licensing together; resource-name hostnames are the default (not "required") for IPv6-only subnets; the peered-VPC resolver statement is now the documented limitation.
Removed: the dhclient command and the Windows per-interface DNS advice (not in the pages).

Method: documentation only; no commands were run.
