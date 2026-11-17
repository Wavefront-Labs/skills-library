---
id: computing-software.software-engineering.typer.typer-terminating
name: typer-terminating
category: computing-software
field: software-engineering
product: typer
tags: [typer, exit, abort, exit-code, cli, exceptions]
level: intro
status: docs-checked
description: "Stop a Typer command early with raise typer.Exit(), set a non-zero exit code with code=, or raise typer.Abort() to print Aborted!."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/terminating.md
  - https://github.com/fastapi/typer/blob/master/docs_src/terminating/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/terminating/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/terminating/tutorial003_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terminating a Typer program

Usually let the function finish. When you must stop mid-way and skip all later code, raise an exception from anywhere in the call chain.

## typer.Exit()

```python
existing_usernames = ["rick", "morty"]


def maybe_create_user(username: str):
    if username in existing_usernames:
        print("The user already exists")
        raise typer.Exit()
    else:
        print(f"User created: {username}")


def send_new_user_notification(username: str):
    # Somehow send a notification here for the new user, maybe an email
    print(f"Notification sent for new user: {username}")


@app.command()
def main(username: str):
    maybe_create_user(username=username)
    send_new_user_notification(username=username)
```

Only `main()` is the CLI function (it takes the CLI argument). `maybe_create_user()` can end the whole program; when it raises `typer.Exit()`, `send_new_user_notification()` never runs. `main.py Camila` prints `User created: Camila` then `Notification sent for new user: Camila`; `main.py rick` prints only `The user already exists`.

Raising an exception does not mean an error: it is used because it halts execution, then Typer catches it and terminates the program normally.

## Exit with an error code

`typer.Exit()` takes an optional `code`, default `0` (no error). Pass another number to signal failure:

```python
@app.command()
def main(username: str):
    if username == "root":
        print("The root user is reserved")
        raise typer.Exit(code=1)
    print(f"New user created: {username}")
```

After the program runs, `echo $?` prints `0` for `main.py Camila` and `1` for `main.py root`. Other programs (such as a Bash script) can use that exit code.

## typer.Abort()

`raise typer.Abort()` works like `typer.Exit()` but also prints `Aborted!` to make it explicit that execution was aborted:

```python
@app.command()
def main(username: str):
    if username == "root":
        print("The root user is reserved")
        raise typer.Abort()
    print(f"New user created: {username}")
```

`main.py root` shows `The root user is reserved` followed by `Aborted!`.

## Which to pick

- Finished early, all fine: `typer.Exit()`.
- Early stop that is a failure for scripts: `typer.Exit(code=1)` (or another non-zero number).
- User declined or operation cancelled: `typer.Abort()`.

## Checked

2026-11-07. Read in full against terminating.md and docs_src terminating examples 1-3 (Typer docs repository checkout). Confirmed: typer.Exit, code=, echo $? results, typer.Abort and Aborted!. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
