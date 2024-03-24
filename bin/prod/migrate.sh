echo "Running migrations..."

poetry run piccolo migrations forwards all

echo "Migrations done"
