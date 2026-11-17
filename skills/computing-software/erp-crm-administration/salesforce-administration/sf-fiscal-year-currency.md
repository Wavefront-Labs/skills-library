---
id: computing-software.erp-crm-administration.salesforce-administration.sf-fiscal-year-currency
name: sf-fiscal-year-currency
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-fiscal-year-currency]
level: practitioner
status: draft
description: "Choose standard or custom fiscal years and enable multicurrency carefully."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set fiscal year and currencies
**Goal:** Choose standard or custom fiscal years and enable multicurrency carefully.

- Setup > Fiscal Year: standard follows the Gregorian year with a chosen start month; custom fiscal years allow 4-4-5 style periods.
- Enabling multiple currencies cannot be turned off; set the corporate currency and dated exchange rates deliberately.
- Reports and forecasts honour the fiscal setting.

## Gotchas
- Changing the fiscal year after data exists changes historical period reporting.

## Self-check
Opportunity close dates fall in the expected fiscal quarter in a report.
