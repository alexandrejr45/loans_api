import pytest

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


def api():
    return APIClient()


def obtain_token():
    user = User.objects.create_user('test', 'example@com', 'password')
    token, _ = Token.objects.get_or_create(user=user)
    return token


def make_post_request(
    api: APIClient,
    token: Token,
    endpoint: str,
    data: dict
) -> Response:
    api.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api.post(endpoint, data=data, format='json')


class TestSimulateLoanView:

    @pytest.fixture
    def endpoint(self):
        return '/simulate-loan/'

    def test_should_simulate_a_loan_with_a_valid_user_and_amount(
        self,
        loan_simulation_payload,
        endpoint
    ):
        response = make_post_request(
            api(),
            obtain_token(),
            endpoint, loan_simulation_payload
        )

        assert response.status_code == HTTP_201_CREATED

    @pytest.mark.parametrize('birthdate', ['2018-12-09', '1900-10-03'])
    def test_should_return_error_400_if_client_birthdate_is_invalid(
        self,
        loan_simulation_payload,
        endpoint,
        birthdate
    ):
        loan_simulation_payload['user']['birthdate'] = birthdate

        response = make_post_request(
            api(),
            obtain_token(),
            endpoint, loan_simulation_payload
        )

        assert response.status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        'document_number', ['12345678902', '123456789', 'xablau']
    )
    def test_should_return_error_400_if_client_document_number_is_invalid(
            self,
            loan_simulation_payload,
            endpoint,
            document_number
    ):
        loan_simulation_payload['user']['document_number'] = document_number

        response = make_post_request(
            api(),
            obtain_token(),
            endpoint, loan_simulation_payload
        )

        assert response.status_code == HTTP_400_BAD_REQUEST
