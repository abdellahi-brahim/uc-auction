userSchema = {
    'type': 'object',
    'required': ['username', 'phone', 'city', 'street', 'zipcode', 'password', 'first_name', 'last_name', 'email'],
    'proprieties': {
        'username': { 'type': 'string'},
        'phone': { 'type': 'number'},
        'city': { 'type': 'string'},
        'street': { 'type': 'string'},
        'zipcode': { 'type': 'string'},
        'password': { 'type': 'string'},
        'first_name': { 'type': 'string'},
        'last_name': { 'type': 'string'},
        'email': { 'type': 'string'}
    }
}
auctionSchema = {
    'type': 'object',
    'required':['title', 'description', 'minimum_price', 'start_time', 'end_time'],
    'proprieties': {
        'title': { 'type': 'string'},
        'description': { 'type': 'string'},
        'minimum_price': { 'type': 'number'},
        'start_time': { 'type': 'string'},
        'end_time': { 'type': 'string'}
    }
}

commentSchema = {
    'type': 'object',
    'required': ['date', 'content', 'auction_id'],
    'proprieties': {
        'date': {'type': 'string'},
        'content': {'type': 'string'},
        'auction_id': {'type', 'number'}
    }
}

bidSchema = {
    'type': 'object',
    'required': ['date', 'increase', 'auction_id'],
    'proprieties': {
        'date': {'type': 'string'},
        'increase': {'type': 'number'},
        'auction_id': {'type', 'number'}
    }
}

loginSchema = {
    'type': 'object',
    'required': ['username', 'password'],
    'proprieties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    }
}
