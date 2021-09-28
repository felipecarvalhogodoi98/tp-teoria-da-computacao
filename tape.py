class Tape:
    
    def __init__(self, word_raw): ## Construtor
        self._head = 0 ## Define a posição inicial da cabeça de leitura
        self._tape = word_raw.split('0') ## Cria uma lista que será minha fita a ser lida
        
    def read_head(self): ## Pegar o elemento que minha cabeça de leitura está apontando
        return self._tape[self._head]
        
    def write_tape(self, value): ## Escrever um valor onde minha cabeça de leitura está apontando
        self._tape[self._head] = value
        
    def move_head_to_right(self): ## Mover minha cabeça de leitura para direita
        self._head += 1
        if len(self._tape) <= self._head: ## Caso a cabeça de leitura execeda o limite A DIREITA da minha fita, adiciono um valor BRANCO
            self._tape.append('111')
        
    def move_head_to_left(self): ## Mover minha cabeça de leitura para esquerda
        if self._head <= 0: ## Caso a cabeça de leitura execeda o limite A ESQUERDA da minha fita, retorno FALSE, caso não retoro TRUE
            return False
        self._head -= 1
        return True
        
    def print_tape(self): ## Apenas uma impressão da tape
        print(self._tape)