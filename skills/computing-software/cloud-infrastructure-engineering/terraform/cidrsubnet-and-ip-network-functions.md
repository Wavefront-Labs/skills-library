---
id: computing-software.cloud-infrastructure-engineering.terraform.cidrsubnet-and-ip-network-functions
name: cidrsubnet-and-ip-network-functions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, cidrsubnet, cidrsubnets, cidrhost, cidrnetmask, ip-functions, subnet-planning, ipam]
level: practitioner
status: verified
description: "Carve address plans with cidrsubnet, cidrsubnets, cidrhost and cidrnetmask: newbits arithmetic, stable per-AZ allocation, IPv6, and avoiding renumbering."
sources: ["https://developer.hashicorp.com/terraform/language/functions/cidrsubnet", "https://developer.hashicorp.com/terraform/language/functions/cidrsubnets", "https://developer.hashicorp.com/terraform/language/functions/cidrhost", "https://registry.terraform.io/modules/hashicorp/subnets/cidr/latest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP network functions

## cidrsubnet(prefix, newbits, netnum)
Adds `newbits` to the prefix length and picks block number `netnum`.
```hcl
cidrsubnet("10.0.0.0/16", 8, 0)    # 10.0.0.0/24
cidrsubnet("10.0.0.0/16", 8, 1)    # 10.0.1.0/24
cidrsubnet("10.0.0.0/16", 4, 15)   # 10.0.240.0/20
```
`netnum` must be < 2^newbits.

## Stable per-AZ plan
```hcl
locals {
  azs = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  private = { for i, az in local.azs : az => cidrsubnet(var.vpc_cidr, 4, i) }        # /20s at 0-2
  public  = { for i, az in local.azs : az => cidrsubnet(var.vpc_cidr, 8, 240 + i) } # /24s high
}
```
Use fixed offsets per tier so adding an AZ appends rather than renumbers. Never
derive `netnum` from a list that can be reordered.

## cidrsubnets — consecutive, mixed sizes
```hcl
cidrsubnets("10.1.0.0/16", 4, 4, 8, 8)
# ["10.1.0.0/20","10.1.16.0/20","10.1.32.0/24","10.1.33.0/24"]
```
Changing an earlier size shifts later ones — append only. The
`hashicorp/subnets/cidr` module wraps this with names.

## Hosts and masks
```hcl
cidrhost("10.0.1.0/24", 10)       # 10.0.1.10   (reserved IPs, DNS resolver = +2 in AWS)
cidrhost("10.0.1.0/24", -2)       # 10.0.1.254  (negative counts from the end)
cidrnetmask("10.0.1.0/24")        # 255.255.255.0 (IPv4 only)
```

## IPv6
```hcl
cidrsubnet(aws_vpc.main.ipv6_cidr_block, 8, 1)   # /56 -> /64
```
Values from resources are unknown until apply — fine for arguments, not for keys.

## Gotchas
- Overlaps are not detected; validate with a precondition or plan on paper.
- AWS reserves 5 IPs per subnet; Azure 5; GCP 4 — size accordingly.
- Changing a subnet's CIDR forces replacement of the subnet and everything in it.
- For org-wide allocation use IPAM (`aws_vpc_ipam_pool_cidr_allocation`) rather than spreadsheets.

## Verify
- [ ] `terraform console` → `local.private` prints non-overlapping blocks inside the VPC CIDR.
- [ ] Adding an AZ to the list plans only new subnets.

## Checked
- Terraform 1.9.8 `terraform console`: cidrsubnet, cidrsubnets, cidrhost (including negative host numbers), cidrnetmask (IPv4 only; IPv6 errors), IPv6 /56 to /64 subnets, netnum out-of-range error, per-AZ maps, element wraparound and index error all matched this text.
- Docs fetched: AWS reserves five addresses per subnet; Azure reserves five; Google Cloud reserves four in primary ranges (network, gateway, second-to-last, broadcast); registry module `hashicorp/subnets/cidr` and the `aws_vpc_ipam_pool_cidr_allocation` page exist.
