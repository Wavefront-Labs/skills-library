---
id: computing-software.systems-network-administration.bash.split-csplit-and-join
name: split-csplit-and-join
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, split-command, csplit, join-command, paste, file-splitting, large-files, lpic-1]
level: practitioner
status: verified
description: "Split big files by lines, bytes or pattern (split, csplit) and reassemble or relationally join sorted files (cat, join, paste), with checksums for safe transfer."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/split-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/csplit-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/join-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# split, csplit and join

## split
```bash
split -b 1G -d -a 3 backup.tar.zst backup.part.      # backup.part.000, 001... (-d numeric suffixes)
split -l 100000 --additional-suffix=.csv big.csv chunk_
split -n l/8 big.log part_                            # 8 pieces without breaking lines
split -l 50000 --filter='gzip > $FILE.gz' big.csv chunk_   # compress on the fly
cat backup.part.* > backup.tar.zst                    # glob order is lexical — keep -a wide enough
sha256sum backup.tar.zst                              # compare with the source checksum
```
CSV with header: `tail -n +2 big.csv | split -l 100000 - part_` then prepend the header to each.

## csplit (by pattern)
```bash
csplit -z -f host_ combined.log '/^=== host/' '{*}'   # new file at each match; -z drop empty
csplit -f sec nginx.conf '/^server {/' '{*}'
```
## join (relational, needs sorted input)
```bash
join -t, -1 1 -2 1 <(sort -t, -k1,1 users.csv) <(sort -t, -k1,1 quotas.csv)
join -a1 -e NULL -o auto -t, a.csv b.csv               # left outer join, fill missing
```
`join: ... is not in sorted order` → sort with the same key and locale (`LC_ALL=C` for both).

## paste
`paste -d, names.txt ages.txt` (side by side); `paste -sd+ nums.txt` turns a column into `1+2+3`, so `echo $(( $(paste -sd+ nums.txt) ))` sums it (prints 6 for 1,2,3).

## Gotchas
- `split` default suffixes (`aa..zz`) run out at 676 pieces → "output file suffixes exhausted"; use `-a`.
- `join` compares as text; numeric IDs need consistent zero-padding or `LC_ALL=C` sorted text.

## Verify
- [ ] Reassembled file checksum equals the original; joined row count matches expectations (`wc -l`).
