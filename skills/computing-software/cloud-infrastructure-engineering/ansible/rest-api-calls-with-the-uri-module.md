---
id: computing-software.cloud-infrastructure-engineering.ansible.rest-api-calls-with-the-uri-module
name: rest-api-calls-with-the-uri-module
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, uri-module, rest-api, delegate-api-calls]
level: practitioner
status: docs-checked
description: "Call REST APIs with ansible.builtin.uri: methods, JSON bodies, auth headers, status codes, retries, idempotence via GET-then-change, and secret-safe output."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/uri.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REST calls with the uri module

```yaml
- name: Look up existing DNS record
  ansible.builtin.uri:
    url: "https://dns.example.com/api/v1/records?name={{ fqdn }}"
    method: GET
    headers:
      Authorization: "Bearer {{ dns_token }}"
    return_content: true
    status_code: [200]
  register: existing
  delegate_to: localhost
  no_log: true

- name: Create record only if missing
  ansible.builtin.uri:
    url: https://dns.example.com/api/v1/records
    method: POST
    body_format: json
    body:
      name: "{{ fqdn }}"
      type: A
      content: "{{ ansible_default_ipv4.address }}"
    headers:
      Authorization: "Bearer {{ dns_token }}"
    status_code: [201, 409]
  register: created
  changed_when: created.status == 201
  when: existing.json.records | length == 0
  delegate_to: localhost
  no_log: true
```

## Key options
| Option | Use |
|---|---|
| `body_format` | `json` (serialises dict, sets Content-Type), `form-urlencoded`, `form-multipart`, `raw` |
| `status_code` | list of acceptable codes; anything else fails |
| `return_content` | include the body in `content`; independently of it, a `Content-Type` of `application/json` is always loaded into `json` |
| `url_username`/`url_password` + `force_basic_auth: true` | send the Basic header on the first request (otherwise an unauthenticated request is tried first) |
| `validate_certs`, `ca_path`, `client_cert` | TLS |
| `timeout` | seconds (default 30) |
| `follow_redirects` | `safe` (default), `all`, `none` or `urllib2` |

## Waiting for an API to be ready
```yaml
- ansible.builtin.uri: {url: "https://{{ inventory_hostname }}/health", status_code: 200}
  register: h
  until: h.status == 200
  retries: 30
  delay: 10
```

## Gotchas
- `uri` reports `changed: false` (except when it writes a `dest` file) whatever the method; set `changed_when` from the status code, since it cannot know whether a POST changed anything.
- Run API calls from the controller with `delegate_to: localhost` (and `run_once` if not per host).
- `no_log: true` hides tokens but also hides the task's output when it fails; disable it temporarily when debugging somewhere safe.

## Verify
- [ ] Second run makes no POST (the task is `skipped`).

## Checked
Checked 2026-10-26 against ansible-core devel `lib/ansible/modules/uri.py` (documentation block and code). Confirmed:
`body_format` choices, `status_code` default `[200]`, `timeout` default 30, `follow_redirects` choices and default `safe`,
`force_basic_auth`, `ca_path`, `client_cert`, `validate_certs`, `return_content` and the `json` key, and that `changed` stays
false unless `dest` is written. Corrected the `return_content`/`json` row and removed the unconfirmed POST-redirect advice.
Method: documentation only; no commands were run.
