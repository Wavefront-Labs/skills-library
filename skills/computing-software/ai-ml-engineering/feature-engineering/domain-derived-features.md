---
id: computing-software.ai-ml-engineering.feature-engineering.domain-derived-features
name: domain-derived-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, domain-features, domain-knowledge, ratio-features, physics-features, expert-features, feature-ideation]
level: practitioner
status: draft
description: "Derive features from domain expertise: interviewing experts, ratios and rates with physical or business meaning, thresholds and rules as features, and validating their lift."
sources:
  - https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/
  - https://developers.google.com/machine-learning/crash-course/numerical-data
  - https://www.feat.engineering/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Domain-derived features

On tabular problems the largest gains usually come from features encoding how experts reason about the problem, not from model tuning.

## Getting the knowledge
- Interview the people who make the decision today (underwriters, clinicians, maintenance engineers): "What do you look at first? What makes a case obviously bad? What do you calculate in your head?"
- Read the existing rule system or scorecard; each rule is a candidate feature.
- Shadow a few real decisions end to end; note every lookup they perform.

## Common patterns
| Pattern | Examples |
|---|---|
| Ratios with meaning | debt-to-income, loan-to-value, price per square metre, BMI, conversion rate |
| Rates over time | transactions per day, failures per 1000 operating hours, growth rate |
| Differences from a reference | price minus category median, temperature minus setpoint, deviation from personal baseline |
| Physical/engineering formulas | power = voltage x current, wind chill, stress = force / area, Reynolds number |
| Business rules as flags | "payment more than 30 days late", "address changed within 7 days of large order" |
| Durations | account age, time since last service, tenure at employer |
| Capacity / utilisation | credit utilisation (balance / limit), machine load %, occupancy |
| Domain scores | clinical scores (Charlson index), credit bureau scores, FICO-like aggregates |

## Implementation rules
- Define each feature in code with a docstring stating the business meaning and the expert source.
- Guard denominators: `np.where(income > 0, debt / income, np.nan)` and let the model handle missing; add an indicator if zero has meaning.
- Use only data available at prediction time (point-in-time); expert formulas often reference "current" values that are only known later.
- Keep raw inputs too; let the model decide.

## Validate lift
- Compare CV metrics with and without each feature group (ablation), and check permutation importance on held-out data.
- Check monotonic expectations with partial dependence: if experts say risk rises with utilisation and the model learns the opposite, investigate data or leakage.
- Watch for features that are too good: a "domain" feature computed from post-outcome data (e.g. "collections status") is leakage.

## Benefits beyond accuracy
Domain features make models explainable to stakeholders, more stable under drift, and allow monotonic constraints consistent with expert knowledge.
