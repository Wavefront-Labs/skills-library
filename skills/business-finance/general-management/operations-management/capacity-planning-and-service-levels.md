---
id: business-finance.general-management.operations-management.capacity-planning-and-service-levels
name: capacity-planning-and-service-levels
category: business-finance
field: general-management
product: operations-management
tags: [general-management, operations-management, capacity-planning, workforce-planning, service-level, sla, slo, handle-time, shrinkage, utilisation, utilization, fte, backlog, queueing, erlang-c, demand-forecasting, back-office, ops-cadence, resourcing]
level: practitioner
status: draft
description: "Plan staffing to hit a service level: measure demand and handle time, apply shrinkage and target utilisation, plan peaks, and run a daily/weekly ops cadence."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity planning against service levels — staff to the demand you actually get

**Goal:** match people (or machine hours) to incoming work so you hit a stated service
level without chronic overtime or idle teams, and know in advance when you will miss.

## 1. Define the unit of work and the service level
- Pick one countable unit: tickets, orders, applications, calls, cases.
- Write the service level as *X% of units completed within Y time* (e.g. "90% of
  invoices processed within 2 business days"). An average ("we take 1.5 days") hides
  the tail that customers complain about.
- Agree the measurement point: received → closed, not assigned → closed. Teams quietly
  shift the start clock to look good.

## 2. Measure demand and handle time
- Pull at least **8–13 weeks** of arrivals by day (and by hour for front-line teams).
  Note the weekly shape: Monday and month-end peaks are the norm in back-office work.
- Measure **handle time** (hands-on minutes per unit) separately from **elapsed time**
  (calendar time including waiting). Capacity is driven by handle time; service level
  is driven by queue and waiting.
- Sample handle time by observation or system timestamps on ~30+ units per work type;
  self-reported estimates typically run low.

## 3. Convert to required capacity
```
workload hours/week   = units per week × handle minutes ÷ 60
productive hours/FTE  = contracted hours × (1 − shrinkage)
FTE required          = workload hours ÷ productive hours/FTE ÷ target utilisation
```
- **Shrinkage** = leave, sickness, training, meetings, breaks. 25–35% is common in
  office teams; measure yours rather than assuming.
- **Target utilisation**: plan at ~75–85% for back-office work. Planning at 100% makes
  queues grow non-linearly — waiting time explodes as utilisation approaches 100%
  (basic queueing behaviour), so small demand spikes blow the service level.
- For real-time queues (phones, chat) use an Erlang C calculator instead of the
  formula above; the linear method understaffs them.

## 4. Plan the peaks, not the average
- Build the plan week by week for the next quarter using the seasonal shape.
- Levers in order of cost: shift work in time (defer non-urgent tasks off peaks),
  cross-train a flex pool, approved overtime, temps/contractors, permanent hires.
  Hiring lead time plus ramp-up (often 2–3 months to full productivity) means the hire
  decision must be made one to two quarters ahead.

## 5. Run the cadence
- **Daily:** backlog, arrivals vs forecast, oldest item age. Oldest-item age is the
  earliest warning that the service level is about to break.
- **Weekly:** service level achieved, utilisation, forecast error; re-plan next 4 weeks.
- **Quarterly:** refresh handle times (process changes alter them), shrinkage and
  the hiring plan.

## Gotchas
- **Mixed work types.** Averaging a 5-minute and a 60-minute task gives nonsense;
  plan by work type or weight by mix.
- **Rework is demand.** Count re-opened and returned items as arrivals.
- **Backlog is a debt.** A team at exactly capacity never clears an existing backlog;
  plan separate burn-down hours.
- **Utilisation as a target for individuals** drives gaming; use it for planning only.
- Benchmarks here (shrinkage, utilisation bands) are typical ranges from operations
  practice, not standards — calibrate to your own data. *(Draft: ranges not
  independently sourced.)*

## Verify
- [ ] Service level is stated as a percentile within a time, with a fixed start clock.
- [ ] Demand history covers at least two months and shows the weekly/monthly shape.
- [ ] FTE requirement includes measured shrinkage and a utilisation target below 90%.
- [ ] Peak weeks are planned explicitly with named levers and lead times.
- [ ] Oldest-item age is reviewed daily and triggers action before the SLA is missed.
