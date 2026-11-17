---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-in-a-vpc-networking
name: lambda-in-a-vpc-networking
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, lambda-in-vpc, hyperplane-eni, lambda-vpc-networking, nat-gateway, vpc-endpoints]
level: practitioner
status: docs-checked
description: "Attach a Lambda function to a VPC with the right subnets, security groups, IAM permissions and internet path, and understand Hyperplane ENI lifecycle and condition keys."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda in a VPC

**Goal:** a function reaches private resources (RDS, ElastiCache, internal APIs) and, if needed, still reaches the internet.

## Configure
```bash
aws lambda update-function-configuration --function-name my-function \
  --vpc-config SubnetIds=subnet-a,subnet-b,SecurityGroupIds=sg-0123
```
- Attach through the private subnets that contain the resources. A public subnet gives no internet access and no public IP.
- To detach: `--vpc-config SubnetIds=[],SecurityGroupIds=[]`.
- Functions cannot connect directly to a VPC with dedicated instance tenancy; peer it to a default-tenancy VPC.
- Every function also runs inside a Lambda-managed VPC you cannot see; attaching to your VPC does not change that.

## IAM
- Execution role: attach the managed policy `AWSLambdaVPCAccessExecutionRole`, or allow on `"Resource": "*"`: `ec2:CreateNetworkInterface`, `ec2:DescribeNetworkInterfaces`, `ec2:DescribeSubnets`, `ec2:DeleteNetworkInterface`, `ec2:AssignPrivateIpAddresses`, `ec2:UnassignPrivateIpAddresses`. The console adds the policy automatically when you create a function with a VPC. The role needs these only to create the ENIs, not to invoke.
- The identity doing the attach needs `ec2:DescribeSecurityGroups`, `ec2:DescribeSubnets`, `ec2:DescribeVpcs`, `ec2:GetSecurityGroupsForVpc`.
- These EC2 permissions are implicitly available to your function code too. To block that, add a Deny on those actions with an `ArnEquals` condition on `lambda:SourceFunctionArn`, which matches only calls made by function code (the page's example also denies `ec2:DetachNetworkInterface`).
- Condition keys on `lambda:CreateFunction` and `lambda:UpdateFunctionConfiguration`: `lambda:VpcIds`, `lambda:SubnetIds`, `lambda:SecurityGroupIds`. Deny when `lambda:VpcIds` is `Null` to force VPC-connected functions.

## Internet access
By default functions have public internet access; once attached to a VPC they reach only what the VPC can reach. Configure the VPC for internet access (the page points to its "Enable internet access for VPC-connected Lambda functions" topic).

## IPv6
Off by default. Enable with `--vpc-config Ipv6AllowedForDualStack=true` (or the console option). All selected subnets must be dual-stack; IPv6-only subnets, and functions not attached to a VPC, do not get outbound IPv6.

## Hyperplane ENIs
- Lambda creates a Hyperplane ENI per subnet and security group combination; other functions in the account with the same combination share it, so reusing combinations avoids new ENIs.
- Each ENI supports up to 65,000 connections/ports; Lambda adds ENIs automatically beyond that.
- A new function stays `Pending` (not invocable) while the ENI is created, which can take several minutes. For existing functions you cannot do operations such as creating versions or updating code meanwhile, but you can invoke previous versions.
- After 14 idle days Lambda reclaims unused ENIs and sets the function `Inactive`; the next invocation fails and the function returns to `Pending` until an ENI is ready. Do not design around ENI persistence.
- After removing the VPC config, Lambda needs up to 20 minutes to delete the ENI, and only if no other function or version uses it. It uses the execution role to delete it, so deleting the role first leaves the ENI for you to delete manually.

## Verify
`aws lambda get-function-configuration --function-name my-function --query VpcConfig`.

## Method
Rewritten from the cited Lambda Developer Guide page only. The earlier NAT/endpoint specifics, RDS Proxy advice and ENI quota troubleshooting were not on the page and were removed.

## Checked
Checked 2026-11-08 against the cited Lambda page "Giving Lambda functions access to resources in an Amazon VPC".
Method: docs-only read of cited pages, 2026-11-08
