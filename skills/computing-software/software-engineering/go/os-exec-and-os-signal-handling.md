---
id: computing-software.software-engineering.go.os-exec-and-os-signal-handling
name: os-exec-and-os-signal-handling
category: computing-software
field: software-engineering
product: go
tags: [go, golang, os-exec, os-signal, subprocess, signal-notifycontext, sigterm, graceful-shutdown, process-groups, go-process-system, go-exec-safety, go-signal-shutdown]
level: practitioner
status: verified
description: "Run subprocesses safely with os/exec (CommandContext, WaitDelay, no shell, output capture) and handle SIGINT/SIGTERM with signal.NotifyContext for clean shutdown."
sources: ["https://pkg.go.dev/os/exec", "https://pkg.go.dev/os/signal", "https://go.dev/blog/path-security", "https://pkg.go.dev/syscall#SysProcAttr"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# os/exec and os/signal handling

**Goal:** subprocesses that cannot hang or be injected, and a process that shuts down cleanly when
the orchestrator sends SIGTERM.

## Running commands
```go
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
cmd := exec.CommandContext(ctx, "git", "-C", dir, "log", "-1", "--format=%H")
cmd.WaitDelay = 5 * time.Second        // Go 1.20: bound waiting for I/O after kill
var stderr bytes.Buffer
cmd.Stderr = &stderr
out, err := cmd.Output()
if err != nil {
    var ee *exec.ExitError
    if errors.As(err, &ee) { return fmt.Errorf("git exit %d: %s", ee.ExitCode(), stderr.String()) }
    return err
}
```
- Arguments go straight to `execve`; there is no shell, so no injection via spaces or `;`. Never
  build `exec.Command("sh", "-c", userInput)`. If user input becomes an argument, put `--` before it
  so it cannot be parsed as a flag.
- `CommandContext` kills the process (SIGKILL on Unix, TerminateProcess on Windows; `Wait` returns `exit status 1` there) when ctx ends. Customise with `cmd.Cancel = func()
  error { return cmd.Process.Signal(os.Interrupt) }` for a graceful stop, plus `WaitDelay` as the
  hard limit. On Windows `Process.Signal(os.Interrupt)` returns `not supported by windows`, so this recipe degrades to a hard kill after `WaitDelay` (checked).
- Without `WaitDelay`, a killed child whose grandchild still holds stdout open makes `Wait` block
  forever (checked on Windows: still blocked after 4 s; with `WaitDelay` 1 s `Run` returned after 1.3 s).
- `cmd.Env = append(os.Environ(), "FOO=1")`; nil Env inherits the parent environment.
- `CombinedOutput` for simple cases; for large output stream via `StdoutPipe` and finish reading
  before calling `Wait`.
- PATH security: since Go 1.19 `LookPath` refuses to resolve a program from the current directory
  (`exec.ErrDot`) on Unix. Windows differs: with Go 1.25.1, `LookPath("prog")` with `prog.exe` only in the current directory returned plain not-found, not `ErrDot`. Use absolute paths for privileged tools.

## Killing a whole process tree (Unix)
```go
cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
// later: syscall.Kill(-cmd.Process.Pid, syscall.SIGTERM)   // negative pid = process group
```
On Windows use Job Objects (`golang.org/x/sys/windows`) for the same effect.

## Signals and graceful shutdown
```go
func main() {
    ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
    defer stop()
    srv := &http.Server{Addr: ":8080", Handler: mux}
    go func() {
        if err := srv.ListenAndServe(); !errors.Is(err, http.ErrServerClosed) { log.Fatal(err) }
    }()
    <-ctx.Done()
    stop()   // restore default: a second Ctrl-C kills immediately
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
    defer cancel()
    srv.Shutdown(shutdownCtx)
}
```
- With `signal.Notify(ch, ...)` the channel must be buffered (`make(chan os.Signal, 1)`), or
  signals are dropped.
- SIGKILL and SIGSTOP cannot be caught. Kubernetes sends SIGTERM, waits
  `terminationGracePeriodSeconds` (default 30s), then SIGKILL - keep shutdown below that.
- In containers your binary must be PID 1 receiving the signal: use exec-form `ENTRYPOINT
  ["/app"]`, not `sh -c`, or add `tini`.
- SIGHUP is a conventional reload trigger; handle it on its own channel.

## Verify
- [ ] A hung child is killed at the timeout and `Wait` returns within WaitDelay.
- [ ] `kill -TERM <pid>` drains in-flight requests and exits 0.
- [ ] No shell invocation with interpolated input (`grep -rn '"sh", "-c"'`).
## Checked
Run on Windows with Go 1.25.1: `CommandContext` kill at the timeout, grandchild holding stdout with and without `WaitDelay`, `Cancel` hook with `os.Interrupt`, `ExitError.ExitCode()`, nil `Env` inheriting, `append(os.Environ(), ...)`, `git -C` with stderr capture. Not run: `Setpgid` and `syscall.Kill(-pid)` (Unix only), Job Objects, `signal.NotifyContext` delivery and the second-Ctrl-C behaviour, buffered-channel signal drops, PID 1 and `tini` in containers, Kubernetes timing. `sh -c` exists on this machine only because Git for Windows is on PATH; do not assume it on Windows.
Linux pass (same setup): `CommandContext` kill reports `signal: killed`; the `Cancel` hook with `os.Interrupt` works (process ended with `signal: interrupt` at the 300 ms deadline, no WaitDelay needed); `Setpgid` plus `syscall.Kill(-pid, SIGTERM)` terminated the child (`signal: terminated`); the grandchild-holds-stdout hang without `WaitDelay` reproduces identically; `signal.NotifyContext` with SIGTERM drained a request and exited 0. `LookPath` ErrDot was not triggered because PATH had no `.` entry.
