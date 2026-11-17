---
id: computing-software.systems-network-administration.active-directory.automated-ad-health-report
name: automated-ad-health-report
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-health, ad-health-report, dcdiag, repadmin]
level: practitioner
status: docs-checked
description: "Build a daily automated AD health report: dcdiag, repadmin replsummary, FSMO reachability, SYSVOL backlog, time offset and backup age, emailed or posted."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dcdiag
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc835092(v=ws.11)
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/send-mailmessage
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-service
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Automated daily AD health report

## What to check every day
| Check | Command | Fail when |
|---|---|---|
| DC tests | `dcdiag /e /q` | any output (quiet mode prints only failures) |
| Replication | `repadmin /replsummary /errorsonly` | any row listed (non-zero partner error); also review the largest delta |
| Queue | `repadmin /queue *` | items piling up |
| FSMO holders reachable | `netdom query fsmo` + `Test-Connection` | holder down |
| SYSVOL | DFSR backlog between hub and each DC | backlog > 100 for hours |
| Time | `w32tm /monitor` | offset from the PDC emulator beyond your tolerance (Kerberos allows 5 minutes) |
| Backups | your backup product's last-success report | no good backup in 24 h |
| Services | NTDS, DNS, Netlogon, KDC, DFSR, W32Time on each DC | not Running |
| Disk | NTDS and SYSVOL volumes free space | < 20% |

## Skeleton script (Windows PowerShell 5.1; run as a gMSA with read rights on DCs)
PowerShell 7's `Get-Service` has no `-ComputerName` parameter; use `Invoke-Command` with remoting there.
```powershell
$dcs = (Get-ADDomainController -Filter *).HostName
$report = foreach ($dc in $dcs) {
  $svc = Get-Service NTDS,DNS,Netlogon,Kdc,DFSR,W32Time -ComputerName $dc -ErrorAction SilentlyContinue | Where-Object Status -ne Running
  $dcd = dcdiag /s:$dc /q 2>&1
  [pscustomobject]@{DC=$dc; StoppedServices=($svc.Name -join ','); DcdiagFailures=($dcd | Out-String).Trim()}
}
$repl = repadmin /replsummary 2>&1 | Out-String
$bad  = $report | Where-Object { $_.StoppedServices -or $_.DcdiagFailures }
$html = ($report | ConvertTo-Html -Fragment | Out-String) + "<pre>$repl</pre>"
$subject = if ($bad) { "AD health: $(@($bad).Count) DC(s) need attention" } else { 'AD health: OK' }
Send-MailMessage -SmtpServer smtp.corp.example.com -From adhealth@example.com -To ad-team@example.com -Subject $subject -Body $html -BodyAsHtml
```
`Send-MailMessage` is documented as obsolete because it does not guarantee secure connections; prefer another
mail path or post to a Teams/Slack webhook with `Invoke-RestMethod`.

## Run it
Scheduled task daily at 06:00 under a gMSA. Store output history (CSV) to spot trends.

## Verify
- [ ] Report arrives daily; a test failure (stop DFSR on a lab DC) shows up as red.

## Checked
2026-10-27, against the dcdiag page on Learn (windowsserverdocs, /q prints only errors; /e all servers), the repadmin /replsummary and /queue pages (Learn previous-versions, Windows Server 2012 R2), the netdom query page, the Send-MailMessage and Get-Service pages (PowerShell 7.5) and the replication troubleshooting article (Kerberos 5-minute time accuracy; w32tm /monitor). Confirmed: dcdiag /e /q behaviour, replsummary /errorsonly, `netdom query fsmo`, w32tm /monitor, Send-MailMessage obsolete warning, Get-Service -ComputerName absent in PowerShell 7. Removed as unconfirmed: repadmin /showbackup and the /monitor /domain: form. Thresholds in the table are suggested operating limits, not documented values.

Method: documentation only; no commands were run.
