---
id: computing-software.cloud-infrastructure-engineering.aws.eni-secondary-ips-and-elastic-ips
name: eni-secondary-ips-and-elastic-ips
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, elastic-network-interface, secondary-private-ip, elastic-ip-management, eni]
level: practitioner
status: docs-checked
description: "Manage ENIs, secondary private IPs and Elastic IPs: per-type limits, OS configuration, moving IPs for failover, source/dest check and EIP recovery."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/MultipleIP.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html", "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AllocateAddress.html", "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssignPrivateIpAddresses.html", "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyAddressAttribute.html", "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyNetworkInterfaceAttribute.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ENIs, secondary private IPs and Elastic IPs

## 1. Limits come from the instance type
```bash
aws ec2 describe-instance-types --instance-types <INSTANCE_TYPE> \
  --query 'InstanceTypes[].NetworkInfo.{enis:MaximumNetworkInterfaces,ipv4PerEni:Ipv4AddressesPerInterface}'
```

## 2. Secondary IPs and extra ENIs
```bash
aws ec2 assign-private-ip-addresses --network-interface-id eni-0abc --secondary-private-ip-address-count 2
aws ec2 assign-private-ip-addresses --network-interface-id eni-0abc --private-ip-addresses 10.0.1.50 --allow-reassignment
ENI=$(aws ec2 create-network-interface --subnet-id subnet-0abc --groups sg-0abc --query NetworkInterface.NetworkInterfaceId --output text)
aws ec2 attach-network-interface --network-interface-id $ENI --instance-id i-0abc --device-index 1
```
- Check the OS network configuration after assigning IPs or attaching an ENI; not every distribution configures them automatically.
- `--allow-reassignment` lets an IP already assigned to another network interface or instance be reassigned to this ENI: the classic floating-IP failover.
- Source/destination checks are enabled by default and must be disabled if the instance runs NAT, routing or firewall services: `aws ec2 modify-network-interface-attribute --network-interface-id eni-0abc --no-source-dest-check`.
- Set the attachment's `DeleteOnTermination` explicitly (`modify-network-interface-attribute --attachment`).

## 3. Elastic IPs
```bash
EIP=$(aws ec2 allocate-address --domain vpc --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=partner-egress}]' --query AllocationId --output text)
aws ec2 associate-address --allocation-id $EIP --network-interface-id eni-0abc --private-ip-address 10.0.1.50
aws ec2 disassociate-address --association-id eipassoc-0abc
aws ec2 release-address --allocation-id $EIP
```
- Release Elastic IPs you no longer use; see the VPC pricing page for public IPv4 charges.
- Accidentally released? `aws ec2 allocate-address --domain vpc --address 203.0.113.10` may recover it; you cannot recover it once it is allocated to another AWS account.
- Reverse DNS: `aws ec2 modify-address-attribute --allocation-id $EIP --domain-name mail.example.com` (see "Using reverse DNS for email applications" in the EC2 User Guide for requirements).

## Verify
- [ ] `ip addr` on the instance lists every assigned private IP.
- [ ] After reassigning the IP to the standby ENI, traffic to it reaches the standby.

## Checked

Checked 2026-10-28 against the EC2 API reference (AllocateAddress, AssignPrivateIpAddresses, ModifyAddressAttribute, ModifyNetworkInterfaceAttribute), the EC2 User Guide network interface pages and the EC2 service model (botocore).
- Confirmed: `MaximumNetworkInterfaces` and `Ipv4AddressesPerInterface` in DescribeInstanceTypes, `AllowReassignment` semantics, `SecondaryPrivateIpAddressCount`, source/destination check default and when to disable it, attachment `DeleteOnTermination`, EIP recovery via `Address` and its limit, `DomainName` on ModifyAddressAttribute.
- Corrected: reassignment works from any other network interface or instance, not only within a subnet.
- Removed: Amazon Linux 2023 auto-configuration, policy-routing and same-AZ claims, the hourly billing statement and the forward-record requirement.

Method: documentation only; no commands were run.
