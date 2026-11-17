---
id: computing-software.cloud-infrastructure-engineering.aws.reachability-analyzer-and-network-access-analyzer
name: reachability-analyzer-and-network-access-analyzer
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, reachability-analyzer, reachability-path, network-access-analyzer, path-analysis, network-troubleshooting, compliance]
level: practitioner
status: docs-checked
description: "Prove connectivity with Reachability Analyzer path analysis (explanation codes, cross-account) and audit unintended access with Network Access Analyzer scopes."
sources: ["https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html", "https://docs.aws.amazon.com/vpc/latest/reachability/explanation-codes.html", "https://docs.aws.amazon.com/vpc/latest/network-access-analyzer/what-is-network-access-analyzer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reachability Analyzer and Network Access Analyzer

Both analyse **configuration**: one answers "can A reach B and if not,
which hop blocks it?", the other answers "what can reach what, against my policy?".

## 1. Reachability Analyzer: one path
```bash
PATH_ID=$(aws ec2 create-network-insights-path --source i-0app --destination i-0db \
  --protocol tcp --destination-port 5432 --query NetworkInsightsPath.NetworkInsightsPathId --output text)
AN=$(aws ec2 start-network-insights-analysis --network-insights-path-id $PATH_ID \
  --query NetworkInsightsAnalysis.NetworkInsightsAnalysisId --output text)
aws ec2 describe-network-insights-analyses --network-insights-analysis-ids $AN \
  --query 'NetworkInsightsAnalyses[0].[Status,NetworkPathFound,Explanations[].ExplanationCode]'
```
- Explanation codes name the blocker: `ENI_SG_RULES_MISMATCH`, `NO_ROUTE_TO_DESTINATION`,
  `SUBNET_ACL_RESTRICTION`, `TGW_RTB_NO_ROUTE`... with the exact resource ID.
- When the destination is reachable you get hop-by-hop details; when not, the blocking component
  (security group, network ACL, route table, load balancer) is identified.

Keep paths as reusable "connectivity tests": re-run after every network change in CI.

## 2. Network Access Analyzer: policy at scale
Define a **scope** of access you do *not* want, then list findings:
```bash
aws ec2 create-network-insights-access-scope --match-paths \
 '[{"Source":{"ResourceStatement":{"ResourceTypes":["AWS::EC2::InternetGateway"]}},
    "Destination":{"ResourceStatement":{"ResourceTypes":["AWS::EC2::NetworkInterface"]},
                   "PacketHeaderStatement":{"DestinationPorts":["22","3389"]}}}]'
aws ec2 start-network-insights-access-scope-analysis --network-insights-access-scope-id nis-123
aws ec2 get-network-insights-access-scope-analysis-findings --network-insights-access-scope-analysis-id nisa-123
```
Typical goals: internet accessibility, trusted network paths (firewalls and NAT gateways on every
path to an internet gateway) and trusted network access (only from trusted IP ranges, ports and
protocols). `MatchPaths` describes the paths you consider violations; use `ExcludePaths` for known exceptions.

## Gotchas
- Reachability Analyzer is charged per analysis run; Network Access Analyzer by the number of
  network interfaces analysed. Don't loop either every minute; see the VPC pricing page.
- It reasons about network configuration: a "reachable" result plus a timeout means look at the host
  (OS firewall, listener) next.

## Verify
- [ ] Path analysis for each critical flow shows `NetworkPathFound: true`; a blocked flow names the specific SG/NACL/route.
- [ ] Internet-to-SSH scope returns zero findings (or only documented exceptions).
- [ ] The tests run after network IaC changes and fail the pipeline on regression.

## Checked
2026-10-31. Confirmed in the Reachability Analyzer and Network Access Analyzer overview pages, the explanation-codes page and the botocore ec2 model: purpose and hop-by-hop or blocking-component output, explanation codes ENI_SG_RULES_MISMATCH, NO_ROUTE_TO_DESTINATION, SUBNET_ACL_RESTRICTION and TGW_RTB_NO_ROUTE_TO_TGW_ATTACHMENT, pricing basis of each tool, access scope goals, MatchPaths and ExcludePaths, and the `create-network-insights-access-scope` request shape (ResourceStatement, PacketHeaderStatement, DestinationPorts). Removed as unconfirmed: the list of supported source and destination types, forward-and-return path checking, the cross-account Organizations service principal, AWS-provided scope names, and EventBridge scheduling.
Method: documentation only; no commands were run.
