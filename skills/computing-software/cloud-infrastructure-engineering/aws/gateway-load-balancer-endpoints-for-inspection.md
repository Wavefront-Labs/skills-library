---
id: computing-software.cloud-infrastructure-engineering.aws.gateway-load-balancer-endpoints-for-inspection
name: gateway-load-balancer-endpoints-for-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, gateway-load-balancer, gwlb-endpoint, traffic-inspection, geneve, ingress-routing]
level: advanced
status: docs-checked
description: "Insert third-party firewalls inline with Gateway Load Balancer and GWLB endpoints: GENEVE targets, edge route tables, symmetric routing and appliance mode."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-load-balancer-endpoints.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/getting-started.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway Load Balancer endpoints for inspection

## 1. Provider side (security VPC)
```bash
GWLB=$(aws elbv2 create-load-balancer --name fw-gwlb --type gateway --subnets subnet-fw-a subnet-fw-b --query 'LoadBalancers[0].LoadBalancerArn' --output text)
TG=$(aws elbv2 create-target-group --name fw-tg --protocol GENEVE --port 6081 --vpc-id vpc-sec \
  --health-check-protocol TCP --health-check-port 80 --target-type instance --query 'TargetGroups[0].TargetGroupArn' --output text)
aws elbv2 register-targets --target-group-arn $TG --targets Id=i-fw1 Id=i-fw2
aws elbv2 create-listener --load-balancer-arn $GWLB --default-actions Type=forward,TargetGroupArn=$TG
aws ec2 create-vpc-endpoint-service-configuration --gateway-load-balancer-arns $GWLB --no-acceptance-required
```
Appliances and the GWLB exchange traffic over GENEVE on port 6081; the appliances' security groups must allow UDP 6081.

## 2. Consumer side: endpoints and routes (distributed ingress)
```bash
aws ec2 create-vpc-endpoint --vpc-endpoint-type GatewayLoadBalancer \
  --service-name com.amazonaws.vpce.<REGION>.vpce-svc-0abc --vpc-id vpc-app --subnet-ids subnet-gwlbe-a
```
| Route table | Destination | Target |
|---|---|---|
| IGW edge table (associated with the IGW) | app subnet CIDR | GWLB endpoint (same AZ) |
| GWLBE subnet | 0.0.0.0/0 | IGW |
| App subnet | 0.0.0.0/0 | GWLB endpoint (same AZ) |
```bash
aws ec2 associate-route-table --route-table-id rtb-edge --gateway-id igw-0abc
```

## 3. Centralized via Transit Gateway
Spoke traffic goes TGW to inspection VPC to GWLBE; enable **appliance mode** (`ApplianceModeSupport`)
on the inspection VPC's TGW attachment so flows stay symmetric.

## Gotchas
- GWLB endpoints are zonal: create one per Availability Zone and send each AZ's traffic to the endpoint in the same AZ.
- GWLB keeps flow stickiness to one appliance using 5-tuple (default), 3-tuple or 2-tuple.

## Verify
- [ ] Firewall logs show both directions of a test flow.
- [ ] Target group shows the appliances healthy.

## Checked
2026-10-28. Confirmed against the Gateway Load Balancer pages "What is a Gateway Load Balancer" and "Getting started" (GENEVE on 6081, UDP 6081 in security groups, 5/3/2-tuple stickiness, route table layout for IGW, application subnet and endpoint subnet, endpoints are zonal, one per AZ), the PrivateLink GWLB endpoint page (same-AZ recommendation) and botocore (elbv2 GENEVE protocol, ec2 ApplianceModeSupport; CLI flags verified by check_commands.py). Removed unconfirmed claims: 8,500-byte jumbo frames, target failover rebalancing behaviour, the UnHealthyHostCount metric name, and the claim that appliance mode pins a flow to one AZ.
Method: documentation only; no commands were run.
