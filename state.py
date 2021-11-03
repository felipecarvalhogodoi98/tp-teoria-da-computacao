class State:

    def __init__(self, num_name, final): # Construtor
        self._name = "q" + str(num_name-1) # Adiciono um nome do tipo q+numero
        self._final = final # Adiciono o valor se é final ou não
        
    def get_name(self): # Retorno o nome do estado
        return self._name
        
    def get_final(self): # Retorno se o estado é final ou não
        return self._final
    