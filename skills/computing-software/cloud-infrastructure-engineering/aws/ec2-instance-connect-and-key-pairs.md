---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-instance-connect-and-key-pairs
name: ec2-instance-connect-and-key-pairs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, instance-connect, ec2-instance-connect-endpoint, key-pairs, ssh, bastion, access-management]
level: practitioner
status: docs-checked
description: "Give SSH access without long-lived keys: EC2 Instance Connect pushed keys, EC2 Instance Connect Endpoint for private subnets, IAM conditions, and managing or rotating key pairs."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-set-up.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-configure-IAM-role.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-using-eice.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/permissions-for-ec2-instance-connect-endpoint.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/eice-quotas.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/delete-key-pair.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 Instance Connect, the Endpoint, and key pairs

## 1. Instance Connect (temporary keys)
The CLI pushes your public key into instance metadata for **60 seconds**; the
`ec2-instance-connect` package on the instance lets sshd accept it.
```bash
aws ec2-instance-connect ssh --instance-id i-123 --os-user ec2-user      # does push + ssh
# or manually:
aws ec2-instance-connect send-ssh-public-key --instance-id i-123 --instance-os-user ec2-user \
  --ssh-public-key file://~/.ssh/id_ed25519.pub
ssh ec2-user@<IP>
```
EC2 Instance Connect is preinstalled on Amazon Linux 2 2.0.20190618 or later and Ubuntu 20.04 or later AMIs
(see "Install EC2 Instance Connect" for other versions). It accepts RSA and ED25519 keys. IAM controls who can
push to which instance/user:
```json
{"Effect": "Allow", "Action": "ec2-instance-connect:SendSSHPublicKey",
 "Resource": "arn:aws:ec2:<REGION>:<ACCOUNT_ID>:instance/*",
 "Condition": {"StringEquals": {"aws:ResourceTag/Team": "${aws:PrincipalTag/Team}", "ec2:osuser": "ec2-user"}}}
```

## 2. EC2 Instance Connect Endpoint (no bastion, no public IP)
```bash
aws ec2 create-instance-connect-endpoint --subnet-id subnet-private-a --security-group-ids sg-eice --preserve-client-ip
aws ec2-instance-connect ssh --instance-id i-123 --connection-type eice
aws ec2-instance-connect open-tunnel --instance-id i-123 --remote-port 3389 --local-port 13389   # RDP etc.
```
- Quotas (not adjustable): 1 endpoint per VPC, 1 per subnet, 5 per Region, 20 concurrent connections per endpoint.
  Target security groups must allow inbound SSH (or RDP) from the endpoint's security group, or from the
  client IP when client IP preservation is on.
- IAM: `ec2-instance-connect:OpenTunnel` with conditions on `ec2-instance-connect:remotePort` and
  `ec2-instance-connect:maxTunnelDuration` (pass `--max-tunnel-duration` when the policy sets it); creating the
  endpoint needs `ec2:CreateInstanceConnectEndpoint`. Connections are logged to CloudTrail.
- No additional charge for the endpoint, except cross-AZ data transfer when the target is in another AZ.
  No SSM Agent is needed; connecting with an ephemeral key needs EC2 Instance Connect installed on the instance,
  while connecting with your own key pair needs only sshd.

## 3. Key pairs
```bash
aws ec2 create-key-pair --key-name ops-2026 --key-type ed25519 --query KeyMaterial --output text > ops-2026.pem
aws ec2 import-key-pair --key-name jo-laptop --public-key-material fileb://~/.ssh/id_ed25519.pub
aws ec2 describe-key-pairs --query 'KeyPairs[].[KeyName,KeyType,CreateTime]'
```
- EC2 stores only the public key. Deleting the key pair in EC2 does **not** remove the public key from
  instances that already have it, and the private key still works. Do not delete a key pair that an Auto Scaling
  launch template still names, or replacement launches fail.
- Rotation: push new keys via SSM Run Command/config management, remove old lines, then
  delete the EC2 key pair. Prefer launching without a key and using Instance Connect/SSM.

## Gotchas
- Windows instances use the key pair to decrypt the initial Administrator password (`get-password-data`); ED25519
  keys are not supported for Windows instances, so use RSA.
- Instance Connect needs network reachability to port 22 (public IP or EICE/VPN).

## Verify
- [ ] Engineers connect with `aws ec2-instance-connect ssh --connection-type eice` to private instances; no bastion exists.
- [ ] CloudTrail shows `SendSSHPublicKey`/`OpenTunnel` with the user's identity.
- [ ] Inventory of `authorized_keys` shows no departed users' keys.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide pages on EC2 Instance Connect (set up, prerequisites, methods, IAM role configuration), EC2 Instance Connect Endpoint (overview, create, permissions, quotas, connect), Create a key pair and Delete your key pair; botocore EC2 model (CreateInstanceConnectEndpoint PreserveClientIp, KeyType rsa/ed25519).
Confirmed: 60-second key lifetime, SendSSHPublicKey with ec2:osuser, OpenTunnel with remotePort and maxTunnelDuration conditions, --connection-type eice, quotas of 1/1/5/20, no endpoint charge, key deletion semantics, ED25519 unsupported on Windows.
Corrected: the preinstalled-AMI statement (the page lists Amazon Linux 2 2.0.20190618+ and Ubuntu 20.04+, not Amazon Linux 2023) and the endpoint scoping, which was stated loosely.
Removed: the comparison with Session Manager.

Method: documentation only; no commands were run.
