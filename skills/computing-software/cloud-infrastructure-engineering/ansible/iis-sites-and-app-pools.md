---
id: computing-software.cloud-infrastructure-engineering.ansible.iis-sites-and-app-pools
name: iis-sites-and-app-pools
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows-automation, win-iis, iis, app-pool, win-feature, web-binding]
level: practitioner
status: docs-checked
description: "Install IIS and deploy a site with app pool, bindings and HTTPS certificate using win_feature and the community.windows or microsoft.iis modules, recycling only on change."
sources: ["https://github.com/ansible-collections/microsoft.iis/blob/main/plugins/modules/website.yml", "https://github.com/ansible-collections/microsoft.iis/blob/main/plugins/modules/web_app_pool.yml", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_certificate_store.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_feature.py", "https://github.com/ansible-collections/community.windows/blob/main/CHANGELOG.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS sites and app pools

## Install IIS
```yaml
- ansible.windows.win_feature:
    name: [Web-Server, Web-Common-Http]
    include_management_tools: true
    state: present
  register: iis
- ansible.windows.win_reboot:
  when: iis.reboot_required
```
## App pool
```yaml
- microsoft.iis.web_app_pool:
    name: Shop
    state: started
    attributes:
      processModel.identityType: ApplicationPoolIdentity
      managedPipelineMode: Integrated
      startMode: AlwaysRunning
```

## Site and bindings
```yaml
- microsoft.iis.website:
    name: Shop
    state: started
    physical_path: <DRIVE>:\Apps\Shop
    application_pool: Shop
    bindings:
      set:
        - protocol: http
          port: 80
          hostname: shop.example.com
        - protocol: https
          port: 443
          hostname: shop.example.com
          use_sni: true
          certificate_hash: "{{ shop_cert_thumbprint }}"
          certificate_store_name: My
```
`bindings.set` is the exact list (others are removed); `bindings.add` and `bindings.remove` change individual bindings. The application pool must already exist or the site will not start.
Import the certificate first with `ansible.windows.win_certificate_store` (`path`, `password`, `store_location: LocalMachine`, `key_storage: machine`); the module notes that `machine` key storage is needed so IIS app pool identities can read the private key.

The `community.windows` IIS modules (`win_iis_website`, `win_iis_webapppool`, `win_iis_webbinding`, `win_iis_webapplication`, `win_iis_virtualdirectory`) are deprecated and scheduled for removal in community.windows 4.0.0; use the `microsoft.iis` collection (`web_app_pool`, `website`, `web_application`, `virtual_directory`).

## Deploy with minimal downtime
```yaml
- ansible.windows.win_copy: {src: build/, dest: <DRIVE>:\Apps\Shop\}
  notify: Recycle Shop pool
handlers:
  - name: Recycle Shop pool
    microsoft.iis.web_app_pool: {name: Shop, state: restarted}
```

## Gotchas
- App pool identity `IIS AppPool\Shop` needs NTFS rights on the content folder (see `win_acl`).
- Pool `attributes` follow the IIS configuration reference names; use enum names (for example `SpecificUser`) rather than numbers. A binding's `ip:port:hostname` combination must be unique, and `hostname` is mandatory with `use_sni`.

## Verify
- [ ] `ansible.windows.win_uri: url=https://shop.example.com validate_certs=true` returns 200 from a client host.
- [ ] The IIS Manager (or `microsoft.iis.website_info` and `microsoft.iis.web_app_pool_info`) shows the site and pool started.

## Checked

Checked 2026-10-26 against the microsoft.iis, ansible.windows and community.windows sources (main). Confirmed: the community.windows `win_iis_*` modules are deprecated in favour of `microsoft.iis` (removal in 4.0.0); `microsoft.iis.website` options `name`, `physical_path`, `application_pool`, `state` and `bindings.set` / `add` / `remove` with `protocol`, `port`, `hostname`, `use_sni`, `certificate_hash` and `certificate_store_name`; `microsoft.iis.web_app_pool` `attributes` (`startMode`, `managedPipelineMode`, `processModel.identityType`) and states absent, present, restarted, started, stopped; `win_feature` `include_management_tools` and the `reboot_required` result; `win_certificate_store` `key_storage: machine` requirement. Removed the .NET hosting bundle, `app_offline.htm`, default site and case-sensitivity remarks.

Method: documentation only; no commands were run.
