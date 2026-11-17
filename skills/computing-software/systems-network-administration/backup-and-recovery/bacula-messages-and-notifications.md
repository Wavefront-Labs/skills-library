---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-messages-and-notifications
name: bacula-messages-and-notifications
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula-messages, bacula, bareos, backup-notifications, bsmtp, job-alerts]
level: practitioner
status: docs-checked
description: "Configure Bacula/Bareos Messages resources: mail on error vs success, operator mount requests, bsmtp, log and catalog destinations, and message types to include or filter."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Messages_Resource.html
  - https://docs.bareos.org/Configuration/Messages.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Brief_Tutorial.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula Messages resource and notifications

**Goal:** the right people hear about failed jobs and mount requests, and every job log is kept, without drowning in success mail.

## How messages work
Each daemon has a full message handler, but File and Storage daemons normally send their messages back to the Director so everything for one Job is combined into one email or one log. Every message has a type (INFO, WARNING, ERROR, FATAL ...) and a message can go to several destinations. Define several Messages resources to treat Job types differently (for example Full versus Incremental). Records have the form `destination = message-type, ...` or `destination = address = message-type, ...`.

## Example (Director Messages resource, from the Bareos manual)
```
Messages {
  Name = Standard
  Mail Command = "/usr/sbin/bsmtp -h mail.example.com -f \"\(Bareos\) %r\" -s \"Bareos: %t %e of %c %l\" %r"
  Operator Command = "/usr/sbin/bsmtp -h mail.example.com -f \"\(Bareos\) %r\" -s \"Bareos: Intervention needed for %j\" %r"
  Mail On Error = backupoperator@example.com = all, !skipped, !terminate
  Append = "/var/log/bareos/bareos.log" = all, !skipped, !terminate
  Operator = backupoperator@example.com = mount
  Console = all, !skipped, !saved
}
```
The Bacula manual's equivalent uses `mailcommand`/`operatorcommand` with its own `bsmtp` path, `MailOnError`, `append`, `operator`, `console`, and adds `catalog = all`. Attach it to a Job with `Messages = Standard`.

Order matters: a `MailCommand` must appear before the `Mail`, `MailOnSuccess` or `MailOnError` directive it applies to, and `OperatorCommand` before `Operator`.

## Destinations
- `mail`: grouped during a job and sent as one email when the job ends; you hear about every job, which gets noisy with many machines (the manual suggests filtering with procmail).
- `mail on error`: emailed only if the job ends in error; discarded on success. Pair it with `append` so the output is still saved.
- `mail on success`: emailed only on normal termination.
- `operator`: like mail but each message is sent as received (one email per message); most useful for `mount` messages.
- `console`: held until the console connects to the Director.
- `append` (appends to the file, creates if missing) and `file` (overwrites an existing file).
- `syslog`: Bacula ignores the address field and always uses LOG_DAEMON / LOG_ERR; Bareos 14.4.0 and later can set the facility in the address field.
- `catalog`: written to the catalog `Log` table, pruned with the Job records, and used only by reporting programs.
- `director`, `stdout`, `stderr` also exist (stdout/stderr normally unused).
- Bareos lists multiple mail addresses as a comma-separated list without spaces.

## Message types
`info`, `warning`, `error` (non-fatal, investigate), `fatal`, `terminate`, `notsaved`, `skipped`, `mount` (volume mount or intervention requests), `restored`, `saved`, `security`, `alert` (tape alerts), `volmgmt`, `all`, and `events` in Bacula (`audit` in Bareos). In Bacula `all` excludes debug, events and saved; in Bareos `all` is every type. Exclude noise with `!skipped, !saved`. `skipped` is not an error (unchanged files, exclusions) while `notsaved` is.

## Substitutions (Mail and Operator commands)
Common to both manuals: `%c` client name, `%e` job exit status, `%i` JobId, `%j` unique job name, `%l` job level, `%n` job name, `%r` recipients, `%t` job type, `%%` literal percent. `%d` is the daemon's name in Bacula and the Director's name in Bareos.

## Gotchas
- With no MailCommand, Bacula mails with `mail -s "Bacula Message" <recipients>` and Bareos uses `/usr/lib/sendmail -F BAREOS <recipients>`; the manuals say this may not work on your machine, so set one explicitly (the manuals use `bsmtp`).
- Test any mail command: the manual warns some mail programs such as Exim can be selective about the forms allowed, particularly in the from part. With multiple recipients, replace `%r` in the sender part with one valid address.
- Messages not tied to a Job (no job running, or a daemon-Director communications error) may wait until the end of the next Job; Bacula mails those through `/usr/lib/sendmail`.
- `-t` makes a daemon read its configuration, print errors and exit, which is a syntax check (for example `bacula-dir -t -c <config file>`).

## Checked
2026-11-07. Read in full: Bacula Messages_Resource (the fetched text starts with a long table of contents; I read the Messages Resource section itself) and Bareos Configuration/Messages (all of it, including the type list and both examples). From Brief_Tutorial I read only the "Daemon Command Line Options" part for `-c` and `-t`. Corrections and trims: removed `audit` from the Bacula type list (it is Bareos-only; Bacula has `events`); corrected `%d` (daemon name in Bacula, Director in Bareos) and `%j` (unique job name); removed "operator = sent immediately" in favour of "each message sent as received"; removed the claim that catalog text is queried with `list joblog` and that daemon messages use a `Messages { Name = Daemon }` resource (neither is on the pages); removed the invented `reload` advice, the "bsmtp fails silently if the relay requires auth" claim with its test command, and the invented Verify step.
Method: documentation only; no commands were run.
