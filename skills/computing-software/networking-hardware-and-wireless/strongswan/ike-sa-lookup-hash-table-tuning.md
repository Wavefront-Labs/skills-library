---
id: computing-software.networking-hardware-and-wireless.strongswan.ike-sa-lookup-hash-table-tuning
name: ike-sa-lookup-hash-table-tuning
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, ikesa-table-size, hash-table, scaling, ikesa-table-segments]
level: advanced
status: docs-checked
description: "Scale strongSwan gateways with thousands of IKE SAs by sizing the charon hash table with ikesa_table_size and ikesa_table_segments, with the recommended ranges."
sources:
  - https://docs.strongswan.org/docs/latest/config/lookupTuning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ike sa lookup hash table tuning
IKE SA storage is a linear list by default, which is fine for clients and small gateways. A gateway with several thousand active IKE SAs should switch to the hash table by setting its size in strongswan.conf.

```
charon {
  ikesa_table_size = 1024
  ikesa_table_segments = 16
}
```

**Table size.** Each entry holds a list of IKE SAs. The page suggests 5 to 20 IKE_SAs per entry; for 20000 simultaneous clients choose a size between 500 and 4000. Use a power of two (otherwise it is rounded up to the next one), and test if performance is critical.

**Segments (locks).** Each segment locks a slice of the table, so lookups on multiple cores collide less. The number is at least one and at most the table size, and should be a power of two. More than 512 segments has led to instabilities on some systems, and extra locks use more resources.

**Implementation note.** The lookup is optimized for responders. Initiators search for an existing IKE SA to reuse; that search is not optimized and benefits only from fewer lock conflicts. To disable IKE_SA reuse and skip that search, which should speed up IKE SA initiation, set `charon.reuse_ikesa = no`.

## Checked
2026-11-04. Confirmed against the strongSwan Tuning IKE SA Lookup page: ikesa_table_size, ikesa_table_segments, 5 to 20 SAs per entry, 500 to 4000 example, power-of-two rounding, 512 segment warning, reuse_ikesa. Nothing removed.

Method: documentation only; no commands were run.
