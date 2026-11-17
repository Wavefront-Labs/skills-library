---
id: computing-software.cloud-infrastructure-engineering.google-cloud.invoices-payment-methods-and-billing-contacts
name: invoices-payment-methods-and-billing-contacts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, invoices, payment-methods, billing-contacts, invoiced-billing, self-serve-billing, payments-profile, tax-information, purchase-order, billing-account-closure, billing-documents]
level: practitioner
status: docs-checked
description: "Set up a billing account for finance: invoiced vs self-serve payment, payments profile, PO numbers, backup payment methods, and where invoices and statements are found."
sources: ["https://cloud.google.com/billing/docs/how-to/invoiced-billing", "https://cloud.google.com/billing/docs/how-to/manage-billing-account", "https://cloud.google.com/billing/docs/how-to/get-invoice", "https://cloud.google.com/billing/docs/how-to/payment-methods"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Invoices, payment methods and billing contacts

**Goal:** finance receives the right documents each month and nobody discovers at quarter end that
the payment method failed or the PO number is missing.

## 1. Two account types
- **Self-serve (online)**: you create it first; costs are paid automatically with the payment
  methods on the linked Google payments account. Documents: statements, debit and credit memos,
  tax invoices as applicable. A statement is a summary of monthly billing activity, not a bill.
- **Invoiced (offline)**: you accrue a month of costs and get the invoice by email at the start of
  the following month (usually by the 5th business day); pay by check or wire transfer within the
  agreed Payment Terms. Eligibility includes, but is not limited to: registered as a business
  for at least one year, expected spend of at least $40,000 a year on Google Cloud, and invoiced
  billing available in your country. Apply as a Billing Account Administrator with the
  "Apply for monthly invoiced billing" form; invoiced accounts can raise project and quota limits.
  Resellers or multiple countries can produce several invoices (split invoicing).

## 2. Payments profile
The Cloud Billing account is associated with a Google payments profile (the legal entity that
pays) and linked to a payments account holding the payment instruments. Billing roles control the
billing account; the payments profile has its own permissions in the Google payments center.
Some billing permissions also grant equivalent payments permissions from the console.
The account name, mailing addresses (including the legally registered address and the invoice
mailing address) and linked projects can be changed later (see "Modify your Cloud Billing account").

## 3. Payment methods (self-serve)
- Each self-serve account must keep at least one valid form of payment, even at a $0.00 balance.
  Without one the account is suspended and **all** APIs, services and resources in **all** linked
  projects stop, including services paid with Prepay credits.
- Add a **backup** credit or debit card: it is charged only if the primary fails. A bank account
  cannot be a backup. A bank account as primary needs an established billing history and
  verification (can take up to 10 days); bank payments can take five to ten business days.
- Not accepted: prepaid cards, debit cards needing two-factor authentication, and wire transfer for
  Prepay, Postpay threshold or monthly-charge accounts. Available methods vary by country.
- Adding, editing or fixing a method needs `billing.accounts.getPaymentInfo` and
  `billing.accounts.updatePaymentInfo`, which comes with Billing Account Administrator.

## 4. Documents and contacts
- Self-serve: Statements and invoices are on the **Invoices** page of the billing account; payment
  receipts are on **Transactions**.
- Invoiced: documents are on the **Payment status** page; you can receive a PDF invoice by email,
  and configure a list of contacts to receive invoices by email.
- Admin-level permission on the Google payments profile is needed to use the Statement of account
  and Payments pages in the Google payments center.

## 5. PO numbers
For billing accounts billed by monthly invoice you can set or change the invoice purchase order
number (also called IO number, CPE or client code); it appears in the header of your invoices.

## Gotchas
- A closed billing account stops all billable services in its linked projects; billing accounts
  cannot be deleted, only closed (information is retained). Disabling billing on projects or
  linking them elsewhere also stops charges.
- Closed accounts can be reopened after payment issues are resolved.

## Verify
- [ ] The invoice for last month reached the finance mailbox listed on the account's contacts.
- [ ] PO number appears on the invoice header (invoiced accounts).
- [ ] A backup payment method is present (self-serve) or the account is invoiced.

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: "Apply for monthly invoiced billing", "Manage your Cloud Billing account", and the first 75 lines of "Add, remove, or update a payment method" (account types, methods, unsupported methods, permissions to add or fix a method; the rest, including removal permissions, was not read). "Get a Cloud Billing document" was searched by keyword (Invoices, Payment status, statements, PDF, contacts), not read end to end.
Corrections: removed "net-30 terms", "12 months history and meaningful spend or enterprise agreement" (page: one year as a business and $40,000 a year), "currency cannot change", the VAT reverse-charge and "Account type: Business" claims, the payments-users "email invoices" tick-box and Essential Contacts steps, "billing.admin does not receive invoices", the "one PO per billing account" advice, the Documents path "Billing -> Documents" and PDF/CSV by month, the Marketplace and reseller document claims, the grace-email suspension claim, and the unconfirmed gotchas on legal name edits, final invoice timing and budget currency mismatch.
