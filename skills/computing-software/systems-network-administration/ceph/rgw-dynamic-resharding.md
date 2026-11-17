---
id: computing-software.systems-network-administration.ceph.rgw-dynamic-resharding
name: rgw-dynamic-resharding
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rgw, bucket-index, reshard, radosgw-admin, shards]
level: advanced
status: docs-checked
description: "Reshard RGW bucket indexes: queue, process and cancel resharding and clean up stale instances."
sources:
  - https://docs.ceph.com/en/latest/radosgw/dynamicresharding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RGW reshards a bucket index automatically when a shard holds too many entries. Writes to the bucket can be blocked briefly during resharding; reads are not. Detection runs as a background scan that periodically checks all buckets and queues those needing resharding; a background thread processes queued tasks one at a time.

Options (defaults from the page): `rgw_dynamic_resharding` (true, not runtime updatable), `rgw_max_objs_per_shard` (100000), `rgw_max_dynamic_shards` (1999, the most shards dynamic resharding creates on its own; it does not limit user-requested resharding; ideally prime), `rgw_dynamic_resharding_may_reduce` (true), `rgw_dynamic_resharding_reduction_wait` (120 seconds; too low a value can significantly reduce cluster performance) and `rgw_reshard_thread_interval` (600 seconds between processing reshard log entries).

Manual control:

```
radosgw-admin reshard add --bucket <bucket_name> --num-shards <new number of shards>
radosgw-admin reshard list
radosgw-admin reshard process
radosgw-admin reshard status --bucket <bucket_name>
radosgw-admin reshard cancel --bucket <bucket_name>
```

`reshard status` prints a JSON array with `reshard_status` (`not-resharding` or `in-progress`), `new_bucket_instance_id` and `num_shards` per shard. A reshard cannot be canceled once it has moved from `not-resharding` to `in-progress`.

Reshard immediately instead of queueing:

```
radosgw-admin bucket reshard --bucket <bucket_name> --num-shards <new number of shards>
```

Anticipate each bucket's peak object count and aim for no more than 100000 entries per shard at any time. Prime shard counts distribute entries more evenly: 7001 is better than 7000.

Set a floor on shard count, since dynamic resharding can now reduce shards (from Tentacle, after a delay that avoids thrashing):

```
radosgw-admin bucket set-min-shards --bucket <bucket_name> --num-shards <min number of shards>
```

This does not prevent a manual reshard to a lower number.

Stale bucket instances left by clusters older than Luminous 12.2.11 and Mimic 13.2.5 can be listed and removed:

```
radosgw-admin reshard stale-instances list
radosgw-admin reshard stale-instances delete
```

Do not clean up stale instances in a multisite deployment. Before Reef, RGW does not support dynamic resharding in a multisite deployment; see the multisite resharding documentation.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "RGW Dynamic Bucket Index Resharding" on docs.ceph.com, including the configuration option table and admin commands. Added the cancel limitation and pre-Reef multisite statement; replaced the vague multisite pointer.
