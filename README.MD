## Create all tables
"""database SQLAlchemy
db.create_all()
"""

## Drop all tables
"""database SQLAlchemy
db.drop_all()
"""

## Guide deploy flask to docker
- https://www.youtube.com/watch?v=fHQWTsWqBdE

## docker install psycopg2 error fixed
https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock

## docker-compose command: (build and up)
"""
docker-compose build --no-cache
docker-compose up -d name
"""

## Checking postgres database
"""
docker exec -it name bash
psql -U postgres
"""

## only rebuild specific service
"""
docker-compose up --force-recreate --no-deps service-name
"""