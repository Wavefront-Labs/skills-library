---
id: computing-software.systems-network-administration.bash.pv-pipe-viewer
name: pv-pipe-viewer
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, pv-command, pipe-viewer, progress-bar, rate-limit, pipes, dd-progress]
level: intro
status: docs-checked
description: "Show progress, ETA and throughput in pipelines with pv, rate-limit copies (-L), watch a running process's file descriptors (-d) and use it with tar, dd and database restores."
sources:
  - https://www.ivarch.com/programs/pv.shtml
  - https://manpages.debian.org/bookworm/pv/pv.1.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pv: progress for pipelines

```bash
pv backup.tar.zst | zstd -d | tar x                      # progress on file size
tar -cf - /data | pv -s $(du -sb /data | cut -f1) | zstd -T0 > data.tar.zst   # -s gives ETA when size unknown
pv dump.sql.gz | gunzip | mysql appdb                    # restore with ETA
pv -L 20m bigfile | ssh host 'cat > bigfile'             # limit to 20 MiB/s (spare the WAN)
dd if=/dev/sda bs=4M | pv -s 500G | dd of=/dev/sdb bs=4M
pv -d $(pgrep -n rsync)                                  # watch an already-running process's open files
pv -l access.log | grep -c 404                           # count lines (-l) instead of bytes
```
Display options: `-p` progress bar, `-t` timer, `-e` ETA, `-r` rate, `-a` average rate, `-b` bytes,
`-n` numeric output for scripts (`pv -n file 2>&1 >/dev/null | while read p; do ...; done`),
`-N name` label for multiple pv in one pipeline (use with `-c`), `-q` quiet with `-L` for rate limit only.
`-d PID[:FD]` is Linux only; with `-d`, `-s` works only in the `PID:FD` form.

## Gotchas
- pv shows no visual display when standard error is not a terminal unless `-f` forces it.
- Without `-s` and a known size, the bar only moves left and right and `-e` has no effect.
- In a pipeline, place pv where the data volume is meaningful (compressed vs uncompressed sizes differ).

## Verify
- [ ] Progress reaches 100% and the exit status of each pipeline stage is checked.

## Checked
2026-11-01. Confirmed against the Debian pv(1) man page: display switches `-p -t -e -r -a -b -n -q -N -l -s -f -c`,
`-L` rate limit with K/M/G/T suffixes, `-d PID[:FD]` (Linux only), size/ETA behaviour. Removed: dd status=progress,
install commands, cron remark.
Method: documentation only; no commands were run.
