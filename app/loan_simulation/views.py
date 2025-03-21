from dataclasses import asdict

from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.views import APIView

from loan_simulation.helpers.calculate_simulations import (
    calculate_loan_simulation
)
from loan_simulation.helpers.converters import convert_loan_model_to_dataclass
from loan_simulation.helpers.record_simulations import (
    save_loan_simulation,
    search_loan_simulation_by_simulation_id
)
from loan_simulation.serializers import LoanSimulationSerializer


class CreateToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
            Cria o token de autenticação do usuário

            Este endpoint cria o token de autenticação do usuário.
            O token é necessário para utilização das rotas que
            exigem autenticação. Ele deve ser enviado
            no cabeçalho 'Authorization' da requisição
            e ser precedido da palavara "Token"  e um espaço em branco.


        """
        return super().post(request, *args, **kwargs)


class SimulateLoanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
            Realiza a simulação de um financiamento para um cliente.
            O payload de request para realizar o financiamento
            segue o exemplo abaixo:

            {
                'amount': '10000',
                'user': {
                    'name': 'José',
                    'last_name': 'Silva',
                    'document_number': '01234567890',
                    'birthdate': '2000-02-21'
                },
                'payment_period': 24
            }

            amount - Valor do empréstimo solicitado
            user - usuário solicitante do empréstimo
                name - nome do usuário
                last_name - último nome do usuário
                document_number - cpf ou cnpj do usuário
                birthdate - data de nascimento do usuário
                payment_period - quantidade de meses
                                na qual o empréstimo vai ser pago

        """
        try:
            serializer = LoanSimulationSerializer(data=request.data)

            if serializer.is_valid():
                loan_simulation_result = calculate_loan_simulation(
                    serializer.save()
                )
                save_loan_simulation(loan_simulation_result)

                return Response(
                    status=HTTP_201_CREATED,
                    data=asdict(loan_simulation_result)
                )

            return Response(
                status=HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        except ValidationError as e:
            return Response(status=HTTP_400_BAD_REQUEST, exception=e)
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e
            )


class SimulateLoanDetailView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, simulation_id, format=None):
        """
            Endpoint to return a loan simulation by id

        """
        try:
            loan_simulation_result = convert_loan_model_to_dataclass(
                search_loan_simulation_by_simulation_id(simulation_id)
            )

            if loan_simulation_result:
                return Response(
                    status=HTTP_200_OK,
                    data=asdict(loan_simulation_result)
                )

            return Response(
                status=HTTP_404_NOT_FOUND,
                data={'error': 'Loan simulations was not found'}
            )

        except ValidationError as e:
            return Response(status=HTTP_400_BAD_REQUEST, exception=e)
        except Exception as e:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR, exception=e)
