---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-enhanced-scanning-and-scan-on-push
name: ecr-enhanced-scanning-and-scan-on-push
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, enhanced-scanning, scan-on-push, inspector, image-scanning, vulnerability-management, ci-gate]
level: practitioner
status: docs-checked
description: "Scan images in ECR: basic vs Inspector enhanced scanning, scan-on-push and continuous rules, reading findings, CI severity gates and EventBridge routing."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-enhanced.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-basic.html", "https://docs.aws.amazon.com/inspector/latest/user/eventbridge-integration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECR enhanced scanning and scan on push

## 1. Basic vs enhanced
| | Basic | Enhanced (Amazon Inspector) |
|---|---|---|
| Coverage | OS packages (AWS native technology, CVE database) | OS **and** programming-language packages |
| When | scan on push or manual | scan on push **or** continuous scan |
| Cost | check current ECR pricing | no ECR charge; Inspector charges to scan (see Inspector pricing) |
| Findings | `DescribeImageScanFindings` | ECR and Inspector; Inspector emits EventBridge events |

## 2. Configure (registry level)
```bash
aws ecr put-registry-scanning-configuration --scan-type ENHANCED --rules '[
 {"scanFrequency":"CONTINUOUS_SCAN","repositoryFilters":[{"filter":"prod/*","filterType":"WILDCARD"}]},
 {"scanFrequency":"SCAN_ON_PUSH","repositoryFilters":[{"filter":"*","filterType":"WILDCARD"}]}]'
```
Enhanced scanning uses a service-linked role that Inspector creates when you turn it on. Repositories matching a filter are scanned with enhanced scanning only; repositories matching no filter get scan frequency Off, and manual enhanced scans are not supported. If a repository matches both a continuous and a scan-on-push filter, continuous wins. The `SCAN_ELIGIBILITY_EXPIRED` status means the Inspector scan duration has elapsed or the image was pushed more than 14 days before enhanced scanning was first enabled; push it again. By default Inspector keeps monitoring until images are deleted or enhanced scanning is disabled; push-date and re-scan durations are set in the Inspector console.

## 3. Read findings
```bash
aws ecr describe-image-scan-findings --repository-name prod/api --image-id imageTag=1.4.2 \
  --query 'imageScanFindings.findingSeverityCounts'
aws inspector2 list-findings --filter-criteria '{"ecrImageRepositoryName":[{"comparison":"EQUALS","value":"prod/api"}],"severity":[{"comparison":"EQUALS","value":"CRITICAL"}]}' \
  --query 'findings[].[title,packageVulnerabilityDetails.vulnerablePackages[0].name,fixAvailable]'
```

## 4. Gate CI
After push, wait until `describe-image-scan-findings` reports a finished scan (status `COMPLETE` for basic scanning; with enhanced scanning check the status values your account returns), then fail on critical findings:
```bash
C=$(aws ecr describe-image-scan-findings --repository-name prod/api --image-id imageTag=$TAG \
   --query 'imageScanFindings.findingSeverityCounts.CRITICAL' --output text)
[ "$C" = "None" ] || [ "$C" -eq 0 ] || { echo "critical vulns: $C"; exit 1; }
```
Record accepted risks in Inspector rather than ignoring the gate.

## 5. Route new findings
EventBridge `source: aws.inspector2`, `detail-type: Inspector2 Finding` (documented finding events) with a filter on the resource type and severity → ticketing/Slack. Inspect a real event for the exact `detail` field names before writing the pattern.

## Gotchas
- Switching between enhanced and basic makes previously established scans unavailable until you switch back or set them up again.
- Archived images cannot be scanned; restore them first.
- Basic scanning: an image can be scanned once per 24 hours (scan on push counts) and up to 100,000 images per 24 hours per registry (quotas page, not adjustable).

## Verify
- [ ] A push to `prod/*` produces findings; they show in ECR and Inspector.
- [ ] CI fails on an image with a known critical CVE (test with an old base image).
- [ ] EventBridge rule delivers a test finding to the alert channel.

## Checked
2026-10-27. Documentation: Amazon ECR User Guide (image scanning, enhanced scanning, basic scanning, service quotas) and Amazon Inspector User Guide EventBridge integration, read this date. Confirmed: basic vs enhanced scope and frequencies; enhanced filters, continuous over scan-on-push precedence, no manual enhanced scans, 14-day SCAN_ELIGIBILITY_EXPIRED rule, default monitoring duration; 24-hour and 100,000 basic scan limits; Inspector event source and detail-type. Confirmed from the ECR API model (botocore): ScanType BASIC/ENHANCED, ScanFrequency SCAN_ON_PUSH/CONTINUOUS_SCAN/MANUAL, filter type WILDCARD, at most 2 scanning rules. Removed the claim that enhanced scanning is delivered to Security Hub, the ecr wait waiter use, and distroless statements as unconfirmed.
Method: documentation only; no commands were run.
