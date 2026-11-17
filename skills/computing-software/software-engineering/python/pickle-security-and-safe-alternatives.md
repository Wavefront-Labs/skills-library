---
id: computing-software.software-engineering.python.pickle-security-and-safe-alternatives
name: pickle-security-and-safe-alternatives
category: computing-software
field: software-engineering
product: python
tags: [python, py-serialization, pickle-security, pickle, unpickling, restricted-unpickler, hmac, safe-serialization]
level: practitioner
status: docs-checked
description: "Why unpickling untrusted data is arbitrary code execution, how to restrict find_class, sign pickles with hmac and when to use a data-only format like json."
sources: ["https://docs.python.org/3/library/pickle.html#restricting-globals", "https://docs.python.org/3/library/pickle.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pickle security and safe alternatives

**Rule:** `pickle.load` / `pickle.loads` on data you did not produce and authenticate is equivalent to running attacker-chosen code (by default unpickling imports and calls any class or function named in the stream). `shelve` is built on pickle, so the same applies to it.

## Prefer data-only formats
The docs point to safer formats such as `json` for untrusted data, and to the marshalling API in `xmlrpc.client` or third-party solutions when security is a concern. Use pickle only for data you trust.

## If you must unpickle
1. **Authenticate first.** Sign with HMAC and verify before loading:
```python
import hmac, hashlib, pickle
def dumps(obj, key): 
    blob = pickle.dumps(obj, protocol=5)
    return hmac.new(key, blob, hashlib.sha256).digest() + blob
def loads(data, key):
    mac, blob = data[:32], data[32:]
    if not hmac.compare_digest(mac, hmac.new(key, blob, hashlib.sha256).digest()):
        raise ValueError("bad signature")
    return pickle.loads(blob)
```
This protects integrity, not confidentiality, and the key must be secret.
2. **Restrict globals** by overriding `Unpickler.find_class` (the documented approach; it is called whenever a class or function is requested):
```python
import io, pickle
SAFE = {("builtins", "set"), ("collections", "OrderedDict")}
class Restricted(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in SAFE: return super().find_class(module, name)
        raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")
obj = Restricted(io.BytesIO(data)).load()
```
The docs warn that you must be careful what you allow to be unpickled; keep the allow-list tiny.

## Gotchas
- Protocol versions: the default is 5 from 3.14 (4 in 3.8-3.13, 3 in 3.0-3.7); protocol 5 is incompatible with older versions. Classes are pickled by qualified name, so they must be importable at the same path when loading.
- `__setstate__` on your own classes is called during loading; keep it side-effect free.

## Verify
- [ ] Code search finds no `pickle.load` on request bodies, uploaded files, shared-cache entries or downloaded files.
- [ ] A test feeds a pickle that calls `os.system` to the restricted loader and expects `UnpicklingError`.

## Checked

- 2026-11-03: checked against the CPython docs `library/pickle.rst` (security warning and hmac signing advice, DEFAULT_PROTOCOL history, Restricting Globals / `find_class`, shelve note, classes pickled by name) and `library/hmac.rst` (`hmac.new(key, msg, digestmod)`, `compare_digest`).
- Removed: numpy, torch, joblib, pandas, safetensors, MessagePack, protobuf, Parquet and picklescan claims, and the multiprocessing remark (not in the pickle docs).

Method: documentation only; no commands were run.
