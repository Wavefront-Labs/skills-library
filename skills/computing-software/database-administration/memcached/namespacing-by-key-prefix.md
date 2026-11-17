---
id: computing-software.database-administration.memcached.namespacing-by-key-prefix
name: namespacing-by-key-prefix
category: computing-software
field: database-administration
product: memcached
tags: [namespacing, key-prefix, invalidate-by-group, versioned-keys, add]
level: practitioner
status: docs-checked
description: "Emulate namespaces with a versioned key prefix to invalidate groups of keys at once, using add and incr."
sources:
  - https://docs.memcached.org/userguide/usecases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memcached does not natively support namespaces or tags: you cannot atomically expire a namespace across all your servers without a lot of complication. You can emulate them with a coordinated key prefix, stored in configuration and changed manually, or stored in an external key.

To delete by namespace, set up a key holding a version number and prefix every group key with it; this costs an extra round trip to memcached to find the namespace.
```
user_prefix = get('user_namespace:' . user_id)
bio_data    = get(user_prefix . user_id . 'bio')
```
Fetch or create the namespace, using `add` so you never blow away an existing one:
```
key = 'namespace:' . user_id
namespace = get(key)
if (!namespace) {
    namespace = time()
    if (!add(key, namespace)) { namespace = get(key) }   # lost the race
}
```
Invalidate by editing the key; the old keys are no longer requested and eventually fall off the end of the LRU:
```
if (!incr(key, 1)) { add(key, time()) }   # incr failed: key must not exist
```
Initialise to something with a low probability of coming up again; an easy recommendation is a Unix timestamp. The docs call this not a perfect algorithm: it works well if invalidations are infrequent, since a missing key is always replaced with a larger number than was slowly incremented. Millisecond resolution drops the race condition further but makes the prefix longer; base64 encoding the number is suggested for bonus points.

## Checked

2026-11-04. Confirmed against the Use Cases page (Namespacing). Removed: nothing factual; code aligned to the page.

Method: documentation only; no commands were run.
