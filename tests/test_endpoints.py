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
        self.registrations = []

    def test_endpoints(self):

        with self.subTest(f"Test health_check endpoint"):
            response = self.app.get(
                "/health_check"
            )
            self.assertEqual(response.status_code, 200)

        with self.subTest(f"test /competition endpoint"):
            payload = {
                "name": "Competição de testes 2",
                "modality": 2,
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

        with self.subTest(f"test update competition endpoint"):
            payload = {
                "name": "Competição de testes 2 - Editado",
                "modality": 2,
                "event_date": "22/02/2025",
                "status": "Open"
            }

            response = self.__perform_request(
                f"/competition/{self.competition_id}",
                "put",
                payload
            )

            competition_data = self.__get_competition_data(self.competition_id)

            print(f"Competição '{competition_data[0]['name']}' criada com sucesso.")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(competition_data[0]['name'], payload['name'])
            self.assertEqual(competition_data[0]['modality'], modalities[f"{payload['modality']}"])
            self.assertEqual(competition_data[0]['event_date'], payload['event_date'])
            self.assertEqual(competition_data[0]['status'], payload['status'])

        with self.subTest(f"test update competition endpoint with invalid status"):
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

        with self.subTest(f"test get competition endpoint"):

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

        with self.subTest(f"test get competitions list endpoint"):

            response = self.__perform_request(
                "competitions",
                "get"
            )

            competition_data = response.get_json()
            print(f"Evento: {competition_data['entries'][0]['modality']} ({competition_data['entries'][0]['name']})\nData: {competition_data['entries'][0]['event_date']}\n\n")

            self.assertEqual(response.status_code, 200)
            self.assertTrue(competition_data['entries'])
            self.assertTrue(len(competition_data['entries']) > 0)
            self.assertTrue(competition_data['entries'][0]['name'])
            self.assertTrue(competition_data['entries'][0]['modality'])
            self.assertTrue(competition_data['entries'][0]['event_date'])
            self.assertTrue(competition_data['entries'][0]['status'])

        with self.subTest(f"test endpoint to register in a competition"):
            print(f"Participação na competição")

            # Create 3 participants
            for j in range(3):
                # Try to register 4 tries for each participant
                for i in range(4):
                    payload = {
                      "athlete": f"Competidor {j + 1}",
                      "value": f"{random.uniform(0.1, 99.9)}"
                    }

                    response = self.__perform_request(
                        f"competition/{self.competition_id}/register",
                        "post",
                        payload
                    )

                    if i < 3:
                        content = response.get_json()
                        self.registration_id = content['registration_id']
                        print(f"Competidor {j+1}:\nTentativa registrada: ID {content['registration_id']}\n\n")
                        self.registrations.append(self.registration_id)
                        self.assertEqual(response.status_code, 201)
                        self.assertTrue(content['registration_id'])
                        self.assertTrue(len(content['registration_id']) > 0)
                    else:
                        #Test for 3 tries limite exceeded
                        self.assertEqual(response.status_code, 400)

        with self.subTest(f"[GET] registrations"):

            response = self.__perform_request(
                f"competition/{self.competition_id}/registrations",
                "get"
            )

            registration_data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(registration_data['entries'])
            self.assertTrue(len(registration_data['entries']) > 0)

        with self.subTest(f"[GET] registration"):

            for registration in self.registrations:
                response = self.__perform_request(
                    f"competition/{self.competition_id}/{registration}",
                    "get"
                )

                registration_data = response.get_json()
                print(f"Pessoa: {registration_data['entry'][0]['athlete']} \n Valor: {round(registration_data['entry'][0]['value'], 2)}\n\n")
                self.assertEqual(response.status_code, 200)
                self.assertTrue(registration_data['entry'])
                self.assertTrue(len(registration_data['entry']) > 0)

        with self.subTest(f"GET ranking"):

            response = self.__perform_request(
                f"competition/{self.competition_id}/ranking",
                "get",
                payload
            )

            content = response.get_json()

            self.assertEqual(response.status_code, 200)

            print("RANKING")
            for item in content['ranking']:
                print(f"{item['position']} - {item['athlete']} - {item['result']}\n")

            # Check ranking positions
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
