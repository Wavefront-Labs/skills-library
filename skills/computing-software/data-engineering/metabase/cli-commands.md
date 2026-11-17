---
id: computing-software.data-engineering.metabase.cli-commands
name: cli-commands
category: computing-software
field: data-engineering
product: metabase
tags: [cli, reset-password, rotate-encryption-key, enable-encryption, dump-to-h2, migrate]
level: advanced
status: docs-checked
description: "Use the Metabase JAR command line: reset-password, migrate directions, encryption commands, dump-to-h2, load-from-h2, export and import, plus their destructive caveats."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Form: `java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar <command>`. Start with `help [command-name]`; `version` prints version information.

- `migrate direction`: valid values `up`, `force`, `down`, `down-force`, `print`, `release-locks`. The page does not explain the differences.
- `reset-password email-address`: resets that user's password.
- `enable-encryption`: encrypts the database with `MB_ENCRYPTION_SECRET_KEY`. Run once with Metabase stopped; once the key is set, Metabase refuses to start until the database is encrypted.
- `rotate-encryption-key new-key`: needs `MB_ENCRYPTION_SECRET_KEY` set to the current key; the new key must be at least 16 characters.
- `remove-encryption`: decrypts, with the current key set.
- `export path` and `import path`: serialization. Export flags include `-c`, `-C`, `-S`, `-D`, `-f`, and both accept `-e, --continue-on-error` and `--full-stacktrace`.
- `dump-to-h2 h2-filename`: copies the application database into an H2 file. The target file is deleted first unless `-k, --keep-existing` is given; `-p` dumps plaintext.
- `load-from-h2`: loads an H2 database into a new MySQL or Postgres database, target set by environment variables.
- `api-documentation`, `generate-openapi-spec`, `config-template`, `command-documentation`, `all-documentation`: generate docs files.

Not documented: `force-set-password` is not listed on this page.

Tip: an H2 shell opens with `java -cp metabase.jar org.h2.tools.Shell -url jdbc:h2:/path/to/metabase.db`.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Metabase JAR commands: command form, help and version, migrate directions, reset-password, enable-encryption, rotate-encryption-key (16-character minimum), remove-encryption, export and import flags, dump-to-h2 flags, load-from-h2, documentation commands, H2 shell. Nothing removed.
Method: documentation only; no commands were run.
