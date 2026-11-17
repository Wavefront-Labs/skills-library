---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.snmp-exporter-and-generator
name: snmp-exporter-and-generator
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [snmp-exporter, snmp-exporter-generator, snmp-mibs, snmpv3, network-monitoring, if-mib]
level: advanced
status: docs-checked
description: "Monitor network gear with snmp_exporter: build snmp.yml with the generator from MIBs, SNMPv2c/v3 auths, walk/lookups/overrides, and the multi-target scrape."
sources: ["https://github.com/prometheus/snmp_exporter", "https://github.com/prometheus/snmp_exporter/tree/main/generator"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# snmp_exporter and the generator

The shipped `snmp.yml` covers common modules (for example `if_mib`, which the README recommends to start with for
switches, access points and routers using the `public_v2` auth). For anything else, generate it.

## generator.yml
```yaml
auths:
  public_v2: {version: 2, community: public}
  secure_v3:
    version: 3
    security_level: authPriv
    username: monitor
    password: ${SNMP_AUTH_PASS}          # snmp_exporter expands env vars in config with --config.expand-environment-variables
    auth_protocol: SHA
    priv_protocol: AES
    priv_password: ${SNMP_PRIV_PASS}
modules:
  if_mib:
    walk: [sysUpTime, interfaces, ifXTable]
    lookups:
      - source_indexes: [ifIndex]
        lookup: ifAlias                  # turn index into a readable label
      - source_indexes: [ifIndex]
        lookup: ifDescr
    overrides:
      ifType: {type: EnumAsInfo}
      ifAlias: {ignore: true}            # already used as a label
  apc_ups:
    walk: [upsBasicIdentModel, upsAdvBatteryCapacity, upsAdvBatteryRunTimeRemaining]
```
```bash
cd generator && make generator mibs      # builds the generator and fetches MIBs; put vendor MIBs in ./mibs
./generator generate -m ./mibs -g generator.yml -o snmp.yml   # or: make generate
```
Generator errors about objects not found in the MIBs usually mean a missing dependency MIB.

## Scrape
```yaml
- job_name: snmp-switches
  metrics_path: /snmp
  params: {module: [if_mib], auth: [secure_v3]}
  static_configs: [{targets: [sw1.example.net, sw2.example.net]}]
  relabel_configs:
    - {source_labels: [__address__], target_label: __param_target}
    - {source_labels: [__param_target], target_label: instance}
    - {target_label: __address__, replacement: snmp-exporter:9116}
  scrape_interval: 60s
  scrape_timeout: 50s
```

## Gotchas
- Big walks (full `interfaces` on a chassis with 500 ports) take seconds; raise timeout, narrow walks, or use
  `max_repetitions` tuning.
- Use 64-bit counters (`ifHCInOctets`) on fast links; 32-bit counters wrap quickly.
- `max_repetitions` (default 25) and the per-request `timeout` (default 5s) are walk settings in the generator.
- Test: `curl 'snmp-exporter:9116/snmp?target=sw1&module=if_mib&auth=secure_v3'`.

## Verify
- [ ] Scrape durations stay below the job's `scrape_timeout` for all devices.
- [ ] `rate(ifHCInOctets[5m]) * 8` matches device-reported throughput.

## Checked

2026-11-02. Confirmed against the prometheus/snmp_exporter README and generator README: `--config.expand-environment-variables` (supports username, password and priv_password in auths); `max_repetitions` default 25 and per-request `timeout` default 5s as module settings; `retries` 3; lookups with `source_indexes`/`lookup`; `EnumAsInfo` override and `ignore: true`; auth fields `version` (default 2), `security_level` (authPriv), `priv_protocol`; `/snmp?target=&module=&auth=` URL on port 9116; `./generator generate -m -g -o` form. Fixed: the build command is `make generator mibs` (not `make mibs`). Removed: the unsourced `MIBDIRS` environment variable.

Method: documentation only; no commands were run.
