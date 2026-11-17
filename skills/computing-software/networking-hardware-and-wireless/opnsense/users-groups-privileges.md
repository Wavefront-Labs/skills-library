---
id: computing-software.networking-hardware-and-wireless.opnsense.users-groups-privileges
name: users-groups-privileges
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [users, groups, privileges, access-control]
level: practitioner
status: docs-checked
description: "OPNsense local user manager: users, groups, privileges, source-network constraints, shell account naming and the local anchor for external auth."
sources: ["https://docs.opnsense.org/manual/users.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Users, groups and privileges

The user manager (System > Access) controls which GUI pages and which services each person can use. Authentication can come from the Local User Database, the Voucher Server (for the captive portal), LDAP (OpenLDAP, Active Directory, Novell eDirectory), RADIUS or OpenID Connect (Business Edition only). Authorization stays local: to give someone fine-grained access to configuration pages, they must exist in the local user list, where privileges attach, even if the password is validated externally. A local user is the linking pin to the ACL system; if a service only needs a yes/no password check (VPN, proxy), the user need not exist locally.

User fields include: Disabled, Username, Password or Scrambled Password (random, to block login), Full name, E-mail, Comments, Preferred landing page, Language, Login shell (admin users only), Expiration date, Group membership, Privileges (groups preferred), OTP seed, and Authorized Keys for SSH when a shell is set. Administrators with a shell have stricter naming rules (at most 33 characters of a limited set); other usernames are flexible because no shell account is created.

Groups bundle privileges: Group name, Description, Privileges, Members, and Source Networks, which restricts the group so its privileges apply only when connecting from the listed networks. Treat users as individuals and groups as roles. Privileges have an internal Id, assigned Users and Groups, and a Match column (grid only) showing the GUI paths the privilege allows.

When using LDAP or similar, ensure the firewall has a route to the server; for classic (non-VTI) IPsec tunnels a static route may be needed. Test with ping from the default source address.

## Checked

2026-11-03. Read the Users manual page (users.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
