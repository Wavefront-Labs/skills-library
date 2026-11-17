---
id: computing-software.devops-ci-cd.earthly.earthly-byoc-aws-install
name: earthly-byoc-aws-install
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, byoc, aws, terraform, cloudformation, earthly-cloud-install, tailscale, satellites]
level: advanced
status: docs-checked
description: "Install Earthly Bring Your Own Cloud satellites in AWS via Terraform, CloudFormation or manual earthly cloud install, then add Tailscale networking and launch a satellite."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/byoc/byoc.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/byoc/aws/requirements.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/byoc/aws/terraform.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/byoc/aws/cloudformation.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/byoc/aws/manual.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/byoc/vpn/tailscale.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BYOC satellites on AWS

BYOC (experimental, Enterprise plan) is Earthly-managed satellites running in your own infrastructure. Only `us-west-2` is supported. You need a VPC and a subnet (note its CIDR), and clients (CI runners, workstations) must reach the satellites directly, with AWS-internal DNS names resolvable.

## Option 1: Terraform
`byoc.tf` in an empty directory:
```hcl
module "byoc" {
  source  = "earthly/byoc/aws"
  version = "0.0.10"

  cloud_name = "my-cloud"
  subnet = "subnet-0123456789abcde01"
}

output "my-cloud" {
  value = module.byoc.automatic_installation
}
```
Run `terraform init && terraform apply`, then `earthly cloud install --via terraform --name my-cloud`. For automatic install, run it in the module's directory and export `automatic_installation`; the output name is the `--name`. Optional input `ssh_public_key` (otherwise a key is generated and the private key is an output).

## Option 2: CloudFormation
Launch the template from the quick-create link on the cloudformation page (us-west-2). The stack name becomes the installation name. Parameters: Subnet, VPC, Ingress CIDR Block (e.g. a Tailscale subnet router IP). It creates two IAM policies and an SSH key `<stack-name>-satellite-key` (private key in SSM Parameter Store under `/ec2/keypair/<key-id>`). Wait for `CREATE_COMPLETE`, then the page gives `earthly cloud install --via terraform --name <stack-name>`.

## Option 3: manual
```shell
earthly cloud install --name <name> --aws-account-id <aws-account-id> --aws-region <aws-region> --aws-security-group-id <aws-security-group-id> --aws-ssh-key-name <aws-ssh-key-id> --aws-subnet-id <aws-subnet-id> --aws-instance-profile-arn <aws-instance-profile-arn> --aws-earthly-access-role-arn <aws-earthly-access-role-arn>
```
Security group ingress from the subnet: TCP 22, 8372 (BuildKit), 9000 (Prometheus node_exporter). CloudWatch log group: `/earthly/satellites/<cloud-name>`. Earthly's access role trusts Earthly's `compute-production` role (full ARN on the manual install page) with `sts:AssumeRole`.

## Networking and test drive
Tailscale: use a subnet router, add Split DNS for `<aws-region>.compute.internal` pointing to `x.x.0.2` (x from the VPC CIDR), and userspace networking in Kubernetes or GHA runners (needs a Global nameserver).
```shell
earthly cloud list
earthly satellite launch --cloud <name> my-byoc-sat
earthly cloud use <name>       # default for the whole org
```
A status of `Green` means the install worked; `earthly-cloud` is the built-in Earthly-managed cloud and `earthly cloud use earthly-cloud` switches back.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: cloud/satellites/byoc/byoc.md, cloud/satellites/byoc/aws/requirements.md, cloud/satellites/byoc/aws/terraform.md, cloud/satellites/byoc/aws/cloudformation.md, cloud/satellites/byoc/aws/manual.md, cloud/satellites/byoc/vpn/tailscale.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: removed a literal AWS account ARN and pointed to the manual install page for it.

Method: documentation only; no commands were run.
