---
id: computing-software.systems-network-administration.windows-server.printer-driver-isolation
name: printer-driver-isolation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [print-server, printer-driver-isolation, print-spooler, printer-drivers, point-and-print]
level: practitioner
status: docs-checked
description: "Use printer driver isolation so a crashing driver does not take down the Print Spooler: isolated vs shared modes, per-driver settings and PrintIsolationHost."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/print/printer-driver-isolation
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Printer driver isolation

Printer drivers can run in processes separate from the spooler, so a faulting driver component does not halt the print
service. Per Microsoft, a driver whose INF omits `DriverIsolation` (same as `DriverIsolation=0`) is configured to run in
the spooler process; `DriverIsolation=2` declares isolation support and the installer then configures an isolated process.
An administrator can override this per driver.

## Modes per driver
- **None**: driver runs in the spooler process.
- **Shared**: driver runs in a process shared with other drivers but separate from the spooler. Ideal for a compatible driver.
- **Isolated**: separate process, not shared with other drivers; for drivers that conflict with others (file-name clashes,
  frequent faults, memory leaks).
- With no mode set, an isolation-compatible driver runs in shared mode (when isolation is enabled by policy).

## Configure
Use the Windows Print Management console to set each driver's mode (or the spooler functions such as `SetPrinterDataEx`).
If driver isolation is disabled by Group Policy it is off for all drivers; a Group Policy override decides what happens
to drivers that are not isolation-compatible. Find the policy settings by searching the Printers administrative templates.

## Strategy for unstable servers
1. Check the Application log for spooler crashes and the faulting module (driver DLL).
2. Set that driver to **Isolated**.
3. Crashes now affect only that driver's queues.
4. Replace or update the driver and remove unused drivers.

## Gotchas
- Some old drivers fail when forced into isolation (print output wrong or jobs fail); test per driver.

## Verify
- [ ] Spooler stays up after a driver fault; the driver's mode in Print Management is as intended.

## Checked
2026-10-28. Confirmed on Learn "Printer driver isolation": None/Shared/Isolated meanings, DriverIsolation=2/0 and the default for
INFs that omit it, Print Management console and spooler functions, group policy on/off behaviour. The opening default
claim was wrong (default is the spooler process unless the INF declares isolation) and is rewritten. Removed as
unconfirmed: process name, registry path, policy names, event 1000, 2008 R2 gate, Type 3/Type 4 statements.
Method: documentation only; no commands were run.
