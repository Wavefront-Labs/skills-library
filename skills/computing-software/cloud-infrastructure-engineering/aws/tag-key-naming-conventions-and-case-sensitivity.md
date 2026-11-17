---
id: computing-software.cloud-infrastructure-engineering.aws.tag-key-naming-conventions-and-case-sensitivity
name: tag-key-naming-conventions-and-case-sensitivity
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, tagging, tag-naming-convention, tag-keys, tag-policies, case-sensitivity, cost-allocation-tags]
level: practitioner
status: docs-checked
description: "Design consistent AWS tag keys: case sensitivity, allowed characters and limits, the reserved aws: prefix, an org prefix convention, and tag policies."
sources: ["https://docs.aws.amazon.com/tag-editor/latest/userguide/best-practices-and-strats.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html", "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag key naming conventions and case sensitivity

## Rules AWS documents
- Tag keys and values are **case sensitive**. Decide one capitalization strategy and use it for
  all resource types; avoid similar tags with inconsistent case (`Costcenter`, `costcenter`,
  `CostCenter`).
- Up to 50 user-created tags per resource. Each key is unique per resource and has one value.
- Key: 1 to 128 Unicode characters (UTF-8). Value: 0 to 256.
- Allowed characters vary by service. In general: letters, numbers, spaces representable in UTF-8,
  and `_ . : / = + - @`. Check the service's own documentation.
- Tags beginning with `aws:` are reserved for AWS, do not count against the 50, and cannot be
  edited or deleted.
- Do not put PII or confidential data in tags: they are accessible to many services, including billing.

## Convention AWS suggests
- All lowercase words, hyphens between words, and an organization prefix followed by a colon,
  for example `anycompany:cost-center`, `anycompany:environment-type`, `anycompany:application-id`.
- The prefix marks tags as yours rather than AWS's or a third-party tool's; lowercase with hyphens
  avoids confusion over capitalization.
- Changing access-control tags later means updating every policy that references them.
- Tag Editor and the Resource Groups Tagging API enable programmatic management of tags.

## Enforce with tag policies (AWS Organizations)
- Tag policies standardize tags across accounts, including the preferred case treatment of keys
  and values, and define valid key names and valid values per key.
- AWS suggests first only monitoring to clean up existing tags, then turning on enforcement to
  prevent non-compliant tags being created.

## Cost allocation
- Cost allocation tags must be activated (user-defined and AWS-generated separately) before
  AWS uses them to organize costs. Tags can take up to 24 hours to appear in the Billing and
  Cost Management console.

## Verify
- [ ] Written tag dictionary (keys, allowed values, owners) published.
- [ ] Tag policy attached and compliance reviewed.

## Checked

Method: docs-checked 2026-11-09 against the Tagging User Guide best-practices page, the AWS Organizations tag policies page and the Billing cost allocation tags page. Removed unconfirmed: policy JSON sample and enforced_for behaviour, SCP aws:RequestTag guidance, get-compliance-summary, mandatory key set, backfill option, child-resource tagging notes, trailing-space note.
