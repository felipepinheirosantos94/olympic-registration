import sqlalchemy as db

modalities = {
    "1": "100m rasos",
    "2": "Lançamento de Dardo"
}

engine = db.create_engine('sqlite:///:memory:?check_same_thread=False')
connection = engine.connect()
metadata = db.MetaData()

competitions_table = db.Table(
    'competitions', metadata,
    db.Column('id', db.Integer(), primary_key=True),
    db.Column('public_id', db.String(255), nullable=False),
    db.Column('name', db.String(255), nullable=True),
    db.Column('status', db.String(255), nullable=True),
    db.Column('modality', db.String(255), nullable=True),
    db.Column('event_date', db.String(255), nullable=True)
)

registrations_table = db.Table(
    'registrations', metadata,
    db.Column('id', db.Integer(), primary_key=True),
    db.Column('public_id', db.String(255), nullable=False),
    db.Column('athlete', db.String(255), nullable=True),
    db.Column('value', db.Float(), nullable=True),
    db.Column('unit', db.String(1), nullable=True),
    db.Column('competition_id', db.String(255))
)
response = metadata.create_all(engine)
