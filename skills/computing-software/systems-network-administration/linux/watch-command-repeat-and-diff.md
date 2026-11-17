---
id: computing-software.systems-network-administration.linux.watch-command-repeat-and-diff
name: watch-command-repeat-and-diff
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, watch-command, watch, monitoring, differences, interval, procps]
level: intro
status: docs-checked
description: "Re-run a command periodically with watch: interval, -d highlighting changes, -g/-e exit conditions, quoting pipes, precise timing, and when to use a loop instead."
sources:
  - https://man7.org/linux/man-pages/man1/watch.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# watch

```bash
watch -n 2 'ss -s'                                  # every 2 s (default), full-screen
watch -d -n 1 'cat /proc/mdstat'                    # -d highlight what changed (--differences=permanent keeps all changes since the first run)
watch -n 5 "df -h | grep -E '/var|/srv'"            # pipes: quote the whole command
watch -t -n 1 'date; ls -l /srv/incoming | wc -l'   # -t no header
watch -g 'systemctl is-active app'                  # exit when output changes
watch -e -n 10 'curl -fsS localhost:8080/health'    # freeze on command failure, exit after a key press
watch -p -n 0.5 'cat /sys/class/net/eth0/statistics/rx_bytes'  # -p: interval measured from the previous start
watch -c 'ls --color=always'                        # interpret ANSI colours
```
`-x` passes the command to exec(3) instead of `sh -c` (no shell features). `-b` beeps on a non-zero exit. Combine with a final check: `watch -g ... && notify-send done`.

## Loops instead when
- You need a log of each sample (watch overwrites the screen):
  `while sleep 5; do date +%T; ss -s | head -2; done | tee samples.log`
- Running unattended/in scripts (watch needs a terminal).

## Gotchas
- Intervals below 0.1 s are raised to 0.1 s; heavy commands at short intervals add load themselves.
- Aliases and functions aren't available (runs `sh -c`) — use full commands.
- Only the first screenful is shown, and `-g` ignores changes that are off screen; filter the output.

## Verify
- [ ] `-d` shows the counter changing as expected; `-g`/`-e` exits at the right moment in a test.

## Checked

Documentation check. Checked 2026-10-27 against procps-ng watch(1) from the man-pages project (man7.org): the 2 second default, the 0.1 second lower bound, `-d[=permanent]`, `-g` (exit when visible output changes), `-e` (freeze on error, exit after a key press), `-b` (beep), `-p`, `-t`, `-c` and `-x`.
Method: documentation only; no commands were run.
