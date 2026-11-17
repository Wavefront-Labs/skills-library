---
id: computing-software.devops-ci-cd.packer.winrm-communicator
name: winrm-communicator
category: computing-software
field: devops-ci-cd
product: packer
tags: [winrm, windows, communicator, ssl, comm-winrm]
level: practitioner
status: docs-checked
description: "Configure the WinRM communicator for Windows guests, including ports, SSL, NTLM and timeouts."
sources:
  - "https://developer.hashicorp.com/packer/docs/communicators/winrm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `winrm` communicator uses Windows Remote Management to upload files and run scripts on the machine Packer creates. It is not the default communicator, so set `communicator = "winrm"` explicitly.

```hcl
source "null" "windows" {
  communicator   = "winrm"
  winrm_host     = "10.0.0.5"
  winrm_username = "Administrator"
  winrm_password = var.admin_password
  winrm_use_ssl  = true
  winrm_insecure = true
}
```

Options and defaults:

- `winrm_username` and `winrm_password`: credentials.
- `winrm_host`: the address to connect to.
- `winrm_port`: defaults to `5985` for plain connections and `5986` with SSL when `winrm_use_ssl` is true.
- `winrm_timeout`: wait for WinRM to become available; defaults to `30m` because setting up a Windows machine generally takes long.
- `winrm_use_ssl`: use HTTPS.
- `winrm_insecure`: do not check the server certificate chain and host name.
- `winrm_use_ntlm`: use NTLMv2 with session security instead of the default basic authentication, removing the need to enable basic auth on the guest.
- `winrm_no_proxy` (default false): adds the remote `host:port` to `NO_PROXY` so configured proxies are bypassed.

You will almost always need a pre-run script (PowerShell or batch) that enables and configures WinRM on the guest. For a brand-new OS image, supply it as part of the `Autounattend.xml` file (for example a `FirstLogonCommands` entry calling a batch file). In a cloud or from a pre-installed image the method varies by builder: AWS uses `user_data_file`, Google Cloud the `windows-startup-script-cmd` metadata tag.

Steps normally needed on the guest:

1. Set up a username and password for Packer.
2. Make registry edits to enable remote execution, with elevated privileges if needed.
3. Start WinRM, setting any config needed to allow basic auth.
4. Open ports 5985 and/or 5986 depending on how you connect.
5. Set WinRM to launch automatically at restart.
6. If necessary, generate a self-signed certificate or provide a real one for the listener (needed for HTTPS).

The docs' minimal batch file (`winrm quickconfig -q`, allowing unencrypted traffic and basic auth, enabling the remote administration firewall group, restarting WinRM) is explicitly described as extremely simplistic and not secure, and works for HTTP only. Close unneeded firewall ports and clean up in a final provisioning step so the image is secure. WinRM is not Packer-specific; if you still cannot connect, check Microsoft's WinRM documentation.

## Checked

Method: docs-checked 2026-11-09 against the Packer WinRM communicator page and its generated WinRM options reference (read in full as published page source). Dropped the connectivity-test and firewall/listener troubleshooting remarks, which are not on the page.
