---
id: computing-software.systems-network-administration.linux.validate-cloud-init-user-data-schema
name: validate-cloud-init-user-data-schema
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cloud-init-schema, cloud-init, user-data, cloud-config, cloud-init-devel, cloud-init-analyze]
level: practitioner
status: docs-checked
description: "Validate cloud-init user-data before boot and debug it after: cloud-init schema checks, common YAML mistakes, running modules locally, and reading cloud-init status and logs."
sources:
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/reference/cli.rst
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/howto/rerun_cloud_init.rst
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/reference/config-format-headers.rst
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/explanation/instancedata.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Validate user-data with cloud-init schema

A malformed user-data file usually doesn't fail loudly: cloud-init skips the bad module and the instance boots half-configured.

## Validate before launching
```bash
cloud-init schema --config-file user-data.yaml --annotate    # annotates the file with errors on stdout
cloud-init schema -c user-data.yaml                          # same check without annotation
cloud-init schema -c network-config.yaml -t network-config   # -t selects the schema type (default cloud-config)
```
Run it in CI for every template on any machine with cloud-init installed.

Common errors it catches:
- First line not exactly `#cloud-config` (then it's treated as a script or ignored).
- `users:` entries missing `name`, or `ssh_authorized_keys` as a string instead of a list.
- Tabs or bad indentation; `runcmd` items that are YAML maps because of an unquoted `: `.
- Keys or values that do not match the jsonschema for the module (`cloud-init schema --docs all` prints the module docs).

## Check on a running instance
```bash
cloud-init status --long --wait          # running / done / disabled / error, plus errors and recoverable_errors; exit 1 crash, 2 recoverable errors
cloud-init schema --system --annotate    # validates the user-data the instance actually received
cloud-init query userdata | head         # raw user-data (root only)
cloud-init analyze show                  # per-stage, per-module timing
cloud-init analyze blame | head          # slowest modules
```
Logs: `/var/log/cloud-init.log` (detailed), `/var/log/cloud-init-output.log` (stdout of runcmd/scripts). `grep -iE 'warn|error|traceback' /var/log/cloud-init.log`.

## Rerun after fixing
```bash
cloud-init clean --logs --reboot           # instance re-runs everything as first boot
cloud-init single --name runcmd --frequency always   # one module (frequency: always|instance|once; not every module is idempotent)
cloud-init modules --mode config           # rerun the config stage
```

## Multi-part and Jinja
- Multi-part MIME (mixing `#cloud-config` and shell scripts): build with `cloud-init devel make-mime -a config.yaml:cloud-config -a script.sh:x-shellscript > user-data`.
- `## template: jinja` first line enables `{{ v1.local_hostname }}` and `ds.meta_data`; render-test with `cloud-init devel render user-data`.

## Size and secrets
- Cloud providers cap user-data size (check the provider's documentation for the limit); `write_files` accepts `encoding: gz+b64` for compressed content.
- Sensitive data such as passwords can appear in instance-data; cloud-init makes it readable only by root, but still avoid long-lived secrets in user-data.

## Verify
- [ ] `cloud-init schema` exits 0 in CI.
- [ ] On first boot `cloud-init status --long` reports `status: done` with no recoverable errors.

## Checked

Checked 2026-10-26 against canonical/cloud-init main (last commit 2026-10-23): doc/rtd cli, rerun_cloud_init, config-format-headers and instancedata pages, cloudinit/cmd/main.py and cloudinit/cmd/devel (make_mime, render). Confirmed: schema options (-c, -t, --system, --docs, --annotate), status output values and exit codes, clean --logs --reboot, single --name/--frequency, modules --mode, make-mime -a file:type and render subcommands, the ## template: jinja header, v1.local_hostname, root-only sensitive instance-data. Removed: the unconfirmed 22.2 version gate, the apt_sources deprecation claim, the AWS 16 KB limit and the IMDSv2 hop-limit claim (AWS documentation is not in a public repository).

Method: documentation only; no commands were run.
