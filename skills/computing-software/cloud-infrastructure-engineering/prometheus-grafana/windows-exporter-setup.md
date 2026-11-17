---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.windows-exporter-setup
name: windows-exporter-setup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, windows-exporter-setup, wmi, windows-server, iis, mssql, perfcounters]
level: practitioner
status: verified
description: "Install and configure windows_exporter on Windows hosts: MSI flags, enabled collectors, service/process filters, perf counters, textfile, firewall and key queries."
sources: ["https://github.com/prometheus-community/windows_exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows_exporter

## Install
```powershell
msiexec /i windows_exporter-<ver>-amd64.msi --% ENABLED_COLLECTORS=cpu,logical_disk,memory,net,os,service,system,textfile,process LISTEN_PORT=9182 ADDLOCAL=FirewallException
```
(`--%` is the form the project README uses from PowerShell. Add `iis` only on hosts with IIS: on a host without it the exporter logged
`couldn't initialize collector ... iis`. The old `cs` collector no longer exists: `windows_exporter.exe --collectors.enabled=cs`
fails with `unknown collector cs` in 0.31.9; physical memory is in `memory`.)
Or a config file: `windows_exporter.exe --config.file=config.yml`:
```yaml
collectors:
  enabled: cpu,logical_disk,memory,net,os,service,system,process,textfile
collector:
  service:
    include: "(MSSQLSERVER|W3SVC|WinRM)"       # regex over service names; default ".+"
  process:
    include: "(sqlservr|w3wp|java)"
  textfile:
    directories: ['<INSTALL_DIR>\textfile_inputs']    # a list; default is the textfile_inputs folder next to the exe
```

## Useful queries
```promql
100 - avg by (instance) (rate(windows_cpu_time_total{mode="idle"}[5m])) * 100
windows_logical_disk_free_bytes{volume!~"HarddiskVolume.*"} / windows_logical_disk_size_bytes < 0.1
windows_service_state{name="WinRM", state="running"} == 0         # name keeps the service's own capitalisation
windows_memory_physical_free_bytes / windows_memory_physical_total_bytes < 0.1
```

## Gotchas
- `process` collector without an include filter produces series for every process (9,306 `windows_process_*` series for 130 process names on a test desktop).
- The `service` collector emits seven `windows_service_state` series per service it matches; filter it with `include`.
- Scrape timeouts: `windows_exporter_collector_duration_seconds` per collector shows the slow one.

## Verify
- [ ] `curl http://host:9182/metrics | findstr windows_exporter_collector_success` all 1.
- [ ] Scrape duration < 5 s; firewall rule allows only the Prometheus source range.

## Checked
Environment: Windows 11, windows_exporter 0.31.9 (windows-amd64 binary), Prometheus 3.15.1.
- The skill's YAML (minus `cs`) loaded with `--config.file`; `directories` as a plain string failed with `cannot unmarshal !!str ... into []string`, as a list it worked; `cs` failed with `unknown collector cs`. With the config, `windows_exporter_collector_success{collector=...}` was 1 for all nine collectors, `windows_exporter_collector_duration_seconds` per collector existed, textfile metrics from a `.prom` file in the directory were served, and the `service` collector with `include: "(WinRM|W32Time|Dnscache)"` returned `windows_service_state` with `name="WinRM"` etc. and states `continue pending`, `pause pending`, `paused`, `running`, `start pending`, `stop pending`, `stopped`.
- Prometheus 3.15.1 scraping that exporter evaluated the four skill queries (with the memory and service fixes): CPU query 95.9, disk query per `C:`/`D:` volume, service query returned `WinRM running 0`, memory ratio 0.26. `windows_cpu_time_total` has labels `core` and `mode`.
- Unfiltered `process` collector: 9,306 `windows_process_*` series for 130 process names.
- MSI properties `ENABLED_COLLECTORS`, `LISTEN_PORT`, `ADDLOCAL=FirewallException` and the `--%` usage: windows_exporter README. The MSI was not installed (no system changes); the `msiexec` line is as documented there. `iis` on a host without IIS: warning seen, other collectors kept working.
