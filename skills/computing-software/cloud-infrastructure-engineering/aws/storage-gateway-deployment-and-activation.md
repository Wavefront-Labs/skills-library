---
id: computing-software.cloud-infrastructure-engineering.aws.storage-gateway-deployment-and-activation
name: storage-gateway-deployment-and-activation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, storage-gateway, gateway-activation, gateway-vm, hybrid-storage]
level: practitioner
status: docs-checked
description: "Deploy a Storage Gateway VM (VMware, Hyper-V, KVM or EC2), size its disks, open the right ports, obtain an activation key and activate it, including via VPC endpoint."
sources: ["https://docs.aws.amazon.com/filegateway/latest/files3/Requirements.html", "https://docs.aws.amazon.com/filegateway/latest/files3/get-activation-key.html", "https://docs.aws.amazon.com/storagegateway/latest/APIReference/API_ActivateGateway.html", "https://docs.aws.amazon.com/storagegateway/latest/vgw/Resource_Ports.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway appliance deployment and activation

## 1. Deploy
- Host: VMware ESXi 7.0 or 8.0 (OVA), Microsoft Hyper-V 2019, 2022 or 2025, Linux KVM, Nutanix AHV, or an EC2 AMI (x86 instance, at least xlarge; Graviton is not supported) for in-cloud gateways.
- Minimum for S3 File Gateway: 4 virtual processors, 16 GiB reserved RAM, 80 GiB for the VM image; plus a
  **cache disk** of at least 150 GiB (maximum 64 TiB). Volume and Tape gateways have their own hardware
  and upload buffer requirements in their user guides.
- At least 100 Mbps to AWS to download, activate and update the gateway. DNS and an NTP source must work; a static IP or DHCP reservation is advisable. Network settings are in the gateway local console.

## 2. Network ports
| Direction | Port | Purpose |
|---|---|---|
| Gateway to AWS | TCP 443 | service and S3 endpoints listed on the requirements page (or a VPC endpoint) |
| Gateway to DNS and NTP | 53 (TCP and UDP); 123 (UDP) | name resolution and time sync |
| Your browser/CLI host to gateway | TCP 80 | one-time activation key retrieval |
| Clients to gateway | 2049, 111, 20048 (NFS); 445 (SMB); 3260 (iSCSI) | data |

## 3. Activation key
```bash
curl -s "http://<GATEWAY_IP>/?activationRegion=<REGION>&no_redirect"
# private activation through an interface endpoint:
curl -s "http://<GATEWAY_IP>/?activationRegion=<REGION>&vpcEndpoint=<VPCE_DNS_NAME>&no_redirect"
```
The output carries the activation key; unused keys expire after 30 minutes. A missing or misspelled Region value silently defaults to us-east-1.

## 4. Activate and add disks
```bash
GW=$(aws storagegateway activate-gateway --activation-key <KEY> --gateway-name dc1-files \
  --gateway-timezone GMT --gateway-region <REGION> --gateway-type FILE_S3 --query GatewayARN --output text)
aws storagegateway list-local-disks --gateway-arn $GW
aws storagegateway add-cache --gateway-arn $GW --disk-ids <DISK_ID>
```
Types: `FILE_S3`, `FILE_FSX_SMB`, `STORED`, `CACHED`, `VTL`. The type cannot be changed after activation, and Amazon FSx File Gateway (`FILE_FSX_SMB`) is no longer available to new customers.

## Verify
- [ ] `describe-gateway-information` reports the expected `GatewayType`, `GatewayState` and VPC endpoint.
- [ ] Gateway health and `CachePercentUsed` metrics appear in CloudWatch.

## Checked

Checked 2026-10-27 against the S3 File Gateway User Guide pages File Gateway setup requirements and Getting an activation key, the Volume Gateway requirements page, the Storage Gateway API reference for ActivateGateway, and the botocore storagegateway model.
Confirmed: supported hypervisors (VMware ESXi 7.0 or 8.0, Hyper-V 2019/2022/2025, KVM, Nutanix AHV 10.0.1.1 or later) and EC2 AMI rules; S3 File Gateway minimums of four virtual processors, 16 GiB RAM, 80 GiB disk, cache 150 GiB to 64 TiB, 100 Mbps; ports 80 (activation), 443, 53, 123, NFS 111, 2049 and 20048, SMB 445, iSCSI 3260 (Volume Gateway guide); activation key curl forms including vpcEndpoint and no_redirect, 30-minute expiry and us-east-1 default; ActivateGateway GatewayType values STORED, CACHED, VTL, FILE_S3, FILE_FSX_SMB, type fixed after activation, FSx File Gateway closed to new customers; AddCache and ListLocalDisks parameters. Removed the unconfirmed local console login and CloudFront requirement.

Method: documentation only; no commands were run.
