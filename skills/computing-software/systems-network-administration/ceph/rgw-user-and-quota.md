---
id: computing-software.systems-network-administration.ceph.rgw-user-and-quota
name: rgw-user-and-quota
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rgw, radosgw-admin, user, quota, bucket]
level: practitioner
status: docs-checked
description: "Create RGW users and subusers, suspend or enable them, and set object-count and size quotas with radosgw-admin."
sources:
  - https://docs.ceph.com/en/latest/radosgw/admin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Users:

```
radosgw-admin user create --uid=johndoe --display-name="John Doe" --email=john@example.com
radosgw-admin subuser create --uid=johndoe --subuser=johndoe:swift --access=full
radosgw-admin user info --uid=johndoe
radosgw-admin user suspend --uid=johndoe
radosgw-admin user enable --uid=johndoe
```

Subuser `--access` is one of `read`, `write`, `readwrite` or `full`. Bucket access can also be suspended with `radosgw-admin bucket suspend --bucket=mybucket` and `unsuspend`.

Quotas have a scope (`user` or `bucket`), `--max-objects` and `--max-size`:

```
radosgw-admin quota set --quota-scope=user --uid=johndoe --max-objects=1024 --max-size=1024B
radosgw-admin quota enable --quota-scope=user --uid=johndoe
radosgw-admin quota disable --quota-scope=user --uid=johndoe
```

A negative value for `--max-objects` or `--max-size` means no limit. A quota set but not enabled does nothing, so run `quota enable` after `quota set`.

Users and keys: `radosgw-admin user rm --uid=johndoe` removes a user with its subusers, and `--purge-data` also purges all data for the UID while `--purge-keys` purges keys. Create specific S3 credentials with `radosgw-admin key create --uid=foo --key-type=s3 --access-key fooAccessKey --secret-key fooSecretKey`, or `--gen-access-key` and `--gen-secret` to generate them. A subuser can have only one Swift secret key. Generated keys sometimes contain a JSON escape backslash that some clients cannot handle; regenerate or set the key manually. User quotas sum across all buckets the user owns. Bucket quotas take `--bucket=<name>` for one bucket or `--uid` for all of a user's buckets. Quota stats update asynchronously (`radosgw-admin user stats --uid=<uid> --sync-stats` forces it) and each RGW instance caches them, so multiple gateways may not enforce perfectly.

## Checked

2026-11-09. Confirmed against the Ceph docs page Admin Guide (radosgw/admin): user and subuser create, suspend and enable, bucket suspend, subuser access levels, user rm and purge options, key create options, single Swift secret key, JSON escape character note, quota set/enable semantics, negative values disabling a limit, user quotas summed across buckets, --sync-stats and per-instance quota caching.

Method: documentation only; no commands were run.
