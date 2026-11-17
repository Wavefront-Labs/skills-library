---
id: computing-software.cybersecurity-defensive.network-defence.ddos-testing
name: ddos-testing
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ddos-testing, ddos-simulation, load-testing, ddos-readiness, red-button-test, cloud-provider-policy, ddos-mitigation]
level: practitioner
status: docs-checked
description: "Test DDoS defences safely: authorised simulation vendors, cloud provider testing policies, scope and kill switches, attack vector selection and measuring mitigation time."
sources: ["https://aws.amazon.com/security/ddos-simulation-testing/", "https://learn.microsoft.com/en-us/azure/ddos-protection/test-through-simulations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DDoS simulation testing

Untested DDoS protection often fails on the day (mis-sized thresholds, origin exposed, scrubbing not
engaged). Test it - legally and safely.

## Rules
- Only via approved vendors. AWS: the test must be run by a pre-approved AWS DDoS Test Partner; the target must be a Protected Resource in an AWS account you own that is subscribed to Shield Advanced (or an edge-optimized API Gateway endpoint in such an account); limits are 20 Gbps, 5 million packets/s for CloudFront or 50,000 packets/s for other resources, and 50,000 requests/s; the test may not originate from an AWS resource or simulate amplification using one; AWS may tell the vendor to stop at any time. Non-compliant tests need an exception request at least 14 days ahead. Azure: only approved partners (MazeBolt, Red Button, RedWolf at last check) against Azure-hosted public IPs in your own subscription that are protected by Azure DDoS Protection.
- Written authorisation from asset owners, ISP and scrubbing provider notified, test window agreed.
- Do not test from your own botnet-like tooling or against shared/third-party infrastructure; use the vendors above.
- Microsoft recommends running simulations in staging environments or during nonpeak hours, with diagnostic logs and an alert on the Under DDoS attack or not metric configured first.

## Plan
1. Objectives: does mitigation engage? time to mitigate? does legitimate traffic survive? are alerts and runbooks followed?
2. Vectors: agree attack vectors, rates and targets with the vendor in a written test plan (Red Button's planning session produces one).
3. Ramp gradually; kill switch with immediate stop command; real-user synthetic monitoring running.
4. Include direct-to-origin tests (attack the origin IP) to verify origin is not reachable bypassing CDN/WAF.

## Measure
Time to detect, time to mitigate, leakage (traffic reaching origin), false positives on legitimate test
traffic, alert receipt by SOC/NOC, provider escalation.

## Gotchas
- Always-on vs on-demand scrubbing: test the swing from detection to diversion.
- AWS treats test results as AWS Confidential Information.

## Verify
- [ ] Report with measured mitigation time per vector and actions raised.
- [ ] Repeat periodically and after major architecture changes (Azure recommends periodic simulations).

## Checked
Checked 2026-11-09 against the AWS DDoS Simulation Testing Policy page (partner requirement, Shield Advanced target, volume limits, origin rules, 14-day exception request) and the Azure DDoS Protection simulation tutorial (approved partners, own-subscription public IPs, staging or nonpeak advice, Red Button stages). Removed: BreakingPoint Cloud (not in the current Azure list), the CISA PDF (blocked, not read), the vector list, BGP diversion timing and autoscaling cost remarks.
Method: docs-checked 2026-11-09 against the AWS and Azure pages named above.
