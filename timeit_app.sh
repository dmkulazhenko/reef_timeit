#!/bin/sh

# wait for db init
python ./mysql_waiter.py

# Migrate / upgrade db
if [ "x$1" = "xtrue" ]; then
  flask db init -d "$SQLALCHEMY_MIGRATIONS_DIR"
  flask db migrate -d "$SQLALCHEMY_MIGRATIONS_DIR"
fi
flask db upgrade -d "$SQLALCHEMY_MIGRATIONS_DIR"

# Initialize cron jobs
flask crontab add
crond

# Run fetcher job on startup
flask crontab run "$(flask crontab show | grep fetcher_job | cut -d ' ' -f 1)"

# Start gunicorn
exec gunicorn -b :5000 --workers 17 --threads 8 --timeout 90 --access-logfile - --error-logfile - timeit_app:app
