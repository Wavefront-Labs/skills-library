---
id: business-finance.accounting.payroll-administration.gross-to-net-pay-run-and-reconciliation
name: gross-to-net-pay-run-and-reconciliation
category: business-finance
field: accounting
product: payroll-administration
tags: [payroll-administration, payroll, gross-to-net, pay-run, payslip, withholding, paye, payg, income-tax-withholding, social-security, national-insurance, fica, superannuation, pension-contributions, pre-tax-deductions, post-tax-deductions, employer-costs, payroll-journal, payroll-reconciliation, year-end-filings, w-2, p60, payroll-controls]
level: practitioner
status: draft
description: "Run a payroll cycle end to end: inputs cut-off, gross-to-net order, employer costs, pre-release checks, payroll journal, liability reconciliation and year-end filings."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gross-to-net pay run and reconciliation

**Goal:** pay every employee the right amount on time, remit every withholding to
the right body, and leave a ledger where payroll liability accounts clear to zero.
Rates, thresholds and form names are **country-specific** (US W-2/941, UK PAYE/RTI
and P60, Australian PAYG/STP and super); the structure below is common to all.

## 1. Inputs and cut-off
Fix a cut-off date each cycle (e.g. 5 working days before pay date). Collect:
starters and leavers, pay-rate changes, hours/overtime/timesheets, commissions and
bonuses, leave taken, expense reimbursements, benefit changes, new tax codes or
withholding forms, court orders/garnishments. Every change needs an **approved
source document** — never a hallway request.

## 2. Gross-to-net, in order
```
  Basic pay (salary/periods, or hours × rate)
+ Overtime, allowances, commission, bonus
+ Taxable benefits (where taxed through payroll)
- Unpaid leave
= GROSS PAY
- Pre-tax deductions (e.g. qualifying pension/401(k), salary sacrifice, some health plans)
= TAXABLE PAY
- Income tax withholding (per employee's code/form and cumulative or period basis)
- Employee social security (NI / FICA / similar)
- Post-tax deductions (loans, union dues, garnishments — attachment priority rules apply)
+ Non-taxable reimbursements
= NET PAY
```
**Employer costs** on top: employer social security, pension/superannuation
contributions, payroll taxes, workers' comp levies. Total cost of employment = gross
+ employer costs.

## 3. Pre-release checks (before you approve the bank file)
- **Variance report vs last period** per employee: flag net-pay changes over a set
  percentage, and anyone paid for the first or last time.
- **Headcount reconciliation:** last period + starters − leavers = this period.
- Zero or negative net pay, and anyone below minimum wage for hours worked.
- Leavers paid final pay and accrued holiday per policy, then stopped.
- Bank details changed this cycle independently verified (a classic fraud route —
  call back on a known number, never use details from the change request email).
- **Segregation:** the person who edits master data isn't the one who releases payment.

## 4. Payroll journal and liabilities
```
Dr Salaries expense (gross)        Cr Net wages payable
Dr Employer taxes/pension expense  Cr Tax withholding payable
                                   Cr Social security payable (ee + er)
                                   Cr Pension payable (ee + er)
                                   Cr Other deductions payable
```
When the bank file pays and each remittance goes out, the payables clear. At month end
every payroll liability account should show only amounts due next remittance date;
anything older is a missed or mismatched payment.

## 5. Year-end
Reconcile the year's payroll register totals to the filings (annual employee tax
statements and employer returns) and to the general ledger expense before submission.
Differences usually come from off-cycle runs, manual cheques or corrections processed
outside the system.

## Gotchas
- **Cumulative vs non-cumulative** tax calculation changes refunds/catch-ups mid-year.
- **Back pay** may be taxed in the period paid, not the period earned.
- Off-cycle and manual payments must go through the payroll system, or year-end won't tie.
- Contractor vs employee status is a legal question; payroll can't fix
  misclassification (see wage-and-hour skills under law-government).
- Thresholds and order of attachment for garnishments differ widely — confirm locally.

## Verify
- [ ] All inputs before cut-off have approved source documents.
- [ ] Variance and headcount reports reviewed and signed before release.
- [ ] Bank-detail changes independently verified.
- [ ] Payroll journal posted; liability accounts clear on remittance.
- [ ] Register totals tie to GL and to statutory filings at year end.
