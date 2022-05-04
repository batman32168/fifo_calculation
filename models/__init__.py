import sqlalchemy as db
engine = db.create_engine('postgresql://postgres:docuvita1@host.docker.internal:5432/fifo_calculator')
