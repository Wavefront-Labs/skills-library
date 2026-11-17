---
id: computing-software.web-development.gin.gin-database-transactions-gorm
name: gin-database-transactions-gorm
category: computing-software
field: web-development
product: gin
tags: [gin, database-sql, gorm, transaction, begintx, rollback, automigrate, shouldbindjson]
level: practitioner
status: docs-checked
description: "Use GORM with Gin handlers and wrap multi-write requests in transactions via db.BeginTx with deferred Rollback or GORM's db.Transaction."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/database.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin transactions and GORM

Goal: make multiple writes in one request succeed or fail together; optionally use GORM.

## database/sql transaction
Defer `tx.Rollback()` right after `BeginTx` so early returns roll back; call `tx.Commit()` last.

```go
r.POST("/transfer", func(c *gin.Context) {
	tx, err := db.BeginTx(c.Request.Context(), nil)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not begin transaction"})
		return
	}
	defer tx.Rollback()

	_, err = tx.ExecContext(c.Request.Context(),
		"UPDATE accounts SET balance = balance - $1 WHERE id = $2", 100, 1)
	if err != nil { /* 500 "debit failed" */ return }
	_, err = tx.ExecContext(c.Request.Context(),
		"UPDATE accounts SET balance = balance + $1 WHERE id = $2", 100, 2)
	if err != nil { /* 500 "credit failed" */ return }

	if err := tx.Commit(); err != nil { /* 500 "commit failed" */ return }
	c.JSON(http.StatusOK, gin.H{"status": "transfer complete"})
})
```

## GORM
GORM wraps `database/sql` and adds migrations, associations and a query builder.

```go
db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
db.AutoMigrate(&Product{})   // Product embeds gorm.Model

r.POST("/products", func(c *gin.Context) {
	var p Product
	if err := c.ShouldBindJSON(&p); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := db.Create(&p).Error; err != nil { /* 500 */ return }
	c.JSON(http.StatusCreated, p)
})
```

GORM transaction:

```go
err := db.Transaction(func(tx *gorm.DB) error {
	if err := tx.Model(&Account{}).Where("id = ?", 1).
		Update("balance", gorm.Expr("balance - ?", 100)).Error; err != nil {
		return err
	}
	return nil
})
```

## Gotcha
`db.Transaction` handles Begin, Commit and Rollback automatically based on the returned error.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Database Integration (BeginTx with deferred Rollback, GORM Create and Transaction, AutoMigrate).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
