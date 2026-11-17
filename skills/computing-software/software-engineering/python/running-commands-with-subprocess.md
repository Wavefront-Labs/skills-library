---
id: computing-software.software-engineering.python.running-commands-with-subprocess
name: running-commands-with-subprocess
category: computing-software
field: software-engineering
product: python
tags: [python, python-subprocess, subprocess-run, shell-injection, popen, timeout, check-true, command-execution]
level: practitioner
status: verified
description: "Run external commands from Python safely: subprocess.run with argument lists, check, capture, timeouts, encoding, streaming output and avoiding shell injection."
sources: ["https://docs.python.org/3/library/subprocess.html", "https://docs.python.org/3/library/subprocess.html#security-considerations", "https://docs.python.org/3/library/shlex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running commands with subprocess

**Goal:** call git, ffmpeg or any CLI from Python so failures surface, output is
captured correctly, nothing hangs, and user input cannot inject commands.

## The default call
```python
import subprocess
res = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    capture_output=True, text=True, encoding="utf-8",
    check=True, timeout=30, cwd=repo_dir,
)
sha = res.stdout.strip()
```
- `check=True` raises `CalledProcessError` (with `.returncode`, `.stdout`, `.stderr`) on
  non-zero exit. Without it, failures are silent.
- `timeout=` kills the child and raises `TimeoutExpired`. Always set one for network
  tools.
- `text=True` + explicit `encoding` avoids locale-dependent decoding (Windows cp1252).
  Add `errors="replace"` for tools that emit garbage bytes: with `capture_output` and strict decoding, invalid bytes made the reader thread fail and `res.stdout` came back `None` (Python 3.14, Windows).

## Never shell=True with untrusted input
```python
subprocess.run(f"convert {user_file} out.png", shell=True)    # injection: "x; rm -rf ~"
subprocess.run(["convert", user_file, "out.png"])             # safe: no shell parsing
```
Still guard against option injection: a filename `-rf` is parsed as a flag. Use `--`
where the tool supports it: `["git", "log", "--", path]`.
If you truly need shell features (pipes, globs), build the pipeline in Python or quote
each piece with `shlex.quote` (POSIX only).

## Streaming long output
```python
with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as p:
    for line in p.stdout:
        log.info(line.rstrip())
rc = p.wait()
```
Never read stdout then stderr sequentially from separate pipes on a chatty process:
the unread pipe buffer fills and both processes deadlock. Merge them (`stderr=STDOUT`)
or use `communicate()`.

## Environment and PATH
- `env={**os.environ, "LC_ALL": "C"}` - pass a full env; a partial dict drops PATH.
- Resolve the binary with `shutil.which("ffmpeg")` and fail clearly if missing.
- On Windows, `.cmd`/`.bat` scripts (npm, yarn) need `shell=True` or the full
  `npm.cmd` name; and arguments to batch files have their own injection risks.

## Asyncio variant
`asyncio.create_subprocess_exec(...)` for many concurrent commands; same rules.

## Verify
- [ ] A failing command raises with stderr included in the logged error.
- [ ] A filename containing spaces, quotes and `;` is passed through correctly.
- [ ] A hung command is killed by the timeout in tests.

## Checked
- Python 3.14.0 on Windows: `run` with `capture_output`, `text`, `encoding`, `check`, `timeout` behaves as written (`CalledProcessError` carries returncode, stdout, stderr; `TimeoutExpired`); without `encoding` UTF-8 output decodes as cp1252 (`Ã©`); `errors="replace"` yields `a�b` while invalid UTF-8 with the default strict handler printed a `UnicodeDecodeError` from the reader thread and left `stdout` as `None` instead of raising; list arguments with spaces, quotes and `;` arrive intact; `Popen` line streaming works; a child writing 200 KB to an unread stderr pipe blocked (deadlock) while `communicate()` returned both streams; a partial `env` drops PATH and a full one keeps it; `shutil.which` and `FileNotFoundError` for a missing binary; on Windows `npm` alone is `FileNotFoundError`, `npm.cmd` and `shell=True` work; `asyncio.create_subprocess_exec` works. The POSIX `shlex.quote` shell-injection case was not run (Windows `cmd` does not split on `;`).
