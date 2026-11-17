---
id: computing-software.cloud-infrastructure-engineering.aws.snowball-edge-compute-ec2
name: snowball-edge-compute-ec2
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, snowball-edge, snowball-compute, ec2-on-snow, snow-family, edge-computing, disconnected-environments, opshub, snowballedge-cli, sbe-instances, eks-anywhere-on-snow, ami-import]
level: advanced
status: docs-checked
description: "Run EC2-compatible instances on Snowball Edge at disconnected edge sites: order with AMIs, unlock, launch via the local EC2 endpoint, networking, storage and limits."
sources: ["https://docs.aws.amazon.com/snowball/latest/developer-guide/using-ec2.html", "https://docs.aws.amazon.com/snowball/latest/developer-guide/using-client-commands.html", "https://docs.aws.amazon.com/snowball/latest/developer-guide/ec2-ami-import-cli.html", "https://docs.aws.amazon.com/snowball/latest/developer-guide/network-config-ec2.html", "https://aws.amazon.com/snowball/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowball Edge compute: EC2 on Snow

**Goal:** applications run on rugged AWS hardware in places with little or no connectivity
using the familiar EC2 API locally, then results move back to AWS when the device returns.

## 0. Availability
AWS's Snowball page carries an end-of-support notice: on 31 December 2026 AWS discontinues support for Snowball
Edge Storage Optimized and Compute Optimized devices in all AWS commercial Regions (GovCloud and ADC customers with
active jobs are not affected), and the Snow Console is no longer accessible after that date. Check the notice
before planning new work.

## 1. Order with compute in mind
- EC2-compatible instances use the `sbe1` (Storage Optimized devices), `sbe-c` (Compute Optimized) and `sbe-g`
  (GPU) instance types; they are unique to Snowball Edge and launch from AMIs.
- AMIs can be added to the job, or imported on-device from an image file in S3 with `import-snapshot`
  against the device's EC2-compatible endpoint (the Snowball Edge Developer Guide covers the full AMI import
  procedure, including the snapshot-bucket IAM policy).

## 2. Unlock and access
```bash
snowballEdge configure --profile snow          # endpoint, manifest, unlock code
snowballEdge list-access-keys && snowballEdge get-secret-access-key --access-key-id <KEY>
```
`list-access-keys` and `get-secret-access-key` return the credentials of the account's admin user on the device.
The AWS CLI then talks to the device's EC2-compatible endpoint; the guide's examples use
`--endpoint http://<device-ip>:8008 --region snow --profile <profile>`:
```bash
aws ec2 run-instances --image-id <IMAGE_ID> --instance-type sbe-c.large \
  --endpoint http://<device-ip>:8008 --region snow --profile snow
```
Device image and instance IDs are prefixed `s.` (for example `s.ami-...`, `s.i-...`). AWS OpsHub can unlock the
device, import images and launch instances without the CLI.

## 3. Networking
- After launch you must give the instance an IP address through a network interface. A **virtual network interface
  (VNI)** is the standard one and you need one per EC2-compatible instance:
```bash
snowballEdge create-virtual-network-interface --physical-network-interface-id s.ni-xxxx --ip-address-assignment STATIC --static-ip-address-configuration IpAddress=192.168.1.50,Netmask=255.255.255.0
```
- A **direct network interface (DNI)** gives instances layer 2 access for multicast, transitive routing and
  load balancing; DNIs attach to RJ45, SFP or QSFP ports, up to 63 per physical port.
- Security groups can control network traffic on the device (see the guide's security groups section).

## 4. Lifecycle
- When you return the device, import-job data is imported to S3; otherwise AWS completely erases the device.
  Copy anything you need first.
- Configure NTP (the Snowball Edge client has `update-time-servers` and `describe-time-sources`; usable while the
  device is locked or unlocked). Providing a secure NTP server is your responsibility.

## Verify
- [ ] `snowballEdge describe-device` shows the device unlocked; `aws ec2 describe-instances --endpoint ...` lists the instance running.
- [ ] Instance reachable on the local network via its VNI address.
- [ ] Data written to device storage is checksummed before return.

## Checked

2026-10-28. Confirmed against the Snowball Edge Developer Guide pages using-ec2, using-client-commands, ec2-ami-import-cli and network-config-ec2, and the AWS Snowball product page end-of-support notice: instance type families, EC2-compatible endpoint on port 8008 over HTTP with `--region snow`, `s.`-prefixed IDs, access key commands, VNI and DNI (63 per port, port types), OpsHub, complete erasure on return, NTP commands.
Removed or corrected: the 8243 HTTPS endpoint and AWS_CA_BUNDLE certificate flow, EKS Anywhere and marketplace AMI claims, Outposts/partner suggestions, NIST sanitisation wording, per-day lease terms, `sbp1` volume types, "no autoscaling/ELB" and certificate-expiry gotchas, and the associate-address step.
Method: documentation only; no commands were run.
