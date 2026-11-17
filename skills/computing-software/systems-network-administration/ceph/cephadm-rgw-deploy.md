---
id: computing-software.systems-network-administration.ceph.cephadm-rgw-deploy
name: cephadm-rgw-deploy
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, rgw, radosgw, orch-apply, multisite]
level: practitioner
status: docs-checked
description: "Deploy RGW daemons with cephadm using ceph orch apply rgw, placement labels, realms and zones, and HTTPS certificates."
sources:
  - https://docs.ceph.com/en/latest/cephadm/services/rgw/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Simplest deployment:

```
ceph orch apply rgw foo
```

Dedicated gateway hosts via a label, two daemons per host on port 8000:

```
ceph orch host label add gwhost1 rgw
ceph orch host label add gwhost2 rgw
ceph orch apply rgw foo --placement='label:rgw count-per-host:2' --port=8000
```

General form:

```
ceph orch apply rgw <name> [--realm=<realm-name>] [--zone=<zone-name>] --placement="<num-daemons> [<host1> ...]"
```

Multisite objects can be created with `radosgw-admin`:

```
radosgw-admin realm create --rgw-realm=<realm-name>
radosgw-admin zonegroup create --rgw-zonegroup=<zonegroup-name> --master
radosgw-admin zone create --rgw-zonegroup=<zonegroup-name> --rgw-zone=<zone-name> --master
radosgw-admin period update --rgw-realm=<realm-name> --commit
```

HTTPS certificates go through the certificate manager:

```
ceph orch certmgr cert set rgw_ssl_cert --service-name rgw.<service_id> -i $PWD/server_cert.pem
ceph orch certmgr key set rgw_ssl_key --service-name rgw.<service_id> -i $PWD/server_key.pem
```

For high availability, an ingress spec applied with `ceph orch apply -i <ingress_spec_file>` fronts the daemons.

Networks and ports can be set in a service spec: `service_type: rgw`, `service_id: foo`, a `placement` with `label: rgw` and `count_per_host: 2`, `networks: [192.168.142.0/24]`, and `spec: rgw_frontend_port: 8080`. Extra frontend arguments go in `rgw_frontend_extra_args`; cephadm merges them with the spec values into one space-separated `rgw_frontends` setting, and `rgw_frontend_type` can be `beast`. With SSL enabled, `rgw_frontend_http_port` adds a plain HTTP port next to HTTPS; it must differ from `rgw_frontend_port`, needs `ssl: true`, and specs that set it without SSL are rejected by validation.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm RGW Service page (docs.ceph.com/en/latest/cephadm/services/rgw/): apply rgw forms, label placement, multisite objects, certificate manager commands, service spec keys, frontend arguments and the HTTP port rules.

Removed: nothing; every command and key was found on the page.

Method: documentation only; no commands were run.

