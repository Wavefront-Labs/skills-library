---
id: computing-software.digital-privacy-hygiene.password-managers.ssh-keys-in-a-password-manager-agent
name: ssh-keys-in-a-password-manager-agent
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, ssh-agent-password-manager, 1password-ssh-agent, bitwarden-ssh-agent, keepassxc-ssh-agent, ssh-keys, git-commit-signing]
level: practitioner
status: docs-checked
description: "Keep SSH private keys inside 1Password, Bitwarden or KeePassXC and use them through an SSH agent with approval, instead of plain key files; setup facts per product."
sources:
  - "https://developer.1password.com/docs/ssh/agent/"
  - "https://bitwarden.com/help/ssh-agent/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_ssh_agent_integration"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH keys in a password manager agent

**Goal:** private keys are not loose files that clients can read; use is approved by the manager.

## 1Password
- Needs the desktop app signed in on Mac, Windows or Linux. On Linux it does not work with Flatpak or Snap installs of 1Password.
- Keys must be SSH Key items (Ed25519 or RSA), in a configured vault, not archived or deleted. Each request still needs your approval; authorization settings control prompts and how long approvals are remembered.
- By default eligible keys in the Personal, Private or Employee vault are offered. For shared or custom vaults, write `~/.config/1Password/ssh/agent.toml`.
- On Mac and Linux set `SSH_AUTH_SOCK` and run `ssh-add -l` to list keys.
- With more than six keys, match keys to hosts via your SSH config or SSH Bookmarks, to avoid failures on OpenSSH servers that limit attempts.
- The page does not give the Settings steps or IdentityAgent paths (see its Get started and config guides).

## Bitwarden
- Desktop app: Settings, Enable SSH agent; "Ask for authorization when using SSH agent" controls approval prompts.
- Point `SSH_AUTH_SOCK` at the socket: Linux `/home/<user>/.bitwarden-ssh-agent.sock`; macOS .dmg `/Users/<user>/.bitwarden-ssh-agent.sock` (App Store build has a Containers path); Snap and Flatpak have their own paths. On Windows disable the OpenSSH Authentication Agent service. Test with `ssh-add -L`.
- Locked vault: list requests work after first unlock; sign requests prompt you to unlock and authorize. Logged out: agent not running.
- Commit signing needs Git 2.34+ and OpenSSH 8.8+: set `gpg.format ssh`, `user.signingkey` (public key), `commit.gpgsign true`, and `gpg.ssh.allowedSignersFile`. Add the key to GitHub as a Signing Key. Agent forwarding via `ssh -A`.

## KeePassXC
- It is a client for any OpenSSH-compatible agent, not an agent itself. Tools > Settings > SSH Agent > Enable SSH Agent integration (off by default).
- Windows: Pageant (default) and/or OpenSSH for Windows (start the OpenSSH Authentication Agent service). macOS and Linux: system ssh-agent via `SSH_AUTH_SOCK`, with an override path option. GPG's agent is incompatible.
- Keys must be in OpenSSH format (PuTTYgen needs conversion). Entry: put the key passphrase in the password field, attach the key file under Advanced, then pick it in the entry's SSH Agent category. Keys can autoload on unlock or be loaded from the entry context menu.

## Verify
- [ ] `ssh-add -l` (or `-L`) lists the manager's keys.
- [ ] A test `ssh -T git@github.com` triggers an approval prompt.

## Checked
Method: 2026-11-08 read all three cited sources. Removed as unsupported: 1Password IdentityAgent and Windows named-pipe details, "~/.1password/agent.sock", the KeePassXC "require user confirmation" wording, the IdentitiesOnly host pinning example, and 1Password commit signing. The Bitwarden macOS App Store path is omitted for brevity.
