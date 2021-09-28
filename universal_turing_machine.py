from tape import Tape
import json

class UniversalTuringMachine:

    def __init__(self):
        self._mt = dict({}) ## Atributo que salva o conceito lógico da minha MT (Favor ver o conceito lógico no comentário no final do arquivo)
        self._tapes = None
        ## self._tapes = []
    
    def read_uh(self, uh):
        uh = uh.replace('\n', '').split('000') ## Retirando os valores de começo e fim da mt e da palavra
        ## OBS: O replace de \n é para caso a entrada esteja em formato de melhor visualização para a pessoa (Facultativo)
        turing_machine_raw = uh[1] ## Pegando a parte que representa a Maquina de Turing 
        word_raw = uh[-2] ## Pegando a parte que representa a palavra que será lida
        self.create_tape(word_raw) 
        self.create_mt(turing_machine_raw)
        
    def create_tape(self, word_raw): ## Criando a fita
        self._tapes = Tape(word_raw)
        ## self._tapes.append(Tape(word_raw))

    def create_mt(self, turing_machine_raw): ## Criando a MT
        for transition in turing_machine_raw.split('00'): ## Separo todas as transições
            items = transition.split('0') ## Separo cada valor da transição
            ## LEMBRETE: A ordem por ENQUANTO é 1º estado atual, 2º lendo x, 3º estado destino, 4º escrevendo y, 5º movendo a cabeça para direita/esquerda
            if items[0] not in self._mt.keys(): ## Vejo se o estado atual não consta como chave, caso não consta eu crio uma chave com estado atual
                self._mt.update({items[0] : dict({})})
            if items[1] not in self._mt[items[0]].keys(): ## Vejo se o lendo x não consta como chave, caso não consta eu crio uma chave lendo x na chave [estado atual]
                self._mt[items[0]].update({items[1] : None})
            self._mt[items[0]][items[1]] = tuple((items[2], items[3], items[4])) ## Salvo os valores (Estado destino, escrever y, direção da cabeça) na chave [lendo ]x da chave [estado atual]
    
    def start(self): ## Função que realiza o processo da MT
        state = '1'
        while True:
        
            aux_state = state
            aux_value_tape = self._tapes.read_head()
            
            if aux_state not in self._mt.keys(): ## Vejo se o estado atual que estou faz alguma transição
                return 'Parou no estado ' + str(aux_state)
            if aux_value_tape not in self._mt[aux_state].keys(): ## Vejo se lendo x no [estado atual] ele realiza alguma transição
                return 'Parou no estado ' + str(aux_state) + ' pois não leu ' + str(aux_value_tape)
                
            state = self._mt[aux_state][aux_value_tape][0] ## Pego o proximo estado
            self._tapes.write_tape(self._mt[aux_state][aux_value_tape][1]) ## Realizo a escrita na fita
            ## Vejo se move a cabeça da fita para direita ou esquerda
            if self._mt[aux_state][aux_value_tape][2] == '1': ## Caso Direita
                self._tapes.move_head_to_right()
            else: ## Caso Esquerda
                if self._tapes.move_head_to_left() is False: ## Vejo se a fita não quebrou
                    return 'ERRO - A fita foi quebrada!'
            
    def print_tape(self): ## Apenas um print
        self._tapes.print_tape()


## EXPLICAÇÃO
# {
    # "q0": { ## Ta no estado q0
        # "a": ## Ler a (ou seja a cabeça da fita está lendo a)
            # [
                # "q1", ## Vai para o q1
                # "b", ## Escreve b na fita
                # "R" ## Move a cabeça da fita para direita
            # ]
    # },
    # "q1": { ## Ta no estado q1
        ##OBS: Nesse caso ele pode ler a ou b, tudo depende de qual valor a cabeça da fita está lendo
        # "a": ## Ler a (ou seja a cabeça da fita está lendo a)
            # [
                # "q1", ## Vai para o q1
                # "b", ## Escreve b na fita
                # "R" ## Move a cabeça da fita para direita
            # ]
        # "b": ## Ler b (ou seja a cabeça da fita está lendo b)
            # [
                # "q0", ## Vai para o q0
                # "a", ## Escreve b na fita
                # "L" ## Move a cabeça da fita para esquerda
            # ]
    # }
# }