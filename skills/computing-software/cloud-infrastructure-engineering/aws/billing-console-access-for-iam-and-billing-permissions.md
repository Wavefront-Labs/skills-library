---
id: computing-software.cloud-infrastructure-engineering.aws.billing-console-access-for-iam-and-billing-permissions
name: billing-console-access-for-iam-and-billing-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, billing, billing-access, iam-billing-permissions, cost-explorer-access, fine-grained-billing-actions, organizations-billing]
level: practitioner
status: docs-checked
description: "Grant IAM billing access: the root-only Activate IAM Access setting, what it does and does not control, and the fine-grained billing, cur, ce and payments actions."
sources: ["https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/control-access-billing.html", "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-permissions-ref.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing console access for IAM

## Step 1: Activate IAM Access (root user, once per account)
- IAM users and roles cannot reach the Billing and Cost Management console by default, even
  with policies granting Billing permissions. The AWS account root user turns on the
  **Activate IAM Access** setting (once per account).
- With AWS Organizations, activate it in each management or member account where IAM access
  is wanted. For member accounts created through Organizations the option is enabled by
  default.
- The setting controls console pages including Home, Budgets, Budgets Reports, Cost and
  Usage Reports, Cost categories, Cost allocation tags, Bills, Payments, Credits, Purchase
  Order, Billing preferences, Payment methods, Tax settings, Cost Explorer, Reports,
  rightsizing and Savings Plans/Reservations recommendations and reports, and Preferences.
- It does **not** control: Cost Anomaly Detection, Savings Plans overview/inventory/purchase/
  cart pages, the mobile app Cost Management view, the Billing and Cost Management SDK APIs
  (Cost Explorer, Budgets, Cost and Usage Reports APIs), Systems Manager Application Manager,
  the in-console Pricing Calculator, the cost analysis capability in Amazon Q and the AWS
  Activate console.
- Activation alone grants nothing: the role also needs an IAM policy for the pages.
- A note on the page says Cost Explorer permissions apply to all accounts and member
  accounts regardless of IAM policies; see "Controlling access to AWS Cost Explorer".

## Step 2: grant actions
- The `aws-portal` namespace, `purchase-orders:ViewPurchaseOrders` and
  `purchase-orders:ModifyPurchaseOrders` reached end of standard support in July 2023. Orgs
  and accounts created on or after 6 March 2023 already use fine-grained actions. Payer
  accounts can use the bulk policy migrator scripts and the old-to-granular mapping reference.
- Actions listed in the Billing console actions table include:
  - `billing:ListBillingViews`, `GetBillingView`, `CreateBillingView`, `UpdateBillingView`,
    `DeleteBillingView` (custom billing views);
  - `cur:DescribeReportDefinitions`, `PutReportDefinition`, `ModifyReportDefinition`,
    `DeleteReportDefinition` (apply to all reports, console or API; not updating them loses
    console access to reports);
  - `ce:CreateCostCategoryDefinition`, `DeleteCostCategoryDefinition`,
    `DescribeCostCategoryDefinition`, `ListCostCategoryDefinitions`, `UpdateCostCategoryDefinition`;
  - `payments:ListPaymentInstruments`, `payments:UpdatePaymentInstrument` and other
    `payments:` actions (connected accounts, financing, tags);
  - `pricing:DescribeServices`, `GetAttributeValues`, `GetProducts` (allow all three for the
    Price List API);
  - `purchase-orders:` view and modify; `tax:GetExemptions`, `tax:UpdateExemptions`.
- Use AWS managed policies as a start and move toward least privilege with customer managed
  policies; add conditions (for example MFA) per the page's policy best practices.
- To use the Billing console a principal needs a minimum set of list/view permissions; a
  policy more restrictive than that breaks the console. CLI/API-only callers need only the
  actions matching their calls.
- Scoping what a principal sees across accounts can use custom billing views (see the
  `billing:*BillingView` actions).

## Gotchas
- Old policies using `aws-portal:*` are past end of standard support: replace them with
  fine-grained actions.
- Activating IAM access and attaching a policy are both required.

## Verify
- [ ] Activate IAM Access is on in each account where IAM principals need the console.
- [ ] An analyst role can open the intended pages but has no `payments:UpdatePaymentInstrument`.

## Checked
Checked 2026-11-08 against the AWS Billing User Guide pages "Overview of managing access permissions" and "Identity-based policy with AWS Billing" (billing actions table).
Removed because the pages do not state them: the exact managed policy names, the sample FinOps JSON policy, `ce:Get*`/`budgets:`/`bcm-data-exports:`/`invoicing:`/`freetier:` action tables, the SCP deny example, the Identity Center permission set advice, Cost Explorer API request pricing, and the "even AdministratorAccess users see no permission" wording. Added the list of pages the setting does and does not control and the member-account default.
Method: docs-only read of cited pages, 2026-11-08
