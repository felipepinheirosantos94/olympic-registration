import unittest
from app import app
import json
from Competition import Competition
import random
from config import modalities

class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.competition_id = ""

    def test_endpoints(self):

        with self.subTest(f"Test health_check endpoint"):
            response = self.app.get(
                "/health_check"
            )
            self.assertEqual(response.status_code, 200)

        with self.subTest(f"test /competition endpoint"):
            payload = {
                "name": "Competição de testes 2",
                "modality": 1,
                "event_date": "20/02/2021"
            }

            response = self.__perform_request(
                "/competition",
                "post",
                payload
            )

            content = response.get_json()
            self.competition_id = content['competition_id']

            self.assertEqual(response.status_code, 201)
            self.assertTrue(len(self.competition_id) > 0)

            competition_data = self.__get_competition_data(self.competition_id)

            self.assertEqual(competition_data[0]['name'], payload['name'])
            self.assertEqual(competition_data[0]['modality'], modalities[f"{payload['modality']}"])
            self.assertEqual(competition_data[0]['event_date'], payload['event_date'])

        with self.subTest(f"[PUT] competition"):
            payload = {
                "name": "Competição de testes 2 - Editado",
                "modality": 2,
                "event_date": "22/02/2025",
                "status": "Closed"
            }

            response = self.__perform_request(
                f"/competition/{self.competition_id}",
                "put",
                payload
            )

            competition_data = self.__get_competition_data(self.competition_id)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(competition_data[0]['name'], payload['name'])
            self.assertEqual(competition_data[0]['modality'], "Modalidade 2")
            self.assertEqual(competition_data[0]['event_date'], payload['event_date'])
            self.assertEqual(competition_data[0]['status'], payload['status'])

        with self.subTest(f"[PUT] competition with BAD status"):
            payload = {
                "name": "Competição de testes 2 - Editado",
                "modality": 2,
                "event_date": "22/02/2025",
                "status": "Bad status"
            }

            response = self.__perform_request(
                f"/competition/{self.competition_id}",
                "put",
                payload
            )

            self.assertEqual(response.status_code, 400)

        with self.subTest(f"[GET] competition"):

            response = self.__perform_request(
                f"competition/{self.competition_id}",
                "get"
            )

            competition_data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(competition_data['entry'])
            self.assertTrue(len(competition_data['entry']) > 0)
            self.assertTrue(competition_data['entry'][0]['name'])
            self.assertTrue(competition_data['entry'][0]['modality'])
            self.assertTrue(competition_data['entry'][0]['event_date'])
            self.assertTrue(competition_data['entry'][0]['status'])

        with self.subTest(f"[GET] competitions"):

            response = self.__perform_request(
                "competitions",
                "get"
            )

            competition_data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(competition_data['entries'])
            self.assertTrue(len(competition_data['entries']) > 0)
            self.assertTrue(competition_data['entries'][0]['name'])
            self.assertTrue(competition_data['entries'][0]['modality'])
            self.assertTrue(competition_data['entries'][0]['event_date'])
            self.assertTrue(competition_data['entries'][0]['status'])

        with self.subTest(f"[POST] /competition/<competition_id>/register"):

            for i in range(3):
                payload = {
                  "competicao": self.competition_id,
                  "atleta": "Joao das Neves",
                  "value": f"{random.uniform(0.1, 99.9)}"
                }

                response = self.__perform_request(
                    f"competition/{self.competition_id}/register",
                    "post",
                    payload
                )

                content = response.get_json()
                self.registration_id = content['registration_id']

                self.assertEqual(response.status_code, 201)
                self.assertTrue(content['registration_id'])
                self.assertTrue(len(content['registration_id']) > 0)

        with self.subTest(f"GET ranking"):

            response = self.__perform_request(
                f"competition/{self.competition_id}/ranking",
                "get",
                payload
            )

            content = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(
                content['ranking'][0]['value'] >= content['ranking'][1]['value'] >= content['ranking'][2]['value']
            )

    def __perform_request(self, endpoint, method, payload={}):
        return getattr(self.app, method)(
            endpoint,
            data=json.dumps(payload),
            content_type="application/json"
        )

    def __get_competition_data(self, competition_id):
        competition = Competition()
        return competition.get_competition_by_public_id(competition_id)


if __name__ == '__main__':
    unittest.main(verbosity=2)
