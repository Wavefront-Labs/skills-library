---
id: computing-software.systems-network-administration.nagios-core.large-installation-tweaks
name: large-installation-tweaks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, use-large-installation-tweaks, large-installation, summary-macros, hostgroupmembers, free-child-process-memory, scaling]
level: advanced
status: docs-checked
description: "What use_large_installation_tweaks changes in Nagios Core (no summary or group-member environment macros, children skip freeing memory) and the trade-offs."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/largeinstalltweaks.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large installation tweaks

Set `use_large_installation_tweaks` in `nagios.cfg`. It makes the daemon skip load-adding work:

1. **Summary macros** (`$TOTALHOSTSUP$` etc.) are not set as environment variables; computing them is slow on big configs.
2. **`$HOSTGROUPMEMBERS$` and `$SERVICEGROUPMEMBERS$`** are not set as environment variables (could exhaust environment space).
3. **Child processes don't free allocated memory before exit**; the OS reclaims it faster.

## Trade-off
Scripts that read those values from the environment will not find them; pass them as command-line arguments instead (`$TOTALHOSTSDOWN$` in the command line still works).

Related main-config option: `free_child_process_memory` (default 1 unless large-install tweaks are on).

Also consider `enable_environment_macros=0` (`computing-software.systems-network-administration.nagios-core.macro-sanitization-environment`) and the wider checklist `computing-software.systems-network-administration.nagios-core.performance-tuning-tips`.

## Checked

2026-11-04. Confirmed against the Large Installation Tweaks page (summary macros, HOSTGROUPMEMBERS and SERVICEGROUPMEMBERS not in the environment, no memory freeing in child processes) and the main configuration page (use_large_installation_tweaks default 0, free_child_process_memory frees by default but not when the tweaks are enabled).

Method: documentation only; no commands were run.
