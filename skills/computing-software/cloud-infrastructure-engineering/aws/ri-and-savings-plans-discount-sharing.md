---
id: computing-software.cloud-infrastructure-engineering.aws.ri-and-savings-plans-discount-sharing
name: ri-and-savings-plans-discount-sharing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, savings-plans, reserved-instances, discount-sharing, ri-sharing, consolidated-billing, preferences-sharing]
level: advanced
status: docs-checked
description: "Control how RI and Savings Plans discounts flow across an organization: default sharing, deactivating per account, group sharing modes and how plans apply."
sources:
  - https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-turn-off.html
  - https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html
  - https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-applying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RI and Savings Plans discount sharing

## 1. Default behaviour
Consolidated billing treats all accounts in an organization as one account for billing, so
all accounts can receive the hourly benefit of Reserved Instances bought by any other
account. Savings Plans apply to usage after EC2 Reserved Instances. EC2 Instance Savings
Plans are applied before Compute Savings Plans because Compute Savings Plans are broader.
In a consolidated billing family, a Savings Plan applies first to the owner account's usage
and then to other accounts' usage, only if sharing is enabled. Within the eligible usage,
the plan applies to the highest savings percentage first; ties go to the usage with the
lowest Savings Plans rate. Each hour's commitment can only be used within that hour.

## 2. Deactivating sharing
The management account of the organization controls sharing for accounts in it. In Billing
and Cost Management, open **Billing preferences**; under *Reserved Instances and Savings
Plans discount sharing preference by account*, select accounts and choose **Deactivate**
(or **Actions > Deactivate All**). Activate works the same way. Notes from the page:
- Deactivating sharing can result in higher monthly bills.
- The Savings Plans owner account must remain active in sharing preferences for its
  discounts to apply to other accounts; both the purchasing and the receiving account need
  sharing activated.
- You can change preferences at any time. Estimated bills use the last set of preferences;
  the final bill for the month uses the preferences set at 23:59:59 UTC on the last day of
  the month.
- If a Savings Plans owner account leaves the organization, its Savings Plans no longer
  apply to the consolidated bill.

## 3. Sharing modes
Group sharing uses AWS Cost Categories to define account groups (Accounts dimension only;
each account in at most one group; the payer account cannot be in a group; the Cost Category
"Uncategorized costs" default value must not overlap a group name). Modes:
- **Organization-wide**: owner first, then any other org account.
- **Prioritized group**: owner first, then the owner's group, then the rest of the org.
- **Restricted group**: owner first, then only the defined group; no sharing outside it,
  even with unused capacity, which may leave commitments underutilised.
Select the mode under Billing preferences > Edit.

## 4. Billing transfer and Billing Conductor
With billing transfer, Reserved Instances and Savings Plans apply only within the
Organization where they were bought, whoever pays the bill; they cannot be bought or shared
across multiple Organizations, and each Organization controls its own preferences.

## 5. Strategy (practitioner guidance)
- Central purchasing with organization-wide sharing tends to maximise utilisation because
  any account's usage can absorb the commitment.
- Decentralised buying: use prioritised group sharing to keep benefit local without
  wasting unused commitment as full deactivation can.
- Check Savings Plans utilisation and RI coverage in Cost Explorer after any change.

## Verify
- [ ] Billing preferences show the intended sharing per account or group.
- [ ] Savings Plans utilisation does not fall after the change.

## Checked
Method: docs-checked 2026-11-09 against the three cited AWS pages (billing guide ri-turn-off and ri-behavior, Savings Plans sp-applying), read via summarising fetch. Rewrote the page: dropped unconfirmed CLI examples, CUR column names, Amortized/Net amortized chargeback claims, zonal RI note, "turning off in management account turns off whole org", and the old cost-management ri-turn-off URL (returned only a title). Section 5 is practitioner guidance.
