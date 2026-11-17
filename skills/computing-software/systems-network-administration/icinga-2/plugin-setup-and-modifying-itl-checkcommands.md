---
id: computing-software.systems-network-administration.icinga-2.plugin-setup-and-modifying-itl-checkcommands
name: plugin-setup-and-modifying-itl-checkcommands
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, plugins, plugindir, custom-plugin-dir, dependency-errors, itl, import-checkcommand]
level: practitioner
status: docs-checked
description: Install and verify plugins for Icinga 2 - PluginDir, testing as the icinga user, missing dependencies, a custom plugin directory constant, and extending an ITL CheckCommand.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plugin setup and modifying ITL CheckCommands
All Icinga or Nagios plugins work with Icinga 2; community plugins are on Icinga Exchange. Recommended: copy them into `PluginDir`. For plugins with many dependencies consider a custom RPM/DEB package, or use Puppet, Ansible, Chef or Saltstack to install plugins and their libraries.

**Verify** by running the plugin as the Icinga user, for example `sudo -u icinga /usr/lib64/nagios/plugins/check_mysql_health --help` on RHEL/Fedora, or `sudo -u nagios /usr/lib/nagios/plugins/...` on Debian/Ubuntu. Do not test on the master; test on the satellites and clients that execute the checks. Hard-coded paths inside a plugin are easier fixed with a symbolic link than by editing the plugin.

**Dependency errors** are typically missing libraries or binaries, such as a Python `ImportError` for a module or Perl's `Can't locate Net/SNMP.pm`. Prefer a distribution package (`libnet-snmp-perl` on Debian/Ubuntu, `perl-Net-SNMP` on RHEL) before CPAN.

**Custom path:** create a directory, copy the plugin and `chmod +x`, then add a constant in constants.conf, e.g. `const CustomPluginDir = "/opt/monitoring/plugins"`, and reference it in your CheckCommand objects.

**Definitions:** every plugin needs a CheckCommand. First check whether the ITL already provides one, and run the plugin on the CLI with the needed parameters.

**Modify an ITL command** by importing it rather than copying:
```
object CheckCommand "http-custom" {
  import "http"
  arguments += {
    "--key" = { value = "$http_..." }
  }
  vars.http_address = "..."
}
```
Use `+=` to add arguments and set `vars` to override defaults.

## Checked

2026-11-04. Confirmed against the Icinga 2 service monitoring chapter: plugin installation advice, running as the Icinga user, dependency errors, CustomPluginDir constant and importing ITL commands.

Method: documentation only; no commands were run.
