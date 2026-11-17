---
id: computing-software.systems-network-administration.linux.cups-printing
name: cups-printing
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cups, printing, lpadmin, lpstat, lp, lpr, cupsd, ipp, ipp-everywhere, driverless, ppd, airprint, avahi, print-server, print-queue, cancel, cupsenable, cupsd-conf, lpoptions, lpic-1, sysadmin, cups-sharing, cups-troubleshooting, lpinfo, printer-discovery]
level: intro
status: docs-checked
description: "Set up and operate CUPS printing on Linux: driverless IPP queues, lpadmin/lpstat/lp, sharing to the LAN and AirPrint clients, cupsd.conf access control, clearing stuck jobs and paused queues."
sources:
  - https://openprinting.github.io/cups/doc/help/man-lpadmin.html
  - https://openprinting.github.io/cups/doc/help/man-cupsd.conf.html
  - https://openprinting.github.io/cups/
  - https://github.com/OpenPrinting/cups/tree/master/doc/help
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# CUPS printing — add a queue, share it, unstick it

**Goal:** a printer queue that works from Linux, Windows and phones, with no vendor
driver when the printer speaks IPP, and a quick path when "nothing prints".

## 1. Install and find printers
```bash
dnf install cups                   # or: apt install cups
systemctl enable --now cups        # web UI: http://localhost:631 (admin users belong to a SystemGroup group)
lpinfo -v                          # available devices (backends)
lpinfo -m                          # available drivers/PPDs
```

## 2. Add a queue
```bash
# IPP Everywhere (preferred): queries the printer at the IPP device URI
lpadmin -p office -E -v "ipp://printer.corp.example/ipp/print" -m everywhere
# with a PPD for an older printer (models other than everywhere are deprecated, lpadmin(8))
lpadmin -p oldprn -E -v "socket://10.0.10.20:9100" -P file.ppd
lpadmin -d office                  # default printer
lpoptions -p office -l             # printer options (duplex, trays)
lpoptions -p office -o sides=two-sided-long-edge -o media=A4   # default options (user-level: ~/.cups/lpoptions)
```
- `-E` after `-p` enables the queue and accepts jobs; without it the queue exists but is stopped.
- `socket://host:9100` is the raw TCP (AppSocket) backend URI and `lpd://` the LPD one; see backend(7) and lpadmin(8).

## 3. Print and manage jobs
```bash
lp -d office -o sides=two-sided-long-edge -n 2 report.pdf
lpstat -p -d          # printer states and default
lpstat -o             # queued jobs
cancel 42; cancel -a office                         # one job / all jobs on a queue
cupsenable office; cupsaccept office                # resume a queue that paused after an error
cupsdisable -r "toner" office                       # pause with a reason
lpstat -t                                           # everything at once
```
CUPS can stop a queue when a backend reports an error, depending on the error policy. `cupsenable` restarts it after the cause is resolved; `lpadmin -p office -o printer-error-policy=retry-job` (or `ErrorPolicy retry-job` in `cupsd.conf`) retries the job at a future time instead.

## 4. Share it (print server)
```bash
cupsctl --share-printers --remote-admin    # listen on all interfaces; writes cupsd.conf
lpadmin -p office -o printer-is-shared=true
firewall-cmd --add-service=ipp --permanent  # IPP, 631/tcp by default
```
`/etc/cups/cupsd.conf` for finer control:
```
Listen 0.0.0.0:631
Browsing On
BrowseLocalProtocols dnssd
<Location />
  Order allow,deny
  Allow @LOCAL
</Location>
<Location /admin>
  Order allow,deny
  Allow 10.0.0.0/8
  Require user @SYSTEM
</Location>
```
Clients then find `ipp://server:631/printers/office`. `BrowseLocalProtocols` defaults to `_cups,_print,_universal` (advertising to CUPS, IPP Everywhere and AirPrint clients); `dnssd` advertises via DNS-SD.

## 5. Troubleshooting
```bash
cupsctl --debug-logging; tail -f /var/log/cups/error_log   # then cupsctl --no-debug-logging
lpstat -p office -l                       # "Unable to connect", "Filter failed", "Paused"
ls /var/spool/cups                        # job files
```
| Symptom | Fix |
|---|---|
| "Filter failed" | wrong or missing PPD or filters; try `-m everywhere` |
| Job stays "processing", printer idle | wrong URI/port; `nc -zv printer 631` or `9100` |
| Blank/garbage pages | raw queue (`-m raw`) receiving PDF; use a proper driver, or print PostScript/PCL |
| Queue paused after the printer was off | set `printer-error-policy=retry-job` |
| Can't add printers in the web UI | user not in a `SystemGroup` group (`cups-files.conf`) |

## Verify
- [ ] `lpstat -p` shows the queue `idle, enabled`; `lp -d office /etc/hostname` prints a page.
- [ ] A second host (and a phone, if AirPrint is wanted) discovers and prints to the shared queue.
- [ ] Powering off the printer mid-job and back on: the job completes without manual `cupsenable`.

## Checked
2026-10-27. Checked against the OpenPrinting CUPS help manual pages in the repository (lpadmin, lpinfo, lp, cancel, cupsenable, cupsctl, cupsd.conf, cups-files.conf, backend). Confirmed: lpadmin -E after -p enables the queue, -m everywhere queries the printer at the IPP device URI, other models are deprecated, printer-error-policy values including retry-job, printer-is-shared; cupsctl --share-printers, --remote-admin, --debug-logging; cupsenable and cupsdisable -r reason; lp -n and -o sides=two-sided-long-edge; cancel -a; cupsd.conf Listen, BrowseLocalProtocols (default _cups,_print,_universal), Browsing, Order and Allow @LOCAL, Require user @SYSTEM, ErrorPolicy retry-job; cups-files.conf SystemGroup and ErrorLog under /var/log/cups. Removed: the driverless command, the 2013 age claim, cups-browsed behaviour, Windows class-driver advice, distribution group names, SELinux and package-specific remarks, and a drv:// PPD example, none of which the manuals confirm.

Method: documentation only; no commands were run.
