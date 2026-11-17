---
id: computing-software.software-engineering.python.sqlalchemy-sessions-and-unit-of-work
name: sqlalchemy-sessions-and-unit-of-work
category: computing-software
field: software-engineering
product: python
tags: [python, py-databases, py-db-sqlalchemy, sqlalchemy-sessions, sqlalchemy, orm, session, unit-of-work, n-plus-one]
level: practitioner
status: draft
description: "Use SQLAlchemy 2.0 Sessions correctly: engine and sessionmaker, transaction scope with begin(), select() queries, relationship loading, expire_on_commit, and avoiding N+1 queries."
sources: ["https://docs.sqlalchemy.org/en/20/orm/session_basics.html", "https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQLAlchemy sessions and the unit of work

```python
from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker, selectinload

class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates="posts")

engine = create_engine("postgresql+psycopg://user@host/db", pool_pre_ping=True)   # one Engine per process
SessionLocal = sessionmaker(engine, expire_on_commit=False)

with SessionLocal.begin() as session:               # begins a transaction; commits on success, rolls back on exception, closes
    u = User(name="ada")
    session.add(u)
    users = session.scalars(select(User).where(User.name.like("a%")).options(selectinload(User.posts))).all()
```

## Session rules
- A Session is a unit of work and identity map: it tracks changes and flushes SQL on `flush()`, `commit()` or before queries (autoflush). It is **not thread-safe** or shareable across async tasks; create one per request/job and close it.
- Use `with Session(engine) as s:` and `s.begin()` blocks (or `SessionLocal.begin()`) so the transaction boundary is visible. Handle errors by rolling back; after an exception inside a flush the Session needs `rollback()`.
- `expire_on_commit=True` (default) reloads attributes after commit; set `False` when returning objects after the session closes (detached objects), accepting possibly stale data.
- Async: `AsyncSession` with `create_async_engine`, and `await session.run_sync` or eager loading since lazy loads need I/O (`MissingGreenlet`).

## N+1 queries
Lazy loading a relationship per row issues one query per row. Use `selectinload` (separate `IN` query, good for collections), `joinedload` (single JOIN, good for many-to-one), or `lazy="raise"` on relationships to make accidental lazy loads fail in tests. Enable `echo=True` or `sqlalchemy.engine` logging to count statements.

## Bulk work
Prefer Core `insert()`/`update()` with `session.execute(insert(User), [{"name": "a"}, ...])` (executemany, ORM bulk insert in 2.0) over adding thousands of ORM objects; flush in batches.

## Gotchas
- `session.query()` is legacy; 2.0 style uses `select()` + `session.execute/scalars`.
- Detached instance errors come from touching expired or lazy attributes after close.
- Mixing `commit()` inside library functions fragments transactions; let the caller own the boundary.
- Concurrent updates: use `with_for_update()` or version counters (`version_id_col`).
- Pool exhaustion if sessions are not closed: check `engine.pool.status()`.

## Verify
- [ ] A test counts SQL statements (event listener on `before_cursor_execute`) and asserts a bounded number for a list endpoint.
- [ ] Failure injection shows no partial writes after an exception in the `begin()` block.
