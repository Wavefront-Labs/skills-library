---
id: computing-software.software-engineering.r.r-dbi-dbplyr
name: r-dbi-dbplyr
category: computing-software
field: software-engineering
product: r
tags: [r, r-databases, dbi-dbplyr]
level: practitioner
status: draft
description: "Query databases from R with DBI, bind parameters instead of pasting SQL and use dbplyr lazily."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DBI connections, parameterised queries and dbplyr
- `con <- DBI::dbConnect(RSQLite::SQLite(), "x.db")`; always `dbDisconnect(con)` (use `on.exit`).
- `dbGetQuery(con, "SELECT * FROM t WHERE id = ?", params = list(5))` avoids SQL injection; `glue::glue_sql()` for interpolation.
- `tbl(con, "t") |> filter(x > 1) |> collect()` translates to SQL lazily; `show_query()` prints it; `collect()` pulls data into memory.
- `dbWriteTable(con, "t", df, append = TRUE)`; use `pool` for Shiny.
- Credentials from environment variables, not code.
Verify: `show_query()` and compare row counts against SQL run by hand.
