---
id: computing-software.search-and-information-retrieval.apache-solr.production-service-install
name: production-service-install
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [production-install, install-solr-service, solr-in-sh, solr-home, systemd-service]
level: practitioner
status: docs-checked
description: "Install Solr as a Linux service with install_solr_service.sh: -i, -d, -u, -s, -p, -n options, /opt/solr and /var/solr layout, solr.in.sh in /etc/default, SOLR_HOME."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# production-service-install

Extract the script from the release archive, then run it: `tar xzf solr-10.1.0.tgz solr-10.1.0/bin/install_solr_service.sh --strip-components=2` and `sudo bash ./install_solr_service.sh solr-10.1.0.tgz`.

Defaults: archive extracted into `/opt`, writable files in `/var/solr`, run as user `solr`, port 8983, service name `solr`. This keeps `/opt/solr` untouched and puts all changing files under `/var/solr`.

Options: `-i` install directory, `-d` data and var directory, `-u` user, `-s` service name, `-p` port, `-n` do not start immediately. Full form: `sudo bash ./install_solr_service.sh solr-10.1.0.tgz -i /opt -d /var/solr -u solr -s solr -p 8983`. See `--help`.

Check with `sudo service solr status`.

Settings live in an include file: `/etc/default/solr.in.sh` (for service `solr-demo` it is `solr-demo.in.sh`). It must at least define `SOLR_PID_DIR` and `SOLR_HOME`, for example `/var/solr` and `/var/solr/data`. SSL variables go in `/var/solr/solr.in.sh`, per the SSL page.

## Checked

2026-11-04. Confirmed against Taking Solr to Production: script defaults, `-i -d -u -s -p -n` options, `/opt/solr` and `/var/solr` layout, `sudo service solr status`, `SOLR_PID_DIR` and `SOLR_HOME`. Removed an unsourced remark about the data subdirectory.

Method: documentation only; no commands were run.
