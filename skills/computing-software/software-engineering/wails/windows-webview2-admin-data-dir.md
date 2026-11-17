---
id: computing-software.software-engineering.wails.windows-webview2-admin-data-dir
name: windows-webview2-admin-data-dir
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, windows, webview2, admin, uac, user-data-path]
level: practitioner
status: docs-checked
description: "Resolve the WebView2 data-directory error when a Wails app runs as another admin user on Windows, by dropping constant admin rights or sharing a data dir with extra privileges."
sources: [https://wails.io/docs/guides/troubleshooting]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Microsoft Edge can't read or write to its data directory" when run as admin

## Cause

A Windows machine has an admin account (Alice) and a standard user (Bob). Bob runs your admin-requiring app and enters Alice's credentials at the UAC prompt. Wails tells WebView2 to keep user data at `WebviewUserDataPath`, default `%APPDATA%\[BinaryName.exe]`, which resolves to Alice's profile. WebView2 spawns some child processes under Bob's account, which cannot access Alice's folder, so the error appears.

## Solution 1: avoid constant admin rights

Run with minimum permissions and elevate only for small tasks (e.g. an updater) via `runas`:
```go
//go:build windows
func RunAs(path string) error {
    verbPtr, _ := syscall.UTF16PtrFromString("runas")
    exePtr, _ := syscall.UTF16PtrFromString(path)
    cwdPtr, _ := syscall.UTF16PtrFromString("")
    argPtr, _ := syscall.UTF16PtrFromString("")
    return windows.ShellExecute(0, verbPtr, exePtr, argPtr, cwdPtr, 1) // SW_NORMAL
}
```
(imports `golang.org/x/sys/windows` and `syscall`.)

## Solution 2: shared data dir plus extended privileges

If admin is mandatory, use a data directory both users can access and launch the app with `SeBackupPrivilege`, `SeDebugPrivilege` and `SeRestorePrivilege`. The page's example uses `github.com/fourcorelabs/wintoken` to open the process token and enable those privileges, relaunches itself via `exec.Command` with that token and an env marker (so it only relaunches once), creates the dir (e.g. `a ProgramData subfolder`) with `os.MkdirAll`, opens its ACL with `github.com/hectane/go-acl` (`acl.Chmod(dir, 0777)`), and sets:
```go
Windows: &windows.Options{ WebviewUserDataPath: webviewDir },
```
A shared directory without the extended privileges yields a WebView2 `80010108 The object invoked has disconnected from its clients` error.

## Gaps

The page notes a possible future in-memory WebView2 mode (solution 3), not yet available. The example snippet omits some imports (`fmt`, `exec`, `syscall`) that you must add.

## Checked

2026-11-07. Read the whole Troubleshooting guide (website/docs/guides/troubleshooting.mdx), specifically the "Microsoft Edge can't read or write to its data directory" section: the Alice/Bob cause, default WebviewUserDataPath of %APPDATA%\[BinaryName.exe], possible solution 1 (runas example with golang.org/x/sys/windows and syscall), possible solution 2 (SeBackupPrivilege, SeDebugPrivilege, SeRestorePrivilege; wintoken, go-acl, env-marker relaunch, os.MkdirAll, acl.Chmod 0777), the 80010108 error and the possible future in-memory solution 3. Confirmed the Gaps note: the page's code imports omit fmt, os/exec and syscall though it uses them. The linked WebView2Feedback issues and the wintoken and go-acl packages were not opened. No claims were trimmed.

Method: documentation only; no commands were run.
