---
id: computing-software.software-engineering.elixir.ports-system-cmd-os-processes
name: ports-system-cmd-os-processes
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, port, system-cmd, os-process, open-port, exec, stdin-stdout, muontrap, ports-system-cmd]
level: practitioner
status: docs-checked
description: "Run external programs with System.cmd (blocking) or Port.open (streaming), handle exit status and avoid zombies."
sources: ["https://hexdocs.pm/elixir/System.html", "https://hexdocs.pm/elixir/Port.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ports, System.cmd and external programs

**Goal:** integrate OS tools safely.

```elixir
{out, 0} = System.cmd("git", ["rev-parse", "HEAD"], stderr_to_stdout: true, cd: "/path/to/repo", env: [{"LANG", "C"}])
System.cmd("echo", ["hello"], into: IO.stream())     # stream output as it arrives
System.cmd("echo", ["a\nb"], into: [], lines: 1024)  # {["a", "b"], 0}
System.find_executable("convert")                    # nil when not on PATH

path = System.find_executable("cat")
port = Port.open({:spawn_executable, path}, [:binary, args: []])
Port.command(port, "hello\n")
receive do
  {^port, {:data, data}} -> data
end
Port.close(port)
```

## Rules
- `System.cmd/3` takes an argv list and does not use a shell: no variable interpolation, no wildcard expansion, and arguments need no escaping or quoting for shell safety. For a trusted command that needs pipes or redirection use `System.shell/2`; never build a shell string from user input.
- `System.cmd/3` returns `{collected_output, exit_status}`; `:into` picks the collectable (default `""`), `:lines` (since 1.15.0) reads by lines.
- The child inherits the parent's environment except what `:env` overrides; a `nil` value unsets a variable, which stops credentials leaking into child processes.
- `Port.open/2` with `:spawn_executable` expects a full path (use `System.find_executable/1`) and takes arguments in `:args`, so names and arguments may contain spaces. `{:spawn, "cmd args"}` splits on spaces and searches `$PATH`; prefer `:spawn_executable`.
- Prefer `System.cmd/3` when you only need to run a program and get its result.
- On Windows, never pass untrusted input as arguments to `.bat` or `.com` programs (they run through `cmd.exe`, whose argument parsing is vulnerable); pass the explicit `.exe` extension.
- Orphans: closing a port closes stdin/stdout but does not terminate the program. If the VM crashes, a long-running child is not terminated automatically. Port docs suggest wrapping the child in a script that kills it when stdin closes (the wrapper takes over stdin).

## Failure modes
- `System.cmd/3` raises `ArgumentError` on invalid or unknown options, and fails with POSIX reasons: `:enoent` (command does not point to an existing file), `:eacces` (not executable), `:emfile`, `:enfile`, `:eagain`, `:enomem`, `:system_limit`, `:enametoolong`.

## Self-check
Run `System.cmd("echo", ["a b"])` and note that the argument stays one argument.

## Checked

Checked 2026-11-09 against hexdocs.pm/elixir System (cmd/3, shell/2, find_executable/1) and Port (open mechanisms, orphan OS processes), Elixir v1.20.5 pages.
Confirmed: argv-without-shell semantics, `:into`, `:lines` since v1.15.0, `:cd`, `:env` with nil to unset, `:stderr_to_stdout`, error reasons, `:spawn_executable` with `:args`, `:spawn` splitting, Windows batch-file warning, orphan process behaviour and the stdin-wrapper workaround.
Removed as unconfirmed: the `:exit_status` port option (only in the Erlang open_port docs, not read), the claim that `System.cmd` has no timeout, and MuonTrap behaviour (third-party library; the tag is kept as a name only).

Method: documentation only; no commands were run.
