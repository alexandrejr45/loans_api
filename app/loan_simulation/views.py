from dataclasses import asdict

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework import authentication, permissions

from loan_simulation.serializers import LoanSimulationSerializer
from loan_simulation.helpers import calculate_loan_simulation


class CreateToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
            Cria o token de autenticação do usuário

            Este endpoint cria o token de autenticação do usuário.
            O token é necessário para utilização das rotas que exigem autenticação.
            Ele deve ser enviado no cabeçalho 'Authorization' da requisição
            e ser precedido da palavara "Token" e um espaço em branco.


        """
        return super().post(request, *args, **kwargs)


class SimulateLoanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
           Realiza a simulação de um financiamento para um cliente.
        """
        try:
            serializer = LoanSimulationSerializer(data=request.data)

            if serializer.is_valid():
                loan_simulation_result = calculate_loan_simulation(
                    serializer.save()
                )

                return Response(
                    status=HTTP_201_CREATED,
                    data=asdict(loan_simulation_result)
                )

            return Response(
                status=HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        except Exception as e:
            return Response(HTTP_500_INTERNAL_SERVER_ERROR, data=e)
