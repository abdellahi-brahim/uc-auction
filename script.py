class Test():
    def __init__(self, argumento):
        self.argumento = argumento

    def decorador(func):
        def inner(self, *args, **kwargs):
            connection = "Conexao"
            func(self, connection, *args, **kwargs)
            print(f"saindo")
        return inner

    @decorador
    def auxiliar(self, connection, terceiro):
        print(connection)
        print(terceiro)

test = Test("Teste")
test.auxiliar("Terceiro")