---
id: computing-software.data-engineering.data-modelling.activity-schema-and-event-tables
name: activity-schema-and-event-tables
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, activity-schema, event-modelling, event-tables, customer-stream, temporal-joins, funnel-analysis, clickstream, behavioural-data]
level: practitioner
status: draft
description: "Model behavioural data as event tables or an activity stream: event grain and naming, the activity schema spec, temporal joins (first-after, last-before) and when stars still win."
sources:
  - https://github.com/ActivitySchema/ActivitySchema/blob/main/2.0.md
  - https://www.activityschema.com/
  - https://docs.snowplow.io/docs/fundamentals/events/
  - https://segment.com/docs/connections/spec/track/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Activity schema and event tables

**Goal:** answer customer-journey questions (what did users do before converting, time between steps, funnels) without building a new star schema per question.

## 1. Event table basics
- Grain: **one row per thing that happened to an entity at a point in time** (immutable). Never update events; corrections are new events.
- Name events as `object_action` in past tense (`order_placed`, `email_opened`, `subscription_cancelled`) from a controlled list.
- Required columns: event id (unique), entity id (customer), event name, timestamp (UTC), source, and properties (typed columns for common ones, JSON for the rest).
- Separate *when it happened* (`occurred_at`) from *when we learned it* (`loaded_at`) — late events are normal.

## 2. Activity schema (v2 spec)
One table per entity (`customer_stream`) containing every activity:
| Column | Meaning |
|---|---|
| `activity_id` | unique id |
| `ts` | when it happened |
| `customer` | entity identifier |
| `activity` | activity name (`completed_order`) |
| `anonymous_customer_id` | pre-identification id |
| `feature_json` | activity-specific attributes |
| `revenue_impact` | optional amount |
| `link` | optional URL to source record |
| `activity_occurrence` | 1 for the customer's first of this activity, 2 second, ... |
| `activity_repeated_at` | ts of the next same activity by this customer (NULL if none) |
Each activity is built by a small transformation from its source (orders, emails, tickets) and appended. Precomputed `activity_occurrence` and `activity_repeated_at` make temporal joins cheap.

## 3. Temporal joins (the point of the model)
```sql
-- for each first order, did the customer open an email in the 7 days before? (last-before)
SELECT o.customer, o.ts AS first_order_at,
       MAX(e.ts) AS last_email_open_before
FROM customer_stream o
LEFT JOIN customer_stream e
  ON e.customer = o.customer AND e.activity = 'opened_email'
 AND e.ts < o.ts AND e.ts >= o.ts - INTERVAL '7 days'
WHERE o.activity = 'completed_order' AND o.activity_occurrence = 1
GROUP BY 1, 2;

-- first-in-between: first support ticket after each order and before the next order
SELECT o.activity_id, MIN(t.ts) AS first_ticket_after
FROM customer_stream o
LEFT JOIN customer_stream t
  ON t.customer = o.customer AND t.activity = 'opened_ticket'
 AND t.ts > o.ts AND (o.activity_repeated_at IS NULL OR t.ts < o.activity_repeated_at)
WHERE o.activity = 'completed_order'
GROUP BY 1;
```
Relationship types: first ever, last ever, first before, last before, first after, last after, first in between, aggregate in between.

## 4. Performance
- Cluster/partition by `activity` then `customer`/`ts`; most queries filter one or two activities.
- Keep `feature_json` small; promote heavily used features to columns or extract in the query layer.

## 5. When to use what
- Activity stream / event tables: journeys, funnels, attribution, retention, product analytics.
- Star schemas: financial reporting, inventory, aggregates by many conformed dimensions, BI semantic models.
Many teams keep both: events as the source for behavioural analysis, stars for governed metrics.

## Verify
- [ ] Event ids are unique; events are never updated in place.
- [ ] `activity_occurrence` and `activity_repeated_at` recomputed correctly after late events (rebuild per customer when late data arrives).
- [ ] A funnel query returns the same counts as the product analytics tool for the same window (within known differences).
