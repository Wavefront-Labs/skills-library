---
id: computing-software.software-engineering.r.r-subset-assignment
name: r-subset-assignment
category: computing-software
field: software-engineering
product: r
tags: [r, r-subsetting, subset-assignment]
level: practitioner
status: draft
description: "Modify vectors, lists and data frames by index, name or logical condition without breaking types."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assigning with subsetting and in-place modification
- `x[x > 5] <- 0` assigns by condition; `x[["k"]] <- v` sets a list element; `df[df$a > 1, "b"] <- NA`.
- Assigning a character into a numeric vector coerces the whole vector to character.
- Assigning beyond the length extends the vector and fills with NA.
- `df$new <- NULL` drops a column; `df[order(df$a), ]` sorts rows.
Verify: `str(x)` after modification to confirm types did not change.
