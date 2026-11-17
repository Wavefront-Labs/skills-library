---
id: computing-software.software-engineering.go.environment-driven-configuration-and-validation
name: environment-driven-configuration-and-validation
category: computing-software
field: software-engineering
product: go
tags: [go, go-cli-config, go-env-config, configuration, environment-variables, twelve-factor]
level: practitioner
status: docs-checked
description: "Load Go service configuration from environment variables into a typed struct with defaults, required fields, validation and secret redaction."
sources:
  - https://12factor.net/config
  - https://pkg.go.dev/os#LookupEnv
  - https://github.com/caarlos0/env
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment-driven configuration and validation

**Goal:** fail fast at start-up with a clear message, never half-configured at 3 a.m.

```go
type Config struct {
    Addr        string        `env:"ADDR" envDefault:":8080"`
    DatabaseURL string        `env:"DATABASE_URL,required"`
    Timeout     time.Duration `env:"TIMEOUT" envDefault:"5s"`
    APIKey      string        `env:"API_KEY,required"`
}

// slog calls LogValue (slog.LogValuer), so logging a Config never prints the key
func (c Config) LogValue() slog.Value {
    return slog.GroupValue(slog.String("addr", c.Addr), slog.String("api_key", "[redacted]"))
}

func Load() (Config, error) {
    var c Config
    if err := env.Parse(&c); err != nil { return c, err }   // github.com/caarlos0/env, or hand-rolled os.LookupEnv
    var errs []error
    if _, err := url.Parse(c.DatabaseURL); err != nil { errs = append(errs, fmt.Errorf("DATABASE_URL: %w", err)) }
    if c.Timeout <= 0 { errs = append(errs, errors.New("TIMEOUT must be positive")) }
    return c, errors.Join(errs...)
}
```

The twelve-factor config rule: store config in environment variables, strictly separated from code, because it varies between deploys. Load once in `main` and pass `Config` down explicitly (no globals). `os.LookupEnv` returns `(string, bool)` so you can tell "unset" from "empty" if you hand-roll the loader. The `caarlos0/env` library supports `time.Duration`, `url.URL` and the built-in types, the `env` tag options `,required`, `,notEmpty`, `,file` (the variable holds a path to read), `,unset` and `,expand`, and `envDefault`.

## Gotchas
- With `caarlos0/env`, a variable that is set but empty falls back to `envDefault`, and `required` is then satisfied by the default; use `,notEmpty` only if there is no default.
- Redact secrets when logging effective config: a type implementing `slog.LogValuer` controls what `log/slog` prints.
- `time.Duration` fields parse strings such as `5s`; `time.ParseDuration` does the same for a hand-rolled loader.
- Validate cross-field rules in one place and combine failures with `errors.Join`.

## Verify
Unit-test `Load` with `t.Setenv` for each required variable missing, and check the error names the variable.

## Checked
2026-11-03. Confirmed: 12factor.net/config (store config in env, separate from code), the caarlos0/env README (tags, `,required`, `,notEmpty`, `,file`, supported types, empty-value caution, `env.Parse`), pkg.go.dev for `os.LookupEnv`, `log/slog.LogValuer`, `errors.Join`, `testing.T.Setenv`, `time.ParseDuration`. Removed: `*_FILE` convention and `/proc/<pid>/environ` claim, the named `Secret` string type (custom types are not shown as supported by the library), `fmt.Errorf` wrapped messages kept only as plain Go.
Method: documentation only; no commands were run.
