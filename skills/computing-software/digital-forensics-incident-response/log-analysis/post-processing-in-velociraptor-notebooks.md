---
id: computing-software.digital-forensics-incident-response.log-analysis.post-processing-in-velociraptor-notebooks
name: post-processing-in-velociraptor-notebooks
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-notebooks, velociraptor, vql, hunt-analysis, notebooks, stacking, dfir]
level: practitioner
status: draft
description: "Analyse Velociraptor hunt and collection results in notebooks: source(), VQL cells, stacking, joins, enrichment, timelines and exporting findings."
sources: ["https://docs.velociraptor.app/docs/notebooks/", "https://docs.velociraptor.app/docs/vql/", "https://docs.velociraptor.app/vql_reference/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-processing in Velociraptor notebooks

**Goal:** turn raw hunt output from hundreds or thousands of endpoints into answers, inside the
Velociraptor GUI, with reproducible VQL.

## Where notebooks live
- Every hunt and every collection has its own notebook (Notebook tab), pre-populated with a
  cell per artifact source.
- Global notebooks (Notebooks menu) for cross-hunt analysis; templates via notebook artifacts.
- Cell types: VQL, Markdown. Cells re-run on demand; results are paged tables, with
  column-level filtering and sorting.

## Core VQL patterns
```sql
-- All rows of an artifact source from this hunt
SELECT * FROM source(artifact="Windows.System.Pslist")

-- Stack: how many clients have each binary
SELECT Name, Exe, count() AS Hosts
FROM source(artifact="Windows.System.Pslist")
GROUP BY Exe ORDER BY Hosts LIMIT 50

-- Filter with regex and add client hostname
SELECT client_info(client_id=ClientId).os_info.hostname AS Host, Name, CommandLine
FROM source(artifact="Windows.System.Pslist")
WHERE CommandLine =~ "(?i)-enc|frombase64string|downloadstring"

-- Join two sources (e.g. netstat with pslist) on client and pid
LET procs <= SELECT ClientId, Pid, Exe FROM source(artifact="Windows.System.Pslist")
SELECT * FROM foreach(row={SELECT ClientId AS C, Pid AS P, Raddr FROM source(artifact="Windows.Network.Netstat")},
  query={SELECT C, P, Raddr, Exe FROM procs WHERE ClientId = C AND Pid = P})
```
- `source()` arguments: `artifact=`, `source=` (artifact sub-source), `hunt_id=`, `client_id=`,
  `flow_id=` for use in global notebooks.
- Use `LET x <= ...` (materialise) for reuse across a cell; `memoize`/`dict` for lookups.
- Enrichment: `lookup_ip`-style artifacts, hash lookups, `parse_csv()` on uploaded IOC lists.
- Timelines: add events to a Velociraptor timeline (`timeline_add`) or export to Timesketch.

## Exporting
- Download a cell's table as CSV/JSON; export the whole notebook as HTML or a ZIP with data.
- Keep notebook VQL as part of the case record so others can rerun it.

## Practical tips
- Filter early (WHERE on source rows) to keep cells fast on large hunts.
- Markdown cells document reasoning between query cells; the notebook becomes the hunt report.
- Long-running cells can be cancelled; prefer GROUP BY on server-side results over pulling
  everything into the browser.

## Self-check
Every finding in your report links to a notebook cell whose VQL reproduces it from the hunt data.
