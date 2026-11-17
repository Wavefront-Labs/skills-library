---
id: computing-software.systems-network-administration.windows-server.performance-baselines-and-pal
name: performance-baselines-and-pal
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, performance-monitoring, pal-tool, baseline, perfmon, data-collector-sets]
level: advanced
status: gated
description: "Build a performance baseline with Data Collector Sets and analyse counter logs with PAL (Performance Analysis of Logs) thresholds to spot CPU, memory, disk and network issues."
sources:
  - https://github.com/clinthuffman/PAL
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance baselines and PAL

A baseline answers "is this slow compared to normal?". Without one, every counter value is a guess.

## Capture a baseline
Collect a representative period of normal operation (choose the sample interval to fit your question):
```cmd
logman create counter Baseline -c "\Processor(_Total)\% Processor Time" "\Memory\Available MBytes" "\Memory\Pages/sec" ^
  "\LogicalDisk(*)\Avg. Disk sec/Read" "\LogicalDisk(*)\Avg. Disk sec/Write" "\LogicalDisk(*)\Disk Transfers/sec" ^
  "\Network Interface(*)\Bytes Total/sec" "\System\Processor Queue Length" -si 30 -f bincirc -max 1024 -o "<LOGS>\Baseline"
logman start Baseline
```
Keep baselines per server role and after major changes. PAL's threshold files can also tell you which counters a product
analysis needs.

## Analyse with PAL
PAL (open source) reads a performance monitor counter log and analyses it against known thresholds. Its project page
lists threshold files for major Microsoft products (for example IIS, SQL Server, Exchange, Active Directory) and an HTML
report.
```powershell
.\PAL.ps1 -Log '<LOGS>\Baseline_000001.blg' -ThresholdFile '.\SystemOverview.xml' -Interval 'AUTO' `
  -NumberOfProcessors 8 -TotalMemory 32 -IsOutputHtml $True -HtmlOutputFileName '[LogFileName]_PAL.htm'
```
Answer the threshold file's questions accurately; thresholds depend on them (see the project page for the exact parameters).

## Reading the report
- Alerts are hints, not verdicts: check whether they happen at peak and compare with the baseline report.
- Judge latency, memory and CPU counters against your own baseline and the vendor's guidance for the workload; Microsoft's
  performance tuning pages are the starting reference.

## Verify
- [ ] Baseline report stored per server; a later incident report compared against it identifies the changed resource.

## Checked
2026-10-28. Confirmed on the PAL project page and Learn performance tuning index: PAL analyses performance counter logs against threshold
files for IIS, SQL Server, Exchange and AD and creates an HTML report. Removed as unconfirmed: .blg specifics, "export to
Perfmon template", Hyper-V threshold file, PAL.ps1 parameter list, fixed latency/memory/queue thresholds and the 15-60 s
sample guidance. The `logman` counter-capture command is standard Windows tooling not checked on a fetched page
(gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
