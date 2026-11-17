---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-plugins-manager
name: jmeter-plugins-manager
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-plugins, plugins-manager, pluginsmanagercmd, custom-thread-groups]
level: practitioner
status: docs-checked
description: "Install and manage JMeter plugins with Plugins Manager (GUI and PluginsManagerCMD for CI), pick widely used ones, and keep plugin sets reproducible across load generators."
sources:
  - https://jmeter-plugins.org/wiki/PluginsManager/
  - https://jmeter-plugins.org/wiki/PluginsManagerAutomated/
  - https://jmeter-plugins.org/wiki/Functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter Plugins Manager

## Install
Download the Plugins Manager JAR into `lib/ext/`, restart JMeter, then open the Options menu > Plugins Manager (the item says "has upgrades" when upgrades exist). Tick plugins on the Available tab to install and untick on the Installed tab to uninstall; review the "Review Changes" pane (plugin dependencies may add changes) before Apply.

## Headless (CI, Docker, remote workers)
```bash
# prerequisites: lib/cmdrunner-2.0.jar present; bin/PluginsManagerCMD.sh created by:
java -cp lib/ext/jmeter-plugins-manager-<v>.jar org.jmeterplugins.repository.PluginManagerCMDInstaller
bin/PluginsManagerCMD.sh install jpgc-casutg,jpgc-tst,jpgc-json
bin/PluginsManagerCMD.sh install-for-jmx tests/checkout.jmx
bin/PluginsManagerCMD.sh status
```
Commands are help, status, upgrades, available, install, install-all-except, install-for-jmx and uninstall. `install-for-jmx` installs the plugins a test plan needs: run it in every generator image build.

## Commonly used plugins
| Plugin id | Provides |
|---|---|
| `jpgc-casutg` | Concurrency, Arrivals, Free-Form Arrivals and Ultimate Thread Groups |
| `jpgc-tst` | Throughput Shaping Timer |
| `jpgc-graphs-basic` | graph listeners (the manual's status example uses this id) |
| `jpgc-functions` | extra functions (`__env`, `__strReplace`, `__strReplaceRegex`) |
| `jpgc-prmctl` | Parameterized Controller |
| `jpgc-dummy` | Dummy Sampler for plan debugging |

## Reproducibility
- Pin versions with `=`: `install jpgc-fifo,jpgc-json=2.2` (the manual's syntax).
- Install the same plugins on the controller and every worker (bake them into the image).
- Commit the plugin list next to the JMX.

## Gotchas
- Keep graph listeners out of non-GUI load runs; generate graphs afterwards from the JTL.
- Check plugin compatibility before upgrading JMeter.
- Behind a proxy: `JVM_ARGS="-Dhttps.proxyHost=<host> -Dhttps.proxyPort=<port>" PluginsManagerCMD status` (add `-Dhttp.proxyUser` and `-Dhttp.proxyPass` if it needs credentials).

## Verify
`PluginsManagerCMD.sh status` lists the same plugin versions on controller and every worker.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01; latest release 5.6.3) and the JMeter Plugins wiki sources (undera/jmeter-plugins, site/dat/wiki, last commit 2026-10-23). Confirmed: install location and Options menu, dialog tabs and Review Changes pane, PluginsManagerCMD commands and bootstrap, cmdrunner prerequisite, `=version` pinning, proxy JVM_ARGS, plugin ids jpgc-casutg, jpgc-tst, jpgc-functions, jpgc-prmctl, jpgc-dummy, jpgc-graphs-basic. Removed the unconfirmed bzm-parallel and jpgc-graphs-additional ids and error-name claim.

Method: documentation only; no commands were run.
