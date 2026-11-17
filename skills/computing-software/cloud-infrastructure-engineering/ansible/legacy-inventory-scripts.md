---
id: computing-software.cloud-infrastructure-engineering.ansible.legacy-inventory-scripts
name: legacy-inventory-scripts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, inventory-script, script-plugin, list-host, meta-hostvars, executable-inventory, json-inventory, cmdb-script, custom-inventory-script, migrate-to-plugin, inventory-json-schema]
level: practitioner
status: docs-checked
description: "Write or maintain an executable inventory script (--list / --host JSON contract with _meta.hostvars), run it through the script plugin, and decide when to replace it with an inventory plugin."
sources: ["https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#inventory-script-conventions", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/inventory/script.py", "https://docs.ansible.com/ansible/latest/plugins/inventory.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy inventory scripts

A script is any **executable** file passed with `-i`. The `script` plugin runs it and
parses JSON. Use it for a quick bridge to a CMDB, a SQL query, or a vendor tool with no
plugin; prefer a proper inventory plugin for anything long-lived (caching, `keyed_groups`,
`constructed`, better errors).

## 1. The contract
```bash
./inv.py --list          # whole inventory
./inv.py --host web1     # vars for one host (only called if _meta is absent)
```
`--list` output:
```json
{
  "web":  {"hosts": ["web1", "web2"], "vars": {"http_port": 80}, "children": ["web_eu"]},
  "web_eu": {"hosts": ["web2"]},
  "_meta": {"hostvars": {"web1": {"ansible_host": "10.0.0.1"}, "web2": {"ansible_host": "10.0.0.2"}}}
}
```
Always emit `_meta.hostvars` (even empty `{}`); without it Ansible calls `--host` once per
host, which is one process spawn per host. A group may be a bare list `"web": ["web1"]`.

## 2. Minimal script
```python
#!/usr/bin/env python3
import json, sys, subprocess
def inventory():
    rows = json.loads(subprocess.check_output(["cmdb-cli", "hosts", "--json"]))
    inv = {"_meta": {"hostvars": {}}}
    for r in rows:
        grp = inv.setdefault(r["role"], {"hosts": []})
        grp["hosts"].append(r["name"])
        inv["_meta"]["hostvars"][r["name"]] = {"ansible_host": r["ip"], "env": r["env"]}
    return inv
if "--host" in sys.argv:
    print(json.dumps({}))                 # _meta covers it
else:
    print(json.dumps(inventory()))
```
`chmod +x inv.py`. Test: `./inv.py --list` then `ansible-inventory -i ./inv.py --graph`.

## 3. Running it
- `-i ./inv.py`: the source must be an executable that returns Ansible inventory JSON.
- The script plugin does not cache results; scripts are responsible for their own caching.
- stderr is shown even when the script succeeds (`always_show_stderr`, default true; env `ANSIBLE_INVENTORY_PLUGIN_SCRIPT_STDERR`).

## 4. Migrate to a plugin
If a maintained plugin exists for the backend (for example `amazon.aws.aws_ec2`), replace the script: same groups via
`keyed_groups`, same derived vars via `compose`, plus `cache: true`. For a bespoke backend
write a plugin class (`BaseInventoryPlugin`, with `Constructable` and `Cacheable` as needed, per the developer guide) and you gain documentation and caching support.

## Gotchas
- Run the script by hand first: it must print valid JSON for `--list` or the plugin fails to parse it.
- Invalid characters in group names are handled by `TRANSFORM_INVALID_GROUP_CHARS` (ini `force_valid_group_names`): the default `never` allows the name with a warning, `always` replaces invalid characters with `_`, `ignore` stays silent.

## Verify
- [ ] `ansible-inventory -i ./inv.py --list` shows every host with its `_meta` variables and no warnings.
- [ ] `time ansible-inventory -i ./inv.py --list` is acceptable for your estate; otherwise add caching inside the script.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/dev_guide/developing_inventory.rst and plugins/inventory/script.py (stable-2.22): `--list` and `--host <hostname>` contract, group value as object or bare host list, `_meta.hostvars` (even empty) avoids a `--host` call per host, the plugin does not cache, always_show_stderr default true; BaseInventoryPlugin, Constructable and Cacheable are the documented base classes.
- Confirmed in config/base.yml: TRANSFORM_INVALID_GROUP_CHARS default never, choices always/never/ignore, ini force_valid_group_names; amazon.aws aws_ec2 inventory plugin exists.
- Removed unconfirmed claims: stderr only with -vvv, group-name rewriting by default, exit-code rules, typed JSON values, Windows launcher remark, the CMDB/AWX credential notes, the plugin line-count remark, the jq checks.

Method: documentation only; no commands were run.
