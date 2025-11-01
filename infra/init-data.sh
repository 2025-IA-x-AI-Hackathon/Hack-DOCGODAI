#!/bin/bash
set -e;

echo "MySQL initialization script running..."

if [ -n "${MYSQL_USER:-}" ] && [ -n "${MYSQL_PASSWORD:-}" ]; then
    echo "Creating user and granting privileges..."
    mysql -u root -p${MYSQL_ROOT_PASSWORD} <<-EOSQL
        GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';
        FLUSH PRIVILEGES;
EOSQL
    echo "User privileges granted successfully"
else
    echo "SETUP INFO: No additional user setup needed (using MYSQL_USER from environment)"
fi