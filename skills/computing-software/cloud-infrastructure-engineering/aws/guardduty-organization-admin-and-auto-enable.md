---
id: computing-software.cloud-infrastructure-engineering.aws.guardduty-organization-admin-and-auto-enable
name: guardduty-organization-admin-and-auto-enable
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, guardduty, guardduty-org-admin, auto-enable-members, delegated-administrator, multi-account-security, organizations]
level: practitioner
status: docs-checked
description: "Run GuardDuty across an organization: delegate admin, auto-enable all members and protection plans in every region, onboard existing accounts, and centralise findings."
sources: ["https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_organizations.html", "https://docs.aws.amazon.com/guardduty/latest/ug/set-guardduty-auto-enable-preferences.html", "https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_exportfindings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GuardDuty across the organization

**Goal:** every current and future account has GuardDuty on in every enabled region, with
the agreed protection plans, managed from a Security Tooling account, and findings flow to
one place.

## 1. Delegate the admin (per region)
From the management account, **in each region**:
```bash
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  aws guardduty enable-organization-admin-account --admin-account-id <ADMIN_ACCOUNT_ID> --region $r
done
```
GuardDuty is regional; AWS requires the same account as delegated administrator in all
Regions.

## 2. Auto-enable (from the delegated admin, per region)
```bash
DET=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)
aws guardduty update-organization-configuration --detector-id $DET \
  --auto-enable-organization-members ALL \
  --features '[
    {"Name":"S3_DATA_EVENTS","AutoEnable":"ALL"},
    {"Name":"EKS_AUDIT_LOGS","AutoEnable":"ALL"},
    {"Name":"EBS_MALWARE_PROTECTION","AutoEnable":"ALL"},
    {"Name":"RDS_LOGIN_EVENTS","AutoEnable":"ALL"},
    {"Name":"LAMBDA_NETWORK_LOGS","AutoEnable":"ALL"},
    {"Name":"RUNTIME_MONITORING","AutoEnable":"NEW",
     "AdditionalConfiguration":[{"Name":"EKS_ADDON_MANAGEMENT","AutoEnable":"NEW"},
                                {"Name":"ECS_FARGATE_AGENT_MANAGEMENT","AutoEnable":"NEW"},
                                {"Name":"EC2_AGENT_MANAGEMENT","AutoEnable":"NEW"}]}]'
```
- `ALL` enables for all accounts in the organization (new accounts, and accounts that were
  suspended or removed and rejoin); `NEW` only for member accounts that join later; `NONE`
  prevents auto-enabling for new accounts and the administrator manages each account.
  Updating from `ALL`/`NEW` to `NONE` does not disable the option on existing accounts.
- Auto-enable preferences cover all protection plans except Malware Protection for S3.
- Decide per plan which to auto-enable; check the vendor pricing page for cost.
- Check coverage: `aws guardduty list-members --detector-id $DET --only-associated false`
  and `get-member-detectors` for feature status per account. Runtime coverage:
  `list-coverage`.

## 3. Findings flow
- Export to S3 for retention beyond GuardDuty's 90-day retention:
  `create-publishing-destination --destination-type S3` with a KMS key (bucket and key in
  the same Region). Export settings are regional: configure them in each Region you use.
- New active findings are exported within about 5 minutes; updated findings are exported
  every 6 hours by default. `--finding-publishing-frequency` accepts `FIFTEEN_MINUTES`,
  `ONE_HOUR` or `SIX_HOURS`.
- Findings from an opt-in Region cannot be exported to an S3 bucket in a different opt-in Region.

## 4. Guarding the setup
- Consider an SCP denying detector-changing actions for everyone but the security
  automation role (verify action names in the service authorization reference).

## Gotchas
- Malware Protection for S3 is excluded from auto-enable preferences (configured separately).

## Verify
- [ ] In each enabled region the delegated admin lists all org accounts as `Enabled` members.
- [ ] A newly created test account shows a detector with the expected features.
- [ ] `aws guardduty create-sample-findings` in a member account surfaces in the admin and in the S3 export.

## Checked

2026-10-28. Confirmed against AWS documentation: same delegated admin in all Regions, ALL/NEW/NONE semantics, Malware Protection for S3 exclusion, 90-day retention, export settings regional, 5 minute / 6 hour export timing; feature, additional-configuration and publishing-frequency enums via the botocore guardduty model.
Removed: console-enforcement and opt-in skip claims, existing-detector and Config-rule gotchas, member-cannot-disable claims, specific SCP action list, per-volume cost note, FIFTEEN_MINUTES-as-default wording, placeholder admin account id.
Method: documentation only; no commands were run.
