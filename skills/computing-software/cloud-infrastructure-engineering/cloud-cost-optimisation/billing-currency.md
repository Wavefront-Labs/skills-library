---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.billing-currency
name: billing-currency
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, billing-concepts, billing-currency, exchange-rates, fx, multi-currency, focus-specification]
level: practitioner
status: docs-checked
description: "Handle currency conversion in cloud cost data: a predetermined chargeback currency, conversion in the monthly process and tracking currency effects separately."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing currency and exchange rates

The FinOps Framework Invoicing and Chargeback capability treats currency conversion as part of the monthly
chargeback process. This skill keeps only what that page supports; provider currency behaviour is not covered there
and must be checked in your own agreements.

## Steps
1. **Agree the chargeback currency** with Finance. The Framework's chargeback file carries data in a predetermined
   currency, aligned to the organisation's general ledger.
2. **Factor conversion into the monthly process** (Walk behaviour). The rate policy (which rate, from which source)
   is yours to agree with Finance; the Framework does not specify one. Record the rates used.
3. **Keep currency visible**: at Run, conversion is automated where possible and shown separately in the chargeback
   file so fluctuations unrelated to cloud usage can be analysed.
4. **Track currency effects versus usage**: the Framework lists tracking changes in cloud cost caused by currency
   fluctuation versus usage as a Finance activity. Report it as its own line so teams are not blamed for currency moves.
5. **Do not sum unconverted amounts** from exports in different currencies; convert first and state the currency on
   every consolidated view.

## Verify
- [ ] Every consolidated view states its currency and the rate source used.
- [ ] Currency effect is reported separately from usage change.

## Checked
Confirmed on the FinOps Framework Invoicing and Chargeback page (read to the KPI list): currency conversion in the
monthly process, automated and distinct currency conversion at Run, tracking currency versus usage change, chargeback
file in a predetermined currency. Removed: all provider-specific currency behaviour (AWS, Azure, Google Cloud;
pages unreadable), the FX variance formula, rate policy options, commitment amortisation rate guidance, FOCUS column
names, and the tool-behaviour gotchas.
Method: docs-checked 2026-11-09 against finops.org Framework Invoicing and Chargeback capability page
