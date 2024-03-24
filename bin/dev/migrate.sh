echo "Running migrations and creating first user..."

poetry run piccolo migrations forwards all
poetry run piccolo user create --username=admin --password=adminadminadmin --email=admin@gpcz.eu  --is_admin=t --is_superuser=t --is_active=t

echo "Migrations done"
