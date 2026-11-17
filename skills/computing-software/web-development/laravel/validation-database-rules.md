---
id: computing-software.web-development.laravel.validation-database-rules
name: validation-database-rules
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, unique, exists, database-rules]
level: practitioner
status: docs-checked
description: "Use the Laravel exists and unique validation rules: custom columns, connections, models, Rule::unique ignore, where clauses and soft deletes."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`exists:table,column` requires the value to exist; `unique:table,column` requires that it does not. The column defaults to the field name.

```php
'state' => ['exists:states'],
'state' => ['exists:states,abbreviation'],
'email' => ['exists:connection.staff,email'],          // custom connection
'user_id' => ['exists:App\Models\User,id'],            // model gives the table
'email' => ['unique:App\Models\User,email_address'],
'email' => ['unique:connection.users,email_address'],
```

Customise the query fluently with `Rule`:

```php
Rule::exists('staff')->where(function (Builder $query) {
    $query->where('account_id', 1);
});
Rule::exists('states', 'abbreviation');
'states' => ['array', Rule::exists('states', 'abbreviation')], // one query checks all values
```

Unique ignoring the current record on an update screen:

```php
Rule::unique('users')->ignore($user->id);
Rule::unique('users')->ignore($user);               // model key extracted automatically
Rule::unique('users')->ignore($user->id, 'user_id'); // non-id primary key
Rule::unique('users', 'email_address')->ignore($user->id);
Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1));
```

Never pass user-controlled request input to `ignore`; pass only a system-generated unique ID (auto-increment or UUID) from a model, or the app is open to SQL injection.

Soft-deleted rows count by default. Exclude them:

```php
Rule::unique('users')->withoutTrashed();
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

An empty string skips normal rules, so `unique:users,name` passes for `['name' => '']`.

## Checked

2026-11-07

Method: read the whole validation page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed exists and unique forms, Rule::exists and Rule::unique, ignore, soft-delete handling and the empty-string implicit-rules note.
