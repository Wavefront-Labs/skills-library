---
id: computing-software.systems-network-administration.bash.timeout-and-retry-with-backoff
name: timeout-and-retry-with-backoff
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, timeout-command, retry-loop, exponential-backoff, until-loop, robust-scripts, network-calls]
level: practitioner
status: verified
description: "Bound and retry flaky commands in scripts: GNU timeout (exit 124, -k, signals), retry loops with exponential backoff and jitter, and waiting for a service to become ready."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html
  - https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# timeout and retry loops

## timeout
```bash
timeout 30 curl -fsS https://api.example/health          # exit 124 if it timed out
timeout -k 10 300 ./migrate.sh                            # SIGTERM at 300s, SIGKILL 10s later if still alive
timeout -s INT 60 tcpdump -i eth0 -w cap.pcap             # stop with SIGINT so tcpdump flushes
timeout --preserve-status 10 cmd                          # return cmd's status instead of 124
```
Exit codes (timeout(1)): 124 timed out, 125 timeout itself failed, 126 command found but cannot be invoked, 127 not found, 137 if the command (or timeout) is sent SIGKILL (tested: `-k` after a TERM-ignoring command gives 137; `--preserve-status` returns the command's own status, 143 for SIGTERM).
Use `--foreground` when `timeout` is not run directly from a shell prompt and the command must read the TTY and get TTY signals; children of the command are then not timed out. Put options before the duration (`timeout --foreground 1 cmd`).

## Retry with exponential backoff
```bash
retry() {                       # retry <max_attempts> <cmd...>
  local max=$1 n=1 delay=1; shift
  until "$@"; do
    (( n >= max )) && { echo "failed after $n attempts: $*" >&2; return 1; }
    sleep $(( delay + RANDOM % delay ))   # jitter avoids thundering herd
    (( delay *= 2, n++ ))
  done
}
retry 5 timeout 10 curl -fsS -o /tmp/pkg.tgz https://mirror/pkg.tgz
```
## Wait for readiness
```bash
for i in $(seq 1 60); do
  pg_isready -h db -q && break    # exit 0 = accepting connections, 1 = rejecting, 2 = no response, 3 = no attempt (PostgreSQL docs)
  [[ $i -eq 60 ]] && { echo "db not ready" >&2; exit 1; }
  sleep 2
done
```
`curl --retry 5 --retry-all-errors --retry-max-time 120` has its own retry logic.

## Gotchas
- Don't retry non-idempotent actions (POST that creates, `useradd`) blindly.
- `set -e` inside `until cmd` is suspended — fine, but check the final status explicitly.
- Cap total time as well as attempts in CI jobs.

## Verify
- [ ] Simulate failure (wrong host) — script gives up after the expected attempts/time with a clear message and non-zero exit.
