---
id: computing-software.cloud-infrastructure-engineering.ansible.module-helpers-run-command-fetch-url-and-no-log-options
name: module-helpers-run-command-fetch-url-and-no-log-options
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-development, run-command, fetch-url, no-log-option, ansiblemodule]
level: advanced
status: docs-checked
description: "Use AnsibleModule helpers correctly: run_command without a shell, fetch_url and open_url for HTTP, and no_log in argument_spec so secrets never reach output."
sources: ["https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/urls.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/common/process.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# run_command, fetch_url and no_log options

## run_command
```python
rc, out, err = module.run_command(
    [module.get_bin_path('lvs', required=True), '--noheadings', '-o', 'lv_name', vg],
    check_rc=False,
    environ_update={'LC_ALL': 'C'},
)
if rc != 0:
    module.fail_json(msg='lvs failed', rc=rc, stdout=out, stderr=err)
```
- Pass a **list**: it runs without a shell. A string is split into a list and run with `shell=False` unless `use_unsafe_shell=True`, which runs it with `shell=True` (avoid).
- `get_bin_path(name, required=True)` searches `PATH`, any `opt_dirs`, and `/sbin`, `/usr/sbin`, `/usr/local/sbin`; with `required=True` it calls `fail_json` if the executable is missing.
- `check_rc=True` calls `fail_json` on a non-zero return code.
- `environ_update` updates environment variables for the command; `data=` supplies stdin; `cwd=` sets the working directory.
- With `use_unsafe_shell=False`, `expand_user_and_vars=True` (the default) expands `~` and environment variables such as `$SHELL` before running the command; `False` disables that expansion.

## fetch_url / open_url
```python
from ansible.module_utils.urls import fetch_url
resp, info = fetch_url(module, url, method='POST',
                       data=module.jsonify(payload),
                       headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token},
                       timeout=30)
if info['status'] not in (200, 201):
    module.fail_json(msg='API error', status=info['status'], body=info.get('body'))
data = module.from_json(resp.read())
```
- `url_argument_spec()` returns the shared spec (`url`, `force`, `http_agent`, `use_proxy`, `validate_certs`, `url_username`, `url_password` with `no_log`, `force_basic_auth`, `client_cert`, `client_key`, `use_gssapi`); extend your module's spec with it. `url_redirect_argument_spec()` adds `follow_redirects`.
- `fetch_url(module, url, data=None, headers=None, method=None, ..., timeout=10, ...)` returns `(response, info)`; on an HTTP error (status >= 400) `info['body']` holds the error response data.
- `open_url` is the underlying function that does not take the module object.

## no_log in argument_spec
```python
argument_spec = dict(
    api_token=dict(type='str', required=True, no_log=True),
    password=dict(type='str', no_log=True),
    password_length=dict(type='int', no_log=False),   # silence the 'password' name heuristic warning
)
```
- A parameter marked `no_log=True` is replaced in the logged invocation (the code uses `$REDACTED$` for logging) and its value is replaced by `VALUE_SPECIFIED_IN_NO_LOG_PARAMETER` where it appears in results.
- When `no_log` is unset, parameter names matching the module's password pattern (names containing `pass`, such as `password` or `passphrase`) are redacted and the module warns "Module did not set no_log for <name>"; set `no_log=False` explicitly when such a parameter is not a secret.
- `module.no_log_values` is the set of values that are masked; add runtime secrets to it.

## Verify
- [ ] A run with `-vvv` shows no secret values in the module invocation.

## Checked
Checked 2026-10-26 against ansible-core devel `module_utils/basic.py` (`run_command` docstring and signature, `get_bin_path`,
`PASSWORD_MATCH` no_log warning, `no_log_values`), `module_utils/common/process.py` (sbin search), `module_utils/urls.py`
(`url_argument_spec`, `url_redirect_argument_spec`, `fetch_url` signature, `info['body']`) and `module_utils/common/parameters.py`
(`VALUE_SPECIFIED_IN_NO_LOG_PARAMETER`). Corrected: the claim that `no_log` values appear as `********` and that names containing
`token`/`key` trigger the warning (the pattern matches `pass`-style names). Removed unconfirmed claims about `requests`,
`LC_ALL=C` and the sanity-test check. The Python examples were not run.
Method: documentation only; no commands were run.
