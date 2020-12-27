#!/bin/sh

if [ "x$1" = "xtrue" ]; then
  flask db init -d "$SQLALCHEMY_MIGRATIONS_DIR"
  flask db migrate -d "$SQLALCHEMY_MIGRATIONS_DIR"
fi
flask db upgrade -d "$SQLALCHEMY_MIGRATIONS_DIR"

exec gunicorn -b :5000 --workers 4 --threads 8 --access-logfile - --error-logfile - timeit_app:app
