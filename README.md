# Api para cálculos de simulações de empréstimos

Api criada com o objetivo de simular um empréstimo de um usuário e devolver uma resposta calculando o valor final da
simulação.

## Requisitos para executar o projeto

As principais tecnologias utilizadas são:
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Docker](https://docs.docker.com/)
- [pytest](https://docs.pytest.org/en/6.2.x/contents.html#toc)
- [Poetry](https://python-poetry.org/)


Para realizar a configuração do projeto, primeiramente é necessário que o **Docker** esteja instalado
e devidamente configurado no seu computador. Caso haja dúvidas sobre como realizar essa configuração, verifique 
o passo a passo descrito [Aqui](https://docs.docker.com/get-docker/).

**Obs: Nesse projeto o docker foi utilizado no modo _rootless_ visando garantir mais segurança e 
facilidade no momento do desenvolvimento. Caso você esteja utilizando docker no modo root, substitua
os comandos do arquivo Makefile para usarem _sudo_**

O projeto também faz uso de uma ferramenta auxiliar do Docker, o docker-compose.
Mais informações sobre instalação e configuração podem ser encontradas [Aqui](https://docs.docker.com/compose/).


Assim, para que o projeto seja executado iremos utilizar o _Makefile_. Esse arquivo contém todos os comandos para
executar o projeto. A seguir, eles serão explicados detalhadamente.


#### Instalação das dependências
Antes de realizar a instalação das dependências, certifique-se que os arquivos `.env` e `.env.db` estão na raiz do projeto. Nesses arquivos estão as variáveis de ambiente necessárias para a devida configuração e execução do projeto, como usuário e senha do banco de dados. 

Após a checagem das variavéis de ambiente, é necessário criar os containers, instalar as dependências, além de outras configurações necessárias. Para fazer isso, execute o comando abaixo:

```sh
    make install
```

Esse comando realizará a configuração inicial dos containers, além de executar as `migrations` e criar um usuário no django para facilitar a utlização do projeto.

**Obs: O comando make é exclusivo dos ambientes shell e Linux, plataforma na qual este projeto foi desenvolvido.
 Caso esteja utilizando outro sistema operacional, verifique o arquivo Makefile e execute os comandos presentes na aba `install` de forma sequencial.**

## Execução do projeto
Após a instalação das dependências, os containers serão criados e estarão prontos para serem iniciados. Para fazer isso, execute o comando abaixo:

```sh
    make run
```

Após a execução, os containers serão executadas em segundo plano, garantindo que o projeto esteja disponível nesse endereço: http://localhost:1337. Caso ocorra algum erro com a porta utilizada ou você possua outro projeto utilizando esta porta, altere as portas usadas em `docker-compose.prod.yml`. Nesse arquivo também é possível alterar o servidor padrão de execução do projeto na opção `command`.

#### Executando os testes
Quando o projeto já estiver sendo executado, é possível executar os testes com o comando abaixo:

```sh
    make tests
```
Com esse comando, os testes serão executados e ao final o pytest gerará um resultado dos testes que falharam e dos que tiveram sucesso.


#### Executando o lint da applicação
Nesse comando a ferramente flake8 e isort são executadas para garantir que o código está de acordo come essas diretrizes
do PEP8.

```sh
    make lint
```

#### Parando os containers
Ao executar esse comando todos os containers criados são parados.

```sh
    make stop
```

#### Apagando os containers criados
Ao executar esse comando todos os containers criados são apagados, incluindo os volumes.

```sh
    make clear
```

## Utilizando a API

#### Para criar os containers e subir a aplicação, utilize os 2 comandos abaixo:

```sh
    make install
    make create-super-user
```

Esses 2 comandos vão garantir que os containers serão criados e que um usuário padrão também será criado.
As credenciais do usuário são essas:

```sh
   username: "user_test"
   password: "user_password"
```
Você pode modificá-las nos arquivo `.env.dev` e `.env.prod` desse projeto.


#### Obtendo Token

A api está protegida com uma autenticação por token, impedindo a utilização de parte das rotas sem ele. Para obter um token, obtenha as credenciais de usuário e senha do django disponíveis no arquivo `.env` ou obtenha as credenciais de um usuário e senha criado por você.

Envie uma requisição `POST` com os parâmetros `username` e `password`, com os valores de usuário e senha para  `/auth-token/`.

Exemplo:
```sh
    {
        "username": user_test,
        "password": user_password,
    }
```
O token deve ser obtido na resposta da requisição. Para utilizá-lo, certifique-se de colocá-lo no cabeçalho `Authorization` da requisição e utilizar a palavra Token com um espaço em branco do valor do token. 

Exemplo:
```sh
    Token 86c10f0dad322b56cad089b1e671bea3cf26aab9
```

#### Rotas

A api possui somente uma rota: `simulate-loan/`. Nessa rota é possível enviar requisições do tipo POST e GET.
Quando a requisição é enviada como POST, a api cria uma nova simulação e devolve o resultado para o usuário.
Esse resultado é armazenado no banco de dados, assim é possível recuperá-lo novamente utilização a requisição do tipo GET.

#### Request POST

Request
```sh
    {
      "amount": "10000",
      "user": {
         "name": "José",
         "last_name": "Silva",
         "document_number": "01234567890",
         "birthdate": "1999-02-21"
      },
      "payment_period": 24
    }
```

Response

```sh
    {
      "id": "a769e2ca-f3ca-42aa-ba21-388ca9517a8e",
      "monthly_installment": 429.81,
      "total_amount": 10315.44,
      "total_interest_amount": 315.44,
      "user": {
          "name": "José",
          "last_name": "Silva",
          "document_number": "01234567890",
          "birthdate": "1999-02-21"
      }
    }
```

#### Curl

```sh
    curl --location 'localhost:1337/simulate-loan/' \
         --header 'Authorization: Token ef4a0e5c2fa083bf8af2e7bef1a4cc20135381a7' \
         --header 'Content-Type: application/json' \
         --data '{
              "amount": "10000",
              "user": {
              "name": "José",
              "last_name": "Silva",
              "document_number": "01234567890",
              "birthdate": "1999-02-21"
         },
        "payment_period": 24
    }'
```

Significado de cada atributo:

- **amount**: Valor do empréstimo
- **user.name**: Nome do cliente
- **user.last_name**: Sobrenome do cliente
- **document_number**: CPF ou CNPJ do cliente
- **birthdate**: Data de nascimento do cliente
- **payment_period**: Prazo de pagamento em meses do empréstimo
- **monthly_installment**: Parcela mensal do empréstimo
- **total_amount**: Valor total do empréstimo a pagar
- **total_interest_amount**: Valor total dos juros aplicados


#### Request GET

Para verificar uma simulação criada, basta criar uma simulação utilizando o método POST e depois requisitá-la para api
utilizando o método GET e o id da simulação.

#### Curl

```sh
    curl --location 'localhost:1337/simulate-loan/09d94efc-c93e-4e6b-97e4-e176da1797e3/' \ 
    --header 'Authorization: Token f9e6a489c482305d62ce306d304efcbbac02ec11'
```