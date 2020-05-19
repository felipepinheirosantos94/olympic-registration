from config import db, competitions_table, connection, modalities
import uuid


class Competition:

    def __init__(self):
        self.modality = modalities

    def __to_json(self, data):
        return [dict(row) for row in data]

    def register_competition(self, name: str, modality: str, event_date: str) -> dict:
        public_id = str(uuid.uuid4())
        query = db.insert(competitions_table).values(
            public_id=public_id,
            name=name,
            status="Open",
            modality=self.modality[f"{modality}"],
            event_date=event_date
        )
        connection.execute(query)
        return public_id

    def get_competition_by_public_id(self, public_id):
        query = db.select([competitions_table]).where(competitions_table.columns.public_id == public_id)
        results = connection.execute(query)
        return self.__to_json(results)

    def get_competitions(self):
        query = db.select([competitions_table])
        results = connection.execute(query)
        return self.__to_json(results)

    def update_competition_by_public_id(
            self, public_id:str, status:str, name:str, event_date:str, modality:str
    ) -> dict:

        query = db.update(competitions_table).values(
            status=status,
            name=name,
            event_date=event_date,
            modality=self.modality[f"{modality}"]
        )
        query = query.where(competitions_table.columns.public_id == public_id)
        results = connection.execute(query)
        return results