---
id: computing-software.cybersecurity-defensive.wazuh.agent-anti-tampering
name: agent-anti-tampering
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [anti-tampering, package-uninstallation, uninstall-validation, validation-token]
level: advanced
status: docs-checked
description: "Block unauthorised Wazuh agent removal on Linux with the anti_tampering package_uninstallation setting and the uninstall_validation.env token or login file."
sources:
  - https://documentation.wazuh.com/current/user-manual/agent/agent-management/anti-tampering.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Anti-tampering requires validation from the Wazuh manager before the agent package can be uninstalled. It applies to Linux endpoints only.

Enable centrally in `/var/ossec/etc/shared/<GROUP>/agent.conf`:

```xml
<agent_config os="linux">
  <anti_tampering>
    <package_uninstallation>yes</package_uninstallation>
  </anti_tampering>
</agent_config>
```

Or locally: the same `<anti_tampering>` block inside `<ossec_config>` in `/var/ossec/etc/ossec.conf`, then `systemctl restart wazuh-agent`.

Authentication before uninstall:
- Temporary token (recommended): a POST to port 55000 at `/security/user/authenticate?raw=true`; the token can be reused across agents.
- Stored credentials: username and password kept on the endpoint, which is less secure.

`/var/ossec/etc/uninstall_validation.env` holds `VALIDATION_TOKEN` or `VALIDATION_LOGIN`, plus `VALIDATION_HOST` and `VALIDATION_SSL_VERIFY`. The page examples set `VALIDATION_SSL_VERIFY` to `"false"`.

Gotchas:
- Package removal keeps config files. Use `apt-get remove --purge`, or delete `/var/ossec/` on RPM-based systems.
- A missing env file gives a "Validation host not provided" error.
- Invalid credentials return HTTP 401.

## Checked

2026-11-03. Confirmed against the Wazuh page "Anti-tampering": Linux-only support, the centralized agent.conf and local ossec.conf blocks, the restart, token vs stored-credential authentication and the `/security/user/authenticate?raw=true` call on port 55000, the env file variables, the purge and /var/ossec/ removal notes, and the "Validation host not provided" and 401 errors. Removed: the unsupported "do not copy into production" advice.

Method: documentation only; no commands were run.
