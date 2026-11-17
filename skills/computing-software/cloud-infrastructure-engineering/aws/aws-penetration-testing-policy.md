---
id: computing-software.cloud-infrastructure-engineering.aws.aws-penetration-testing-policy
name: aws-penetration-testing-policy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, penetration-testing, customer-support-policy, simulated-events, red-team, shared-responsibility, security-testing]
level: practitioner
status: docs-checked
description: "Pen test AWS-hosted systems within AWS policy: permitted services without approval, prohibited activities, simulated events requests and DDoS test rules."
sources:
  - https://aws.amazon.com/security/penetration-testing/
  - https://aws.amazon.com/security/ddos-simulation-testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS penetration testing policy

## 1. No pre-approval needed for permitted services
AWS customers may run security assessments and penetration tests against **their own**
resources on the permitted-services list without prior approval. The list on the policy page
at the time of checking: EC2 instances, WAF, NAT gateways and Elastic Load Balancers; RDS;
CloudFront; Aurora; API Gateway; AppSync; Lambda and Lambda@Edge; Lightsail; Elastic
Beanstalk; ECS; Fargate; OpenSearch Service; FSx; Transit Gateway; Bedrock AgentCore; Global
Accelerator. The page also notes API Gateway and Bedrock AgentCore are prohibited for
outbound penetration testing. The list changes, so check the policy page at the time of
testing.

## 2. Prohibited activities
- DNS zone walking, DNS hijacking and DNS pharming via Route 53 hosted zones.
- DoS, DDoS, simulated DoS and simulated DDoS (see section 3).
- Port flooding, protocol flooding, and request flooding (login or API request flooding).
  Tools may not perform these even when crashing a process for exploitation.
- S3 bucket takeover and subdomain takeover.

## 3. Simulated events and DDoS tests
Red, blue and purple team tests, simulated phishing, malware testing, iPerf testing and other
simulated events go through the **Simulated Events form** in the AWS Support console
(China regions use a separate form on the amazonaws.cn console). Include dates, account IDs,
assets involved, contact information including a phone number, and a detailed description.
Submit at least two weeks before the start date. AWS says to expect a non-automated reply
within 2 business days confirming receipt; once authorised, no further action is needed
through the stated testing period.

**DDoS simulation testing** has its own policy:
- It must be performed by an AWS Partner Network partner pre-approved by AWS (the page lists
  NCC Group plc, RedWolf Security Incorporated, Red Button and Safedash Analytics); other
  vendors need an exception request, submitted at least 14 days before the proposed test date.
- The target must be a Protected Resource in an account subscribed to AWS Shield Advanced, or
  an edge-optimised API Gateway endpoint in such an account.
- Limits: 20 Gbps bit volume; 5 million packets per second for CloudFront or 50,000 packets
  per second for any other resource type; 50,000 requests per second.

## 4. Running a test responsibly (practitioner guidance)
1. Written authorisation from the account owner listing accounts, regions, resources and
   the test window.
2. Scope by account and resource tags; exclude production data stores unless agreed.
3. Notify your own SOC and plan for expected security-tool alerts from the tester's source
   IPs; remove any suppressions afterwards.
4. Third-party testers use their own AWS accounts and IPs; never share root or admin
   credentials; give scoped, time-boxed roles if authenticated testing is needed.
5. Cloud-specific checks to include: IAM privilege escalation paths, public S3/snapshots/AMIs,
   IMDSv1 SSRF, exposed management ports, overly permissive security groups, secrets in
   user data/environment variables, cross-account trust misconfigurations.
6. Report findings with AWS-specific remediation; retest.

## Verify
- [ ] Test plan confirms all targets are on the permitted services list or covered by an approved simulated event.
- [ ] No flooding or DoS activity in scope; DDoS tests only via an approved partner.
- [ ] SOC informed, any alert suppressions removed after the window, findings tracked to closure.

## Checked
Method: docs-checked 2026-11-09 against the AWS penetration testing policy page and the DDoS simulation testing policy page, read via summarising fetch. Dropped unconfirmed: Cognito, Amazon MQ, Transfer Family, EKS in the permitted list, "allow a week or more" reply time, Trust and Safety contact paragraph, GuardDuty trusted-IP detail, and the unread incident response whitepaper source. Section 4 is practitioner guidance, not from the pages.
