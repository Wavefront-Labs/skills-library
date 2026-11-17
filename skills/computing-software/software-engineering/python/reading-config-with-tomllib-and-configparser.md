---
id: computing-software.software-engineering.python.reading-config-with-tomllib-and-configparser
name: reading-config-with-tomllib-and-configparser
category: computing-software
field: software-engineering
product: python
tags: [python, tomllib, configparser, configuration, environment-variables, pydantic-settings, python-stdlib]
level: practitioner
status: verified
description: "Load application config with tomllib (TOML) or configparser (INI), layer defaults, files and environment variables, and validate config at startup."
sources: ["https://docs.python.org/3/library/tomllib.html", "https://docs.python.org/3/library/configparser.html", "https://docs.pydantic.dev/latest/concepts/pydantic_settings/", "https://12factor.net/config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading config with tomllib and configparser

**Goal:** one predictable configuration path: defaults -> config file -> environment ->
CLI flags, validated once at startup with clear errors.

## TOML with tomllib (3.11+, read-only)
```python
import tomllib
from pathlib import Path
with open("config.toml", "rb") as f:          # must be binary mode
    cfg = tomllib.load(f)
db_url = cfg["database"]["url"]
```
```toml
[database]
url = "postgresql://localhost/app"
pool_size = 10
[features]
beta = ["search", "export"]
```
TOML has real types (int, bool, datetime, arrays). Writing TOML needs a third-party lib
(`tomli-w`, `tomlkit` to preserve comments). Older Pythons: `tomli` has the same API.

## INI with configparser
```python
import configparser
cp = configparser.ConfigParser(interpolation=None)   # disable %-interpolation surprises
cp.read(["/etc/app.ini", Path.home() / ".app.ini"])  # later files override earlier; missing ignored
timeout = cp.getfloat("server", "timeout", fallback=30.0)
debug = cp.getboolean("server", "debug", fallback=False)   # accepts yes/no/on/off/1/0
```
Everything is a string until you use `getint/getfloat/getboolean`. Keys are case-insensitive.
`read()` returns the list of files actually read - log it.

## Layering with environment variables
```python
import os
pool = int(os.environ.get("APP_DB_POOL_SIZE", cfg["database"].get("pool_size", 5)))
```
Better: declare once and validate with pydantic-settings:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
class DB(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_DB_", env_file=".env")
    url: str
    pool_size: int = 5
settings = DB()     # raises ValidationError listing every bad/missing field at startup
```
To also read TOML, add `TomlConfigSettingsSource` via `settings_customise_sources`; the
order of returned sources defines precedence.

## Secrets
Keep secrets out of committed config files: environment variables, mounted secret files
(`/run/secrets/...`), or a secret manager. Never log the resolved config without redaction.

## Gotchas
- Relative config paths resolve against cwd, which differs under systemd/cron/IDEs; resolve
  relative to an explicit `--config` flag or a well-known directory (`platformdirs`).
- Fail fast: a typo'd key should error at startup, not on the first request at 3am.
- Don't use `eval`/`ast.literal_eval` or Python files as config for untrusted input.

## Verify
- [ ] Startup logs which config files were loaded and from where (no secret values).
- [ ] Missing required setting -> process exits non-zero with a message naming the key.
