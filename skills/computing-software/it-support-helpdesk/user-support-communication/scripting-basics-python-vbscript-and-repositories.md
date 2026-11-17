---
id: computing-software.it-support-helpdesk.user-support-communication.scripting-basics-python-vbscript-and-repositories
name: scripting-basics-python-vbscript-and-repositories
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, python-scripting, vbscript, script-constructs, script-repository, version-control, support-scripting]
level: practitioner
status: draft
description: "Scripting basics for support: variables, loops and conditionals, Python for support tasks, reading legacy VBScript, and keeping scripts in a version-controlled repository."
sources:
  - "https://docs.python.org/3/tutorial/"
  - "https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/hh875526(v=vs.85)"
  - "https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# scripting-basics-python-vbscript-and-repositories

## Core constructs (any language)
| Construct | PowerShell | Python | Bash |
|---|---|---|---|
| Variable | `$name = "PC01"` | `name = "PC01"` | `name="PC01"` |
| Condition | `if ($x -gt 5) { } else { }` | `if x > 5:` | `if [ "$x" -gt 5 ]; then ... fi` |
| Loop | `foreach ($pc in $list) { }` | `for pc in pcs:` | `for pc in $list; do ... done` |
| Comment | `# text` | `# text` | `# text` |
| Function | `function Get-X { }` | `def get_x():` | `get_x() { }` |
Always comment the why, not the what; put a header with purpose, author, date, usage.

## Python for support tasks
Useful where cross-platform or text/data processing matters:
```python
# Report free disk space on the local machine (any OS)
import shutil, socket
total, used, free = shutil.disk_usage("/")
print(f"{socket.gethostname()}: {free // 2**30} GB free of {total // 2**30} GB")
```
```python
# Find users in a CSV export who haven't signed in for 90 days
import csv, datetime
cutoff = datetime.datetime.now() - datetime.timedelta(days=90)
with open("signins.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if datetime.datetime.fromisoformat(row["LastSignIn"]) < cutoff:
            print(row["UserPrincipalName"])
```
- Use virtual environments (`python -m venv .venv`) and `requests` for APIs (ITSM, Graph).
- Python isn't installed on Windows by default; don't depend on it on endpoints unless
  deployed; prefer PowerShell there.

## Legacy VBScript and JScript
- Still found in old logon scripts and HTAs. VBScript is deprecated: a Windows feature
  on demand that Microsoft is removing in phases; plan migration to PowerShell.
- Reading it: `Set objNetwork = CreateObject("WScript.Network")`
  `objNetwork.MapNetworkDrive "H:", "\\server\home\" & strUser` maps a drive; run with
  `cscript //nologo script.vbs`.
- Common logon script jobs and modern replacements: drive maps (GPP drive maps or
  Intune), printers (Universal Print / GPP), registry (GPP/Intune).

## Script repository
- One Git repository for support scripts (Azure DevOps, GitHub, GitLab), not a share
  of `final_v2_fixed.ps1` files.
- Structure: folders by purpose, README per script with usage and risk; pull requests
  with peer review before production use; tag releases deployed via RMM/Intune.
- No secrets in scripts or history: use the vault, managed identities or parameters.
  Scan with secret scanning.
- Record who ran what where (RMM/Intune logs) and link scripts to change records for
  bulk actions.

## Verify
Scripts in use exist in the repository with a review history, have headers and comments,
and no credentials appear in code or commits.
