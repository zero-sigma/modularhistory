#!/bin/bash

sleep 3 && wait-for-it.sh postgres:5432 --
sleep 3 && wait-for-it.sh elasticsearch:9200 --

writable_dirs=( ".backups" ".init" "_static" "_media" )
for writable_dir in "${writable_dirs[@]}"; do
    # Must be run by a www-data user:
    test -w "/modularhistory/$writable_dir" || {
        echo "Django lacks permission to write in ${writable_dir}."
        [[ "$ENVIRONMENT" = dev ]] && exit 1
    }
done

# python manage.py cleanup_django_defender  # TODO

[[ "$ENVIRONMENT" = prod ]] && {
    invoke db.backup || {
        echo "Failed to create db backup."
        exit 1
    }
}

python manage.py migrate || {
    echo "Failed to run db migrations."
    exit 1
}

python manage.py collectstatic --no-input || {
    echo "Failed to collect static files."
    exit 1
}

# Rebuild indexes.
python manage.py search_index --rebuild -f || {
    echo "Failed to rebuild elasticsearch indexes."
    exit 1
}

if [ "$ENVIRONMENT" = prod ]; then
    gunicorn core.asgi:application \
      --user www-data --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker \
      --workers 9 --max-requests 100 --max-requests-jitter 50
else
    # Create superuser if necessary.
    python manage.py createsuperuser --no-input --username="$DJANGO_SUPERUSER_EMAIL" --email="$DJANGO_SUPERUSER_EMAIL" &>/dev/null
    # Run the dev server.
    python manage.py runserver 0.0.0.0:8000
fi
