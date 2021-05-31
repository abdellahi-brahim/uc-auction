
# uc-auction

Aplicação de leilões em Python3 com recurso a Flask e com uma base de dados postgres. A aplicação está alojada no heroku e poderá ser acessada neste link: https://uc-auction.herokuapp.com/

## Rotas

As rotas criadas estão expostas nos seguintes endereços:

### Registar Utilizador

```http

POST /user/ HTTP/1.1

Content-Type: application/json

Host: https://uc-auction.herokuapp.com/

Content-Length: 66

{

"username" : "abdellahi",

"phone" : 913078866,

"city" : "Coimbra",

"street" : "Rua Cidade Dili, Bloco 13, 1º Direito",

"zipcode": "3020-208",

"password" : "1a2b3c4d",

"first_name" : "Abdellahi",

"last_name" : "Brahim",

"email" : "uchihaabdellahi@gmail.com"

}

```

### Login

```http

PUT /user

Content-Type: application/json

Host: https://uc-auction.herokuapp.com/

{

"username": "abdellahi",

"password": "1a2b3c4d"

}
```
### Criar Eleição

```http
POST /auction HTTP/1.1

Content-Type: application/json

Host: https://uc-auction.herokuapp.com/

Content-Length: 66

{
    "title": "auction",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus eu ligula viverra, pellentesque sem non, tristique sapien. Aenean varius et ex eu vehicula.",
    "minimum_price": 100,
    "start_time": "2021-05-29 10:11:58.743155",
    "end_time": "2021-05-29 10:11:58.743155",
    "product_id": "9781234567897",
    "product_description": "Livro Mongo"
}
```
### Pesquisar eleição por id

```http
GET /auction/<id>

Header: access-token: token

Host: localhost:5000
```
### Editar detalhes de uma eleição
```http
POST /auction/<id>

Content-Type: application/json

Header: access-token: token

Host: https://uc-auction.herokuapp.com/

{

"title": "Novo Título",

"description": "Nova Descrição"

}
```
### Adicionar mensagem ao mural de um leilão
```http
PUT /auction/comment

Content-Type: application/json

Header: access-token: token

Host: https://uc-auction.herokuapp.com/

{

"auction_id": 1,

"content": "Qual é a edição do livro?"

}
```

### Listar um leilões com keywords
```http
GET /auction/<keyword>

Header: access-token: token

Host: https://uc-auction.herokuapp.com/
```

### Realizar uma licitação
```http
PUT /bid/<auction_id>/<bid>

Header: access-token: token

Host: https://uc-auction.herokuapp.com/
```

### Listar todas as notificações
```http
GET /user/notifications

Content-Type: application/json

Header: access-token: token
```

### Receber a data de fim do próximo leilão
```http
GET /auctions/next

Host: https://uc-auction.herokuapp.com/
```

### Terminar todos os leilões
```http
POST /auctions/end

Host: https://uc-auction.herokuapp.com/
```

### Listar todos os leilões em ocorrência
```http
GET /auctions/current

Host: https://uc-auction.herokuapp.com/
```


