---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-distributed-testing
name: jmeter-distributed-testing
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, remote-testing, jmeter-distributed, jmeter-server, distributed-load-testing, rmi, jmeter-reporting]
level: practitioner
status: docs-checked
description: "Run JMeter distributed: controller and remote servers, RMI ports and SSL keystore, -R/-r options, data file distribution, and when to run independent instances instead."
sources:
  - https://jmeter.apache.org/usermanual/remote-test.html
  - https://jmeter.apache.org/usermanual/get-started.html#override
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter distributed (controller/worker) testing

**Goal:** generate load from several machines and collect results centrally.

## Setup
1. Same JMeter version on all machines (the manual also asks for the same Java version; mixing may work but is discouraged). Keep plugins identical too.
2. RMI SSL keystore: run `bin/create-rmi-keystore.sh` (`.bat` on Windows) once and copy the generated `rmi_keystore.jks` to the `bin` folder of every server and client (or set `server.rmi.ssl.disable=true` on trusted networks only).
3. On each worker: RMI uses a dynamic port by default, so fix ports for firewalls in `user.properties`:
   ```
   server.rmi.localport=50000
   server_port=1099
   ```
   then start `jmeter-server` (add `-Djava.rmi.server.hostname=<worker-ip>` if the machine has several addresses).
4. Controller: `client.rmi.localport=60000` (up to three ports from this one are used) and `remote_hosts=10.0.0.11,10.0.0.12` in jmeter.properties.

## Run
```bash
jmeter -n -t plan.jmx -R 10.0.0.11,10.0.0.12 -Gthreads=100 -l results.jtl -e -o report/
jmeter -n -t plan.jmx -r     # all remote_hosts
```
JMeter does not divide load between servers: each runs the full plan (100 threads x 2 workers = 200 users). Data files are not sent by the client, so they must exist in the appropriate directory on each server; split the data between them if each server needs unique ids. `-G` defines a property on all servers; `-X` exits the servers at the end.

## Results traffic
The `mode` property (set on the client) defaults to `StrippedBatch`, which removes response data from successful samples and sends them in batches; the manual warns that the client or its network can still be overloaded with many servers. Alternative: run independent non-GUI instances on each machine (`jmeter -n ... -l results-<host>.jtl`), then merge JTL files and generate one dashboard (`jmeter -g merged.jtl -o report/`; `-g` generates the dashboard from a CSV file only).

## Gotchas
- A wrong or loopback host name in `java.rmi.server.hostname` or `/etc/hosts` causes "connection refused"; the manual describes removing loopback entries and passing the option.
- Because each server runs the full plan, a Constant Throughput Timer target applies per server, not globally; divide the target by the server count.

## Verify
Active threads in the report equal threads x workers, and each worker's CPU stays within limits.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: full plan runs on each server, data files not sent, `-R`/`-r`/`-G`/`-X`, `remote_hosts`, `server_port`, `server.rmi.localport`, `client.rmi.localport`, `server.rmi.ssl.disable`, create-rmi-keystore script, `mode` default StrippedBatch, `-g` dashboard-only option, Constant Throughput Timer options.

Method: documentation only; no commands were run.
