---
id: computing-software.general-digital-literacy.basic-troubleshooting.everyday-troubleshooting-method
name: everyday-troubleshooting-method
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, troubleshooting, tech-support, restart, reboot, updates, windows-update, macos-update, wifi, connectivity, router, dns, ping, ipconfig, task-manager, force-quit, error-messages, screenshot, safe-mode, disk-space, isolate-the-problem, help-desk, bug-report, tech-support-scam]
level: intro
status: draft
description: "A repeatable ladder for everyday computer problems: describe it, restart properly, update, check connectivity, read the exact error, isolate the cause, ask well."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Everyday troubleshooting method — fix most problems yourself, escalate well

**Goal:** resolve the common 80% (frozen app, no internet, "it was working yesterday")
with a fixed sequence instead of random clicking, and hand the rest to support with
enough detail that they can fix it first time.

## 1. Pin the problem down (one minute, saves twenty)
Write down:
- **What exactly happens** — the exact error text, not "it broke". Screenshot it:
  Windows `Win+Shift+S`, macOS `Cmd+Shift+4` (or `Cmd+Shift+5` for options).
- **What changed** since it last worked: an update, new software, new Wi-Fi, a moved file.
- **Scope:** one app or everything? one website or all? one device or all devices on
  this network? one user or everyone?
- **Repeatable?** The steps that make it happen again.
Scope usually points straight at the cause: all devices offline = the router or
provider; one site down for everyone = their problem, not yours.

## 2. The escalation ladder — stop at the first rung that works
1. **Retry / wait 30 seconds.** Many errors are momentary timeouts.
2. **Close and reopen the app.** If it's frozen: Windows Task Manager (`Ctrl+Shift+Esc`)
   › select › End task; macOS Force Quit (`Cmd+Option+Esc`).
3. **Restart the device — choose Restart, not Shut down.** On Windows, Fast Startup
   means a shutdown can resume a saved kernel state; *Restart* gives the full fresh
   start. A machine that has been "on" for weeks often just needs this.
4. **Update** the OS and the misbehaving app (Windows: Settings › Windows Update;
   macOS: System Settings › General › Software Update; browsers update from their
   About page). Restart again after updating.
5. **Check free space** — under ~10% free disk causes slowdowns and failed updates.
6. **Undo the recent change** (uninstall the new program, roll back a driver, reconnect
   to the old network).
7. **Isolate:** try another browser or a private window, another user account, another
   device, safe mode. If it works elsewhere, the problem is local to the thing you swapped out.
8. **Search the exact error** (in quotes, plus the app and OS name) — see
   searching-and-evaluating-sources. Prefer the vendor's support site and recent answers.
9. **Ask for help** (section 4).

## 3. No internet: a quick split
1. Other devices on the same Wi-Fi working? If **no** → restart the router/modem: unplug
   power, wait ~30 s, plug in, give it 2–3 minutes to come back.
2. If only this device: toggle Wi-Fi off/on, "forget" and rejoin the network, or try a
   cable or phone hotspot.
3. Command-line check (Windows Command Prompt / macOS Terminal):
   ```
   ping 1.1.1.1        # reaches the internet by number?
   ping example.com    # reaches it by name?
   ```
   First works but second fails → name lookup (DNS) problem. On Windows try
   `ipconfig /flushdns`; or switch DNS to your router's default/a public resolver.
   Both fail → not connected; `ipconfig` (Windows) shows whether you even have an
   address — one starting `169.254.` means the router never gave you one.
   Note: some networks block ping, so a failure there is a hint, not proof.
4. One website only: check it from your phone on mobile data, or a "is it down"
   service. If it's down for everyone, wait.

## 4. Asking for help well
Send: what you were trying to do, the exact error (screenshot), when it started and
what changed, what you've already tried from the ladder above, device + OS + app
version. One clear message gets a fix; "my computer's broken" gets a round of questions.

## 5. Safety: the fake-support trap
A pop-up or call saying your computer is infected and giving a **phone number to ring**
is a scam — real Microsoft/Apple warnings never do this. Close the browser (Task Manager
if it won't close), and never let an unsolicited caller install remote-access software
or "verify" a payment. Only accept remote help you initiated through a known channel.

## Verify
- [ ] You can state the problem's scope (app / device / network / everyone) before acting.
- [ ] You used *Restart*, not shut down, and applied pending updates.
- [ ] For network issues you know whether it's the router, the device, DNS or the site.
- [ ] Any escalation includes exact error, steps tried and versions.
- [ ] No phone number from a pop-up was called; no stranger got remote access.
