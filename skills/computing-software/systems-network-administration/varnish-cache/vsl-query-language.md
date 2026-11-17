---
id: computing-software.systems-network-administration.varnish-cache.vsl-query-language
name: vsl-query-language
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vsl-query, log-filtering, vxid, timestamp-queries]
level: advanced
status: docs-checked
description: "Filter Varnish logs with VSL queries: record selection (level, taglist, prefix, field), operators, boolean logic, grouping, and ready queries for errors, slow requests and passes."
sources:
  - https://www.varnish.org/docs/reference/vsl-query/
  - https://www.varnish.org/docs/tutorials/vsl-cheatsheet/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vsl query language

Queries go to `-q` of varnishlog, varnishncsa, varnishtop and varnishhist. A query runs on a group of transactions and is true if any log record in the group satisfies it. Syntax: `{level}taglist:record-prefix[field] operator operand`; only the taglist is mandatory, and a bare selection is true if any record matches.

- level: limits to that transaction level (levels start at 1; 0 only in raw grouping); `2+` means at least 2, `2-` at most 2. A request restart does not raise the level.
- taglist: comma-separated tag names or globs with `*` at the start or end; a single `*` selects all tags.
- record-prefix: matches records whose content starts with prefix then a colon, case-insensitively (handy for headers).
- field: whitespace-separated field number, counting from 1.
- Operators: `== != < <= > >=` numeric; `eq ne` string; `~ !~` PCRE2 regex. Operands are quoted or unquoted (unquoted allows only a-z A-Z 0-9 + - _ . *). An operand without a period or exponent is an integer; with one it is a float. Compare timestamps with a trailing dot (`> 8.`); the cheatsheet warns that `> 8` gives the wrong parse.
- Logic: `not`, `and`, `or` in decreasing precedence, with parentheses.
- `vxid <numeric operator> <integer>` queries the transaction id, available from the X-Varnish header, the Guru Meditation page, or Begin and Link records.
- A query must fit on one line (a trailing backslash continues it). Several queries, one per line, are ORed; empty lines are ignored and `#` starts a comment.

Grouping with `-g`: `vxid` (default, nothing grouped), `request` (request plus its backend requests and ESI subrequests), `session` (everything from a client connection; open-ended with keep-alive and memory hungry), `raw` (each record is its own transaction, including vxid 0 data). varnishlog normally shows individual transactions; `-d` reads the backlog; `-w` writes a binary file that varnishlog or varnishncsa can read with `-r`.

Examples from the pages:

```
RespStatus >= 500
RespStatus != 200 and RespStatus != 304
ReqURL eq "/foo"
ReqHeader:Host eq api.example.com
RespHeader:Server ~ apache
not ReqHeader:cookie
Timestamp:Resp[2] > 5.           # slow client
Timestamp:BerespBody[2] > 5.     # slow backend
vxid == 47822
VCL_Log:tagA                     # set by std.log("tagA: valueA")
VCL_Log:tagA eq valueA
Link[3] eq pass                  # passes
HitMiss                          # hit-for-miss
TTL[6] eq uncacheable            # backend responses marked hit-for-miss (also shows hit-for-pass insertions)
Link[3] eq pass and VCL_return eq lookup   # hit-for-pass requests
TTL[1] eq HFP                    # hit-for-pass insertions
BerespStatus >= 500 or {2+}Timestamp:Process[2] > 1.   # with request grouping
vxid == 0 and Error              # with raw grouping
```

## Checked

Method: 2026-11-08 docs-only read of the vsl-query reference and the VSL cheatsheet. Corrected the earlier "ESI subrequests" comment to the page's combined example, and added the hit-for-miss and hit-for-pass queries, level syntax and memory caveat. The `TTL[6] eq uncacheable` one-liner is said by the page to work only without -g.
