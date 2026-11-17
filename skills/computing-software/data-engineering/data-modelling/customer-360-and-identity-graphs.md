---
id: computing-software.data-engineering.data-modelling.customer-360-and-identity-graphs
name: customer-360-and-identity-graphs
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, identity-graph, customer-360, identity-resolution, deterministic-matching, probabilistic-matching, graph-components]
level: practitioner
status: draft
description: "Build a customer 360 with an identity graph: identifier edges, deterministic and probabilistic matching, connected components, stable person IDs and over-merge safeguards."
sources:
  - https://segment.com/docs/unify/identity-resolution/
  - https://github.com/zinggAI/zingg
  - https://spark.apache.org/docs/latest/graphx-programming-guide.html#connected-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customer 360 and identity graphs

An identity graph links identifiers (emails, phone numbers, device IDs, cookie IDs, loyalty numbers, CRM IDs) observed together. Connected groups become one person/household, which is the key for a customer 360 view.

## 1. Collect edges
```sql
CREATE TABLE identity_edges (
  id_a_type TEXT, id_a TEXT, id_b_type TEXT, id_b TEXT,
  source TEXT, observed_at TIMESTAMP, confidence NUMERIC
);
-- examples: (email, 'a@x.com') -- (crm_id, 'C123') from CRM; (cookie, 'ck1') -- (email, 'a@x.com') from login event
```
Normalise first: lowercase/trim emails (and decide on Gmail dot/plus handling), E.164 phone numbers, hashed identifiers consistently salted.

## 2. Matching rules
- **Deterministic**: exact match on strong identifiers (login ID, verified email, loyalty number). High precision.
- **Probabilistic/fuzzy**: name + address + DOB similarity (Fellegi-Sunter, Splink, Zingg) with thresholds; produce edges with confidence, often reviewed.
- Rank identifier strength; never merge on weak shared identifiers (shared household IP, a call centre's default phone `0000000000`, `test@test.com`).

## 3. Resolve components
Iterative label propagation in SQL (works in any warehouse):
```sql
-- nodes start with own id as label; repeat until no label changes
UPDATE node_labels n SET label = sub.min_label
FROM (SELECT e.node, MIN(l.label) AS min_label
      FROM edges_both_directions e JOIN node_labels l ON l.node = e.neighbor
      GROUP BY e.node) sub
WHERE n.node = sub.node AND sub.min_label < n.label;
```
Or Spark GraphFrames `connectedComponents()`, Neo4j GDS WCC.

## 4. Safeguards against over-merging
- Cap component size (e.g. > 50 identifiers = suspicious) and quarantine giant components for review; they usually come from a shared junk identifier.
- Per-type limits: a person rarely has > 5 emails or > 3 phone numbers.
- Blocklist known shared identifiers.
- Keep edges with provenance so a bad source can be removed and the graph recomputed.

## 5. Stable person IDs
Components change as edges arrive (merges and splits). Assign a persistent `person_id` and maintain it: when components merge, keep the oldest ID and record `merged_into`; on split, the larger part keeps the ID. Downstream tables need the mapping history to restate metrics.

## 6. The 360 view
Join profile attributes (survivorship rules per attribute: most recent, most trusted source), aggregates (LTV, last order, channels), consent flags. Serve to CDP/activation tools via reverse ETL.

## Privacy
- Consent and purpose limits apply to the graph itself (linking identities is processing under GDPR/CCPA).
- Deletion requests must remove the person's identifiers and edges and recompute affected components.
- Hash identifiers in shared environments; limit who can see raw PII.

## Verify
- [ ] Component size distribution monitored; no unexplained giant components.
- [ ] Sampled matches reviewed for precision; person_id mapping history retained.
