---
id: computing-software.software-engineering.php.php-php-cli-scripts
name: php-php-cli-scripts
category: computing-software
field: software-engineering
product: php
tags: [php, php-cli-scripts, cli]
level: practitioner
status: docs-checked
description: "Write robust PHP CLI scripts: argv/getopt, exit codes, STDIN/STDERR, signals, CLI SAPI differences and Symfony Console commands."
sources: ["https://www.php.net/manual/en/features.commandline.php", "https://www.php.net/manual/en/features.commandline.differences.php", "https://www.php.net/manual/en/function.getopt.php", "https://www.php.net/manual/en/reserved.variables.argv.php", "https://www.php.net/manual/en/function.pcntl-async-signals.php", "https://symfony.com/doc/current/console.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI scripts and Symfony Console

Plain script:
```php
#!/usr/bin/env php
<?php
declare(strict_types=1);
$opts = getopt('v', ['input:', 'limit::', 'help'], $restIndex);   // 'input:' required value, 'limit::' optional value
$files = array_slice($argv, $restIndex);                          // positional args after option parsing stopped
if (isset($opts['help']) || !isset($opts['input'])) { fwrite(STDERR, "Usage: tool --input FILE\n"); exit(2); }
set_error_handler(fn ($n, $s, $f, $l) => throw new ErrorException($s, 0, $n, $f, $l));   // warnings become exceptions
pcntl_async_signals(true); pcntl_signal(SIGTERM, function () use (&$stop) { $stop = true; });
try { run($opts); exit(0); } catch (Throwable $e) { fwrite(STDERR, $e->getMessage() . PHP_EOL); exit(1); }
```
Symfony Console command (invokable form from the current Symfony docs):
```php
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;

#[AsCommand(name: 'app:import')]      // the name users type after "php bin/console"
class ImportCommand
{
    public function __invoke(): int
    {
        return Command::SUCCESS;      // 0; Command::FAILURE is 1, Command::INVALID is 2 (incorrect usage)
    }
}
```

## What the manual states
- `getopt(string $short_options, array $long_options = [], int &$rest_index = null): array|false`. A trailing `:` means a required value, `::` an optional value; `$rest_index` (added in 7.1.0) receives the index where parsing stopped. Options that take no value come back as `false` in the result array, so test with `isset`.
- `pcntl_async_signals(?bool $enable = null): bool` enables or disables asynchronous signal handling; with null it returns the current setting (PHP 7.1.0 and later).
- The CLI SAPI overrides some php.ini directives: `html_errors` false, `implicit_flush` true, `max_execution_time` 0 (unlimited), `output_buffering` false, `register_argc_argv` true. These cannot be set to another value in php.ini (they are applied after the files are parsed) but can be changed at runtime.
- `$argv[0]` is the name used to run the script. `$argv` is unavailable when `register_argc_argv` is disabled. Because `$argv` can exist in other contexts, test for CLI with `php_sapi_name() === 'cli'`. The manual flags `register_argc_argv` as deprecated as of PHP 8.5.0.
- The CLI does not change the working directory to the script's directory. Plain-text error messages, no HTTP headers.
- The CLI defines constants for the I/O streams (the `STDERR` used above is one).
- Windows: the CLI binary is `php.exe` in the main folder; `php-win.exe` (built with `--enable-cli-win32`) behaves the same but shows no console.
- Symfony: command classes are auto-registered through `#[AsCommand]`; the command's code returns an integer exit status, and `Command::SUCCESS`, `FAILURE` and `INVALID` are equivalent to 0, 1 and 2.

## Gotchas
- Print data to STDOUT and diagnostics to STDERR so pipes stay clean; return non-zero exit codes on failure (cron and CI depend on them).
- Long-running scripts leak memory: process in batches, `unset` big arrays, and watch `memory_get_peak_usage`.
- Use `flock` or a lock file so cron-run commands do not overlap.
- Check the CLI's effective settings (`memory_limit`, OPcache) rather than assuming they match the web SAPI's.

Verify: run with no args and check `$?` is 2; redirect stdout to `/dev/null` and confirm diagnostics still show on the terminal.

## Checked
Confirmed 2026-11-08 against the PHP manual pages for command line usage, CLI differences from other SAPIs, getopt, `$argv` and pcntl_async_signals, plus the Symfony Console documentation. Removed as not stated by those pages: the claim that CLI `memory_limit` is often -1, that OPcache is off in CLI unless `opcache.enable_cli=1`, the `configure()`/`addArgument`/`addOption` example and `<info>` markup (the current docs show the invokable form), and "no shebang on Windows".
Method: docs-only read of cited pages, 2026-11-08
