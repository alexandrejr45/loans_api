from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework import authentication, permissions

from loan_simulation.serializers import LoanSimulationSerializer

class CreateToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
            Cria o token de autenticação do usuário

            Este método cria o token de autenticação do usuário. O token é necessário para
            utilização das rotas que exigem autenticação. Ele deve ser enviado no cabeçalho 'Authorization'
            da requisição e ser precedido da palavara "Token" e um espaço em branco.
        """
        return super().post(request, *args, **kwargs)


class SimulateLoanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
           Simulate a loan with the provided informations.
        """
        try:
            serializer = LoanSimulationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            return Response(
                status=HTTP_201_CREATED,
                data=serializer.validated_data
            )

        except ValidationError as e:
            return Response(HTTP_400_BAD_REQUEST, data=e)
