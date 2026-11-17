---
id: computing-software.cloud-infrastructure-engineering.aws.nat-instance-low-cost-egress
name: nat-instance-low-cost-egress
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-instance, fck-nat, source-dest-check, iptables, cost-optimization, egress, graviton]
level: practitioner
status: docs-checked
description: "Run a NAT instance (e.g. fck-nat on Graviton) instead of a NAT gateway for dev or low-traffic VPCs: source/dest check, iptables masquerade, ASG self-healing and limits."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/VPC_NAT_Instance.html", "https://docs.aws.amazon.com/vpc/latest/userguide/work-with-nat-instances.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html", "https://fck-nat.dev/stable/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT instance as low-cost egress

**When:** sandbox/dev VPCs and low-volume workloads where you accept managing the instance yourself.
AWS recommends NAT gateways (better availability and bandwidth, less administration), and the AWS-provided NAT AMI is built on the Amazon Linux AMI 2018.03, which reached end of maintenance support on 31 December 2023, so build your own NAT AMI from a current Amazon Linux.

## 1. Build one by hand (Amazon Linux 2023)
```bash
# on the instance (public subnet, public IP/EIP)
sudo yum install -y iptables-services
sudo systemctl enable iptables && sudo systemctl start iptables
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/custom-ip-forwarding.conf
sudo sysctl -p /etc/sysctl.d/custom-ip-forwarding.conf
sudo /sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE   # use your primary interface name
sudo /sbin/iptables -F FORWARD
sudo service iptables save
```
```bash
# from your workstation
aws ec2 modify-instance-attribute --instance-id i-nat --no-source-dest-check
aws ec2 create-route --route-table-id rtb-private-a --destination-cidr-block 0.0.0.0/0 --network-interface-id eni-nat
```
Every EC2 instance performs source/destination checks by default, so they **must be disabled** on the NAT instance.
The NAT instance must be in a public subnet and have a public IP or Elastic IP. Security group: allow inbound from the private subnets; outbound to the internet.

## 2. Use fck-nat instead of hand-rolling
fck-nat is a community project (not an AWS product) that publishes ready-made public NAT AMIs for arm64 and x86_64 built on Amazon Linux 2023; list them with
`aws ec2 describe-images --owners 568608671756 --filters 'Name=name,Values=fck-nat-al2023-*'`. You still need a security group, disabled source/destination checks and a route table entry.
Its deployment guide covers CDK, Terraform, CloudFormation (an Auto Scaling group using the AMI) and manual setup, and a high-availability mode; read it for the current options.

## 3. Limits vs NAT gateway
| | NAT instance | NAT gateway |
|---|---|---|
| HA | you script failover between instances | managed, redundant within the AZ |
| Bandwidth | depends on the instance type | scales up to 100 Gbps |
| Cost basis | instances, by type and size | number of gateways, duration and data processed |
| Security groups | yes | no |
| Patching | yours | AWS |
| Idle timeout | sends a FIN to close the connection | returns an RST |
| IP fragmentation | reassembles UDP, TCP and ICMP | forwards fragmented UDP only |

## Gotchas
- NAT instance throughput is bounded by the instance type, so size it for the workload.
- A replacement instance needs the route (and Elastic IP) moved to it; until then the route to the old instance is a blackhole.
- Moving from a NAT instance to a NAT gateway drops current connections.

## Verify
- [ ] `aws ec2 describe-instance-attribute --instance-id i-nat --attribute sourceDestCheck` → false.
- [ ] From a private instance: `curl -s https://checkip.amazonaws.com` returns the NAT instance's EIP.
- [ ] Terminating the NAT instance: your failover mechanism restores egress within the time you require.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (NAT instances, NAT instance tutorial, compare NAT gateways and NAT instances), the fck-nat documentation (fck-nat.dev) and the botocore EC2 model.
- The AMI end-of-support note, public-subnet and public IP requirement, source/destination check requirement, the iptables, `ip_forward` and MASQUERADE steps (the AWS tutorial uses `yum` and `eth0`) and the comparison table rows confirmed on the AWS pages.
- fck-nat AMI naming, owner ID, supported architectures and Amazon Linux 2023 base confirmed on its site; it is third-party and its pricing figures are not repeated here.
- Removed the NAT gateway processing price, the t4g.nano cost claim, the static-ENI Auto Scaling design and the CDK construct names, which no AWS page confirms.

Method: documentation only; no commands were run.
