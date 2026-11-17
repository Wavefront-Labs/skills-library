---
id: computing-software.systems-network-administration.bash.awk-reports-and-aggregation
name: awk-reports-and-aggregation
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, awk, gawk, awk-aggregation, awk-report, associative-arrays, group-by, sum-column, begin-end, printf, field-separator, log-analysis, text-processing, sysadmin]
level: practitioner
status: gated
description: "Use awk as a one-pass report engine: group-by with associative arrays, sums/max/averages per key, BEGIN/END blocks, printf tables, and sorting the result."
sources:
  - https://www.gnu.org/software/gawk/manual/gawk.html
  - https://man7.org/linux/man-pages/man1/awk.1p.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# awk reports and aggregation — group-by without a database

**Goal:** turn a log or CSV into a per-key summary (count, sum, max, average) in one pass,
formatted as a readable table.

## 1. The pattern: accumulate in arrays, print in END
```bash
# requests and bytes per client IP from an nginx access log
awk '{ n[$1]++; bytes[$1]+=$10 }
     END { for (ip in n) printf "%-16s %8d %12d\n", ip, n[ip], bytes[ip] }' access.log | sort -k2 -rn | head
```
- `n[$1]++` creates the key on first sight; arrays are associative (string keys), unordered.
- `for (k in arr)` order is arbitrary — pipe to `sort`, or in gawk set
  `PROCINFO["sorted_in"]="@val_num_desc"` before the loop.
- Uninitialised values are `0`/`""`, so `+=` and `++` need no setup.

## 2. Common aggregates
```bash
awk '{ s+=$3 } END { print s }'                            # sum
awk '{ s+=$3 } END { print (NR ? s/NR : 0) }'              # average (guard NR=0)
awk '$3 > max { max=$3; row=$0 } END { print row }'        # row holding the max
awk '!seen[$2]++'                                           # first occurrence per key (dedupe keeping order)
awk '{ c[$2]++ } END { for (k in c) if (c[k] > 1) print k, c[k] }'   # keys seen more than once
awk -F, 'NR>1 { sum[$1]+=$4 } END { for (k in sum) print k "," sum[k] }' sales.csv  # skip header
```
Status-code histogram: `awk '{ c[$9]++ } END { for (k in c) print c[k], k }' access.log | sort -rn`.

## 3. Field handling that bites
- `-F,` is a single char; `-F'[,;]'` is a regex; `-F'\t'` for tabs. Quoted CSV with
  embedded commas needs gawk `--csv` (new in gawk 5.3.0 per its NEWS; gawk 5.0.0 here rejects the option) or `FPAT='([^,]+)|("[^"]+")'`.
- `$NF` is the last field, `$(NF-1)` the one before. `NF` changes per line.
- Whitespace default FS collapses runs and trims — ideal for `ps`/`df` output.
- Set `OFS` when rebuilding lines: `awk 'BEGIN{OFS=","} {$1=$1; print}'` (the `$1=$1`
  forces reassembly with the new OFS).

## 4. Formatting
```bash
awk 'BEGIN { printf "%-20s %10s\n", "USER", "RSS(MB)" }
     NR>1 { rss[$1]+=$6 }
     END { for (u in rss) printf "%-20s %10.1f\n", u, rss[u]/1024 }' <(ps aux)
```
`printf` does not add a newline; `%-20s` left-aligns; `%'d` groups thousands in gawk with
a locale that supports it.

## 5. Time windows and multi-file
- `FNR==1 { file=FILENAME }` to track which file you are in; `NR` is global, `FNR` per file.
- Two-file lookup: `awk 'NR==FNR { allow[$1]; next } ($1 in allow)' allowlist.txt data.txt`.
- Bucket by hour: `awk '{ split($4, t, ":"); h[t[2]]++ } END { for (k in h) print k, h[k] }' access.log | sort`.

## Failure modes
- Totals look wrong: a field shifted because a value contained a space (user agents,
  quoted strings). Check `NF` distribution first: `awk '{print NF}' f | sort | uniq -c`.
- String vs numeric comparison: input fields that look like numbers compare numerically (`echo "10 9" | awk '{print ($1 < $2)}'` prints 0), but string constants, concatenated values (`$1 ""`) and fields that do not look numeric compare as strings (`"10" < "9"` is 1). Force numeric with `$3+0`.
- `mawk` (Debian default) lacks `PROCINFO`, `--csv` and some functions — `apt install gawk`
  or write portable awk. (gated: unconfirmed, source is paywalled or blocked; mawk is not installed here, and gawk 5.3 was not available to run `--csv`)
- Large key spaces (millions of distinct IPs) can exhaust RAM; pre-filter or use `sort | uniq -c`.

## Verify
- [ ] Sum of per-key counts equals `wc -l` of the filtered input.
- [ ] A hand-checked key (one IP, one user) matches `grep -c` for that key.
