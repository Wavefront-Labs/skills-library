---
id: computing-software.software-engineering.r.r-sprintf-paste-format
name: r-sprintf-paste-format
category: computing-software
field: software-engineering
product: r
tags: [r, r-strings, sprintf-paste-format]
level: practitioner
status: docs-checked
description: "Build strings with paste0, sprintf, format and handle encodings with enc2utf8."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/paste.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/sprintf.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/format.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Encoding.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/iconv.html", "https://stat.ethz.ch/R-manual/R-devel/library/utils/html/read.table.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# paste, sprintf, format and encoding
- `paste(..., sep = " ", collapse = NULL, recycle0 = FALSE)`: `collapse` joins to one string; `recycle0 = TRUE` makes zero-length arguments give a zero-length result (`?paste`).
- `format(x, nsmall = 0L, big.mark = "", ...)` takes `nsmall` and `big.mark` (`?format`); `sprintf` is the C-style formatter (`?sprintf`).
- `enc2utf8(x)` and `Encoding(x)` are on `?Encoding`; `iconv(x, from, to)` converts encodings (`?iconv`); `read.table` and `read.csv` take `fileEncoding` (`?read.table`).
Verify: Compare `nchar(x, "bytes")` and `nchar(x)` for non-ASCII input.

## Checked

Date: 2026-11-02. Confirmed on: ?paste (recycle0), ?format (nsmall, big.mark), ?Encoding (enc2utf8), ?iconv, ?read.table (fileEncoding), ?sprintf exists. Removed as not confirmed on those pages: The R 4.0.1 version gate for recycle0, the sprintf %d integer-valued remark, and the formatC example (not read on these pages).

Method: documentation only; no commands were run.
