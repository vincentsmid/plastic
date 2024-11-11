#!/bin/bash

check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

echo "Running migrations..."
piccolo migrations forwards all
check_error "Running migrations"

echo "Creating admin user..."
piccolo user create --username=admin --password= --is_admin=t --is_superuser=t --is_active=t
check_error "Creating admin user"

echo "Migrations and user creation completed successfully"
