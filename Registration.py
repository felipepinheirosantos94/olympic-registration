from config import db, registrations_table, connection
import uuid
from Competition import Competition
from operator import itemgetter


class Registration:

    def __to_json(self, data):
        return [dict(row) for row in data]

    def register_for_competition(self, competition_id: str, athlete: str, value: str, unit: str) -> dict:
        public_id = str(uuid.uuid4())
        query = db.insert(registrations_table).values(
            public_id=public_id,
            athlete=athlete,
            value=float(value),
            unit=unit,
            competition_id=competition_id
        )
        connection.execute(query)
        return public_id

    def list_registers_by_competition_id(self, competition_id: str) -> dict:
        query = db.select([registrations_table]).where(registrations_table.columns.competition_id == competition_id)
        results = connection.execute(query)
        return self.__to_json(results)

    def get_competition_results(self, competition_id):
        results = self.list_registers_by_competition_id(competition_id)

        competition = Competition()
        competition_data = competition.get_competition_by_public_id(competition_id)

        reverse = False
        if len(competition_data) > 0 and results[0]['unit'] == 'm':
             reverse = True

        sorted_results = sorted(results, key=itemgetter('value'), reverse=reverse)

        ranking = []
        i = 1
        for result in sorted_results:
            ranking.append({
                "athlete": result['athlete'],
                "position": f"{i}º lugar",
                "result": f"{round(result['value'], 2)}{result['unit']}",
                "value": round(result['value'])
            })
            i = i + 1

        return ranking