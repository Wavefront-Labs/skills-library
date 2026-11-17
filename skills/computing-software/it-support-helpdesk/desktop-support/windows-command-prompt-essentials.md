---
id: computing-software.it-support-helpdesk.desktop-support.windows-command-prompt-essentials
name: windows-command-prompt-essentials
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, netstat, taskkill, tasklist, cmd, windows-commands]
level: practitioner
status: docs-checked
description: "Use classic Windows commands for quick support tasks: netstat to find connections and owning PIDs, taskkill to end processes, with the verified flags and cautions."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/taskkill"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-command-prompt-essentials

Classic command-shell tools for quick support tasks. The Windows commands A-Z
page lists the full set (for example `tasklist`, `shutdown`, `whoami`,
`hostname`, `ver`, `xcopy`, `robocopy`, `rmdir`, `format`, `diskpart`);
open each command's own page before relying on a flag. This skill covers the
two commands whose pages were checked.

## netstat
Displays active TCP connections, listening ports, Ethernet statistics, the IP
routing table and per-protocol statistics. It is only available when TCP/IP is
installed on a network adapter.

```
netstat [-a] [-b] [-e] [-n] [-o] [-p <Protocol>] [-q] [-r] [-s] [<interval>]
```
- `-a` all active TCP connections plus listening TCP and UDP ports.
- `-n` numeric addresses and ports, no name lookups.
- `-o` adds the owning process ID; combine with `-a`, `-n`, `-p`. Find the
  application from the PID on the Processes tab of Task Manager (or with
  `tasklist`).
- `-b` the executable behind each connection or port. Can be slow and fails
  without sufficient permissions.
- `-e` Ethernet statistics (bytes and packets sent and received); combine with
  `-s`.
- `-r` the IP routing table, equivalent to `route print`.
- `-s` statistics by protocol; `-p tcp|udp|tcpv6|udpv6` restricts the
  connection list (with `-s` also icmp, ip, icmpv6, ipv6).
- `-q` all connections, listening ports and bound non-listening TCP ports.
- `<interval>` repeats every N seconds until Ctrl+C.
- Examples from the page: `netstat -n -o`, `netstat -o 5`, `netstat -e -s`,
  `netstat -s -p tcp udp`, `netstat -anobq`.
- The page's State column lists CLOSE_WAIT, CLOSED, ESTABLISHED, FIN_WAIT_1,
  FIN_WAIT_2, LAST_ACK, LISTEN, SYN_RECEIVED, SYN_SEND and TIMED_WAIT.

## taskkill
Ends processes by PID or image name; use `tasklist` to find the PID.
```
taskkill [/s <computer> [/u [<domain>\]<username> [/p [<password>]]]] {[/fi <filter>] [...] [/pid <processID> | /im <imagename>]} [/f] [/t]
```
- `/pid <id>` or `/im <imagename>` selects the target; repeat `/pid` for
  several.
- `/f` forces termination; `/t` also ends child processes.
- `/s <computer>` targets a remote machine (no backslashes). A remote process
  is always ended forcefully whether or not `/f` is given. `/u` works only
  with `/s`. The WINDOWTITLE and STATUS filters are not supported remotely.
- `/fi` filters: STATUS, IMAGENAME, PID, SESSION, CPUTime, MEMUSAGE, USERNAME,
  SERVICES, WINDOWTITLE, MODULES, each with listed operators (eq, ne, and gt,
  lt, ge, le for numeric ones).
- The `*` wildcard is accepted for `/im` only when a filter is applied.
- Page examples: `taskkill /pid 2134 /t /fi "username eq administrator"`,
  `taskkill /f /fi "PID ge 1000" /im *`. The last one ends every matching
  process, so never run such a wildcard on a user's machine.
- `/p` supplies the password for `/u`; the page's own example shows a
  password in clear text on the command line, so avoid copying that.

## Verify
The target process or connection is the intended one (check PID and image
name first) before you force-kill anything.

## Checked

Date 2026-11-08. Pages read in full: netstat, taskkill; the Windows commands A-Z page was read for which commands exist. Confirmed: all netstat and taskkill flags, filters and remote behaviour above, and the command names in the opening paragraph. Removed as not covered by the cited pages: whoami and shutdown examples, the High Mandatory Level SID check, xcopy flag meanings, format filesystem advice, the 4 GB FAT32 limit, "polite close" wording for taskkill without /f, and netstat state names as printed by older tools (the page spells them differently).

Method: docs-only read of cited pages, 2026-11-08
