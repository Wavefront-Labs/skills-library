---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.forming-the-error-budget
name: forming-the-error-budget
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [error-budget, slo, sre, release-velocity, risk]
level: practitioner
status: docs-checked
description: "Form an error budget from an SLO as the Google SRE Book and Workbook describe: who defines the SLO, who measures, window choice, and what happens at exhaustion."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/error-budget-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forming the error budget

The SRE Book says the two teams jointly define an error budget based on the service's SLO, giving "a clear, objective metric that determines how unreliable the service is allowed to be", which "removes the politics" from risk negotiations.

## Steps (SRE Book "Forming Your Error Budget")
1. Product Management defines an SLO, an expectation of how much uptime the service should have per quarter.
2. The actual uptime is measured by a neutral third party: the monitoring system.
3. The difference between the two is the budget of "unreliability" remaining.
4. While budget remains, new releases can be pushed.

The book's example: a 99.999% SLO means a 0.001% failure budget for the quarter; failing 0.0002% of expected queries spends 20% of it.

## Arithmetic
The Workbook's policy appendix: an error budget is 1 minus the SLO; a 99.9% SLO has a 0.1% budget; 1,000,000 requests in four weeks at 99.9% gives 1,000 allowed errors. The Workbook's SLO document computes each objective's budget separately (97% availability over 1,000,000 requests allows 30,000 errors).

## Choosing the window
From the Workbook: rolling windows track user experience better and should be an integral number of weeks so each contains the same number of weekends; calendar windows suit business planning but make mid-period decisions speculative because future traffic is unknown. Shorter windows give faster decisions; longer windows suit strategic decisions. The Workbook found a four-week rolling window a good general-purpose interval, complemented by weekly summaries for task prioritisation and quarterly reports for project planning.

## Governance
- The budget gives product development and SRE a common incentive. When the budget is large developers can take more risks; when nearly drained they push for more testing or slower pushes.
- The SRE Book notes this relies on the SRE team having authority to stop launches if the SLO is broken.
- Outages from networks or datacenter failures also eat the budget, and the whole team supports the resulting reduction in pushes.
- The book says simple on/off halting can be refined, for example slowing or rolling back releases when the budget is close to used up.
- If the team has trouble launching features it may loosen the SLO, which increases the budget.
- Write the actions at exhaustion into an error budget policy (see the policy skills); the Workbook says without a policy SLO compliance is just a KPI, not a decision tool.

## Gotchas
- 100% is probably never the right target (SRE Book key insight).
- Dependency failures: the Workbook describes two schools of thought on whether to freeze when a dependency owned by another team caused the miss, favours freezing, and says to record the decision in the policy.

## Verify
- [ ] The SLO is approved by stakeholders and measured by the monitoring system, not by the team being measured.
- [ ] A written policy states what happens when the budget is exhausted.

## Checked
Confirmed against the SRE Book "Embracing Risk" (Forming Your Error Budget, Benefits, Key Insights) and the Workbook "Implementing SLOs" (time window section, dependency schools of thought) and "Example Error Budget Policy" / "Example SLO Document" (arithmetic). Removed: the Prometheus recording rules (not in the sources), the "28-day default" claim as stated, and the unsourced gotchas about unmeasured SLOs and current performance.
Method: docs-only read of cited pages, 2026-11-08
