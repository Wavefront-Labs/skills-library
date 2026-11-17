---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.account-decommissioning
name: account-decommissioning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, account-decommissioning, subscription-cancellation, close-account, data-retention, offboarding-workload]
level: practitioner
status: docs-checked
description: "Decommission an account, subscription or project safely: data retention checks, dependency removal, quarantine OU, deletion, closure timelines and evidence for audit."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_close.html", "https://learn.microsoft.com/azure/cost-management-billing/manage/cancel-azure-subscription", "https://docs.cloud.google.com/resource-manager/docs/delete-restore-projects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Account / subscription decommissioning

## Steps
1. **Confirm** with owner, finance and security; check retention obligations for data/logs.
2. **Archive** required data and logs to the central archive (with retention lock if required).
3. **Remove dependencies**: DNS records, peering/transit attachments, private endpoints into
   shared services, IAM trust from other accounts, firewall rules, CI/CD credentials, monitoring.
4. **Quarantine**: move to a "decommissioned" OU/management group with deny-all (except read for
   audit) for a grace period (e.g. 30 days) to catch hidden dependencies.
5. **Delete resources** (or rely on closure), release reserved IPs, cancel marketplace
   subscriptions and commitments scoped to it.
6. **Close**:
   - AWS: close the member account from the management account (Organizations console, or
     `aws organizations close-account --account-id <ACCOUNT_ID>`; the console option needs All features
     mode). It shows a CLOSED label for up to 90 days, then is permanently closed.
   - Azure: cancel the subscription. Services are disabled (VMs deallocated, storage read-only), billing
     stops, and the subscription is automatically deleted 90 days after cancellation. Cancelling does not
     delete data immediately. Non-pay-as-you-go subscriptions can be reactivated via support within 90 days.
   - Google Cloud: shut down the project. It enters DELETE_REQUESTED for a 30-day recovery period, then
     is permanently deleted. Billing is disconnected and not reinstated on restore, and some services
     (for example Cloud Storage, Pub/Sub) may delete resources sooner than 30 days.
7. **Update** CMDB, EA repository, cost allocation mappings, and budget owners.

## Gotchas
- Check commitments (reservations, savings plans) tied to the account before closing; the vendor
  pages cited here do not cover them.
- Orphaned DNS records pointing to released IPs/buckets enable subdomain takeover.
- Closing the account that holds the only copy of audit logs.

## Verify
- [ ] Zero spend in the account for a full month before closure.
- [ ] No DNS records or trusts reference it.

## Checked
2026-11-08. Confirmed the closure behaviour in step 6 against the AWS Organizations close-member-account page
(All features mode, CLOSED label up to 90 days, close-account command), the Azure cancel-subscription page
(services disabled, automatic deletion after 90 days, reactivation window) and the Google Cloud delete and restore
projects page (30-day recovery, billing disconnection, early deletion by some services). The Azure page was read
in part (cancellation and deletion sections). Removed the unsupported AWS closure-quota claim, the claim that
resources persist in the AWS window, and the commitments-billing claim. The 30-day quarantine in step 4 is
labelled an example in the skill, not a vendor figure; the quarantine OU idea is advice, not a vendor claim.
Method: documentation only; no commands were run.
