import json
import logging
import random

import grpc
from faker import Faker
from locust import User, task, constant

from proto.auth_service_pb2_grpc import AuthServiceStub
from proto.rpc_create_vacancy_pb2 import CreateVacancyRequest
from proto.rpc_signin_user_pb2 import SignInUserInput
from proto.rpc_update_vacancy_pb2 import UpdateVacancyRequest
from proto.vacancy_service_pb2 import VacancyRequest, GetVacanciesRequest
from proto.vacancy_service_pb2_grpc import VacancyServiceStub


logger = logging.getLogger(__name__)


with open("users.json", "r") as f:
    users = json.load(f)


class VacancyTest(User):
    wait_time = constant(30)
    host = "vacancies.cyrextech.net:7823"

    def on_start(self):
        self.fake = Faker()
        self.host = "vacancies.cyrextech.net:7823"
        self._channel = grpc.insecure_channel(self.host)
        self.user_stub = AuthServiceStub(self._channel)
        self.user = random.choice(users)
        self.login()
        self.vacancy_stub = VacancyServiceStub(self._channel)
        self.vacancy_id = None

    def login(self):
        response = self.user_stub.SignInUser(
            SignInUserInput(
                email=self.user['email'],
                password=self.user['password']
            )
        )
        self.access_token = response.access_token

    @task
    def create_vacancy(self):
        create_response = self.vacancy_stub.CreateVacancy(
            CreateVacancyRequest(
                Title=self.fake.text(max_nb_chars=5),
                Description=self.fake.text(max_nb_chars=10),
                Division=0,
                Country=self.fake.country(),
            )
        )
        self.vacancy_id = create_response.vacancy.Id

    @task
    def update_vacancy(self):
        self.vacancy_stub.UpdateVacancy(
            UpdateVacancyRequest(
                Id=self.vacancy_id,
                Title=self.fake.text(max_nb_chars=5),
                Country=self.fake.country(),
            )
        )

    @task
    def fetch_vacancy(self):
        self.vacancy_stub.GetVacancy(
            VacancyRequest(
                Id=self.vacancy_id,
            )
        )

    @task
    def delete_vacancy(self):
        self.vacancy_stub.DeleteVacancy(
            VacancyRequest(
                Id=self.vacancy_id,
            )
        )

    @task
    def fetch_all_vacancies(self):
        self.vacancy_stub.GetVacancies(
            GetVacanciesRequest(
                page=2,
                limit=2,
            )
        )


if __name__ == '__main__':
    pass
