import os
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# docker run --name postgres-dev -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres 