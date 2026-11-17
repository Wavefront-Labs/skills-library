---
id: computing-software.collaboration-platform-administration.mattermost.smtp-email-setup
name: smtp-email-setup
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [smtp, email-notifications, system-console, amazon-ses]
level: practitioner
status: docs-checked
description: "Configure Mattermost SMTP in the System Console: required values, connection security, sample provider settings, test connection and troubleshooting."
sources: ["https://docs.mattermost.com/administration-guide/configure/smtp-email.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SMTP email setup

In production Mattermost needs SMTP for email notifications and password resets when email sign-in is used. Any SMTP service works; collect Server Name, Port, SMTP Username and SMTP Password. If you have none, Amazon SES can supply credentials (SMTP Settings > Create My SMTP Credentials); verify a domain, enable DKIM generation, set up SPF and/or DKIM, choose a sender such as mattermost@domain.com and send a test. Local sendmail is an option using server 127.0.0.1 and port 25. In Docker, the standard 172.16.0.0/12 range is not used; tell the mail service about 192.168.0.0/24 (with postfix, mynetworks = 192.168.0.0/24 in /etc/postfix/main.cf) to avoid relay errors. Outlook365 no longer supports the Basic Auth Mattermost needs, so use another service such as SES.

Configure:
1. System Console > Authentication > Email: set Allow Sign Up With Email to true.
2. System Console > Notifications > Email: set Send Email Notifications to true, Notification Display Name, Notification Email Address, SMTP Username, Password, Server and Port. Prefer Connection Security TLS. Ports in config use string form such as "465".
3. Save, then use Test Connection under Connection Security; failures show details in the console.

Sample settings from the page: Amazon SES uses email-smtp.us-east-1.amazonaws.com port 465 with TLS; Postfix on the same host uses localhost port 25 with empty username, password and security; Gmail uses smtp.gmail.com port 587 with STARTTLS (needs Google SMTP relay configuration); Hotmail uses smtp-mail.outlook.com port 587 STARTTLS; Office365 uses smtp.office365.com port 587 STARTTLS.

Troubleshooting: if you supply a username and password you must set Connection Security to TLS or STARTTLS. Check System Console > Logs and search the error code (for example 554 5.7.1 Client host rejected). A 550 5.7.27 failure sending the test means checking Site Configuration > Notifications. Test reachability from the Mattermost host with telnet mail.example.com 25 then HELO <domain>; Docker images lack telnet.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/configure/smtp-email (setup, sample settings, troubleshooting). Nothing removed.

Method: documentation only; no commands were run.
