---
id: computing-software.software-engineering.python.environment-variables-and-process-information
name: environment-variables-and-process-information
category: computing-software
field: software-engineering
product: python
tags: [python, py-os, os-environ-process, os-environ, getenv, putenv, cwd, pid, platform, sys-platform]
level: practitioner
status: docs-checked
description: "Read and set environment variables with os.environ, pass modified environments to children, inspect the process (pid, cwd, user, CPU count) and handle Windows key casing."
sources: ["https://docs.python.org/3/library/os.html#os.environ", "https://docs.python.org/3/library/os.html#process-parameters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables and process information

```python
import os, sys, platform, subprocess

os.environ.get("APP_MODE", "dev")              # preferred: default instead of KeyError
os.environ["APP_DEBUG"] = "1"                  # values must be str; calls putenv for children
del os.environ["APP_DEBUG"]
int(os.environ.get("WORKERS", "4"))            # parse and validate once at startup

env = {**os.environ, "LANG": "C.UTF-8", "PYTHONUNBUFFERED": "1"}
subprocess.run(["tool"], env=env, check=True)  # change a COPY for the child, not the parent

os.getpid(), os.getppid(), os.getcwd(), os.cpu_count()
os.process_cpu_count()                          # 3.13+: CPUs this process may use (affinity-aware)
sys.platform                                    # 'linux', 'win32', 'darwin'
platform.system(), platform.machine(), sys.version_info >= (3, 12)
os.path.expanduser("~"), os.getlogin()          # controlling-terminal user; getpass.getuser() checks LOGNAME/USERNAME then the uid
```

## Rules
- Booleans: parse explicitly (`value.lower() in {"1","true","yes"}`); `bool("0")` is `True`.
- Child processes receive the environment you pass (for example `subprocess.run(env=...)`); build a copy without secrets for children that do not need them.
- Config loading belongs in one place (settings object), not scattered `os.getenv` calls.

## Gotchas
- On Windows `os.environ` keys are converted to uppercase (`environ['monty'] = 'python'` maps `'MONTY'`).
- `os.environ` is captured when `os` is first imported; later changes to the process environment made outside Python, or via `os.putenv`/`os.unsetenv`, are not reflected (`os.reload_environ()` refreshes it in newer versions).
- Calling `os.putenv` directly does not change `os.environ`; modify `os.environ` instead, which calls `putenv` automatically. On some platforms (FreeBSD, macOS) setting `environ` may leak memory.
- `os.cpu_count()` is the number of logical CPUs in the system; `os.process_cpu_count()` (3.13+) is the number usable by the calling thread of the current process and can be smaller depending on CPU affinity. `-X cpu_count` or `PYTHON_CPU_COUNT` override both. On Unix `os.sched_getaffinity(0)` is the set of CPUs the process is restricted to.

## Verify
- [ ] Startup logs the resolved (non-secret) settings and fails fast on missing required variables.
- [ ] Tests that change `os.environ` restore it afterwards.

## Checked

- 2026-11-03: checked against the CPython docs `library/os.rst` (`environ`, `putenv`, `getlogin`, `cpu_count`, `process_cpu_count`, `sched_getaffinity`), `library/sys.rst` (`platform` values), `library/getpass.rst` (`getuser`).
- Removed: the `/proc/<pid>/environ` remark, POSIX case-sensitivity claim, `os.chdir` thread-safety claim, the container/cgroup CPU claim and the pytest `monkeypatch` reference.

Method: documentation only; no commands were run.
