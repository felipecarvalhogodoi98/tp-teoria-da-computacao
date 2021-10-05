from tape import Tape
import json


def get_name_state(state):
    return 'q' + str(len(state) - 1)


class UniversalTuringMachine:

    def __init__(self):
        # Atributo que salva o conceito lógico da minha MT (Favor ver o conceito lógico no comentário no final do arquivo)
        self._mt = dict({})
        self._tapes = None
        ## self._tapes = []

    def read_uh(self, uh):
        # Retirando os valores de começo e fim da mt e da palavra
        uh = uh.replace('\n', '').split('000')
        # OBS: O replace de \n é para caso a entrada esteja em formato de melhor visualização para a pessoa (Facultativo)
        # Pegando a parte que representa a Maquina de Turing
        turing_machine_raw = uh[1]
        # Pegando a parte que representa a palavra que será lida
        word_raw = uh[-2]

        self.create_tape(word_raw)
        self.create_mt(turing_machine_raw)

    def create_tape(self, word_raw):  # Criando a fita
        self._tapes = Tape(word_raw)
        # self._tapes.append(Tape(word_raw))

    def create_mt(self, turing_machine_raw):  # Criando a MT
        # Separo todas as transições
        for transition in turing_machine_raw.split('00'):
            items = transition.split('0')  # Separo cada valor da transição
            # LEMBRETE: A ordem por ENQUANTO é 1º estado atual, 2º lendo x, 3º estado destino, 4º escrevendo y, 5º movendo a cabeça para direita/esquerda, 6º final ou não
            # Vejo se o estado atual não consta como chave, caso não consta eu crio uma chave com estado atual

            # Estado normal com funções de transição
            if len(items) >= 5:
                if items[0] not in self._mt.keys():
                    self._mt.update({
                        items[0]: dict({
                            'name': get_name_state(items[0]),
                            'final': len(items) > 5
                        })})

                # Vejo se o lendo x não consta como chave, caso não consta eu crio uma chave lendo x na chave [estado atual]
                if items[1] not in self._mt[items[0]].keys():
                    self._mt[items[0]].update({items[1]: None})
                # Salvo os valores (Estado destino, escrever y, direção da cabeça) na chave [lendo ]x da chave [estado atual]
                self._mt[items[0]][items[1]] = tuple(
                    (items[2], items[3], items[4]))

            # Estado sem função de transição
            else:
                self._mt.update({
                    items[0]: dict({
                        'name': get_name_state(items[0]),
                        'final': len(items) > 1
                    })})

        # Cria JSON com a mt
        with open('mt.json', 'w') as json_file:
            json.dump(self._mt, json_file, indent=4)

    def start(self):  # Função que realiza o processo da MT
        state = '1'

        i = 0
        while True:
            i += 1

            aux_state = state
            aux_value_tape = self._tapes.read_head()

            if aux_state not in self._mt.keys():  # Vejo se o estado atual que estou faz alguma transição
                return 'Parou no estado ' + get_name_state(aux_state)
            # Vejo se lendo x no [estado atual] ele realiza alguma transição
            if aux_value_tape not in self._mt[aux_state].keys():
                return 'Parou no estado ' + get_name_state(aux_state) + ' pois não leu ' + str(aux_value_tape)

            # Pego o proximo estado
            state = self._mt[aux_state][aux_value_tape][0]
            # Realizo a escrita na fita
            self._tapes.write_tape(self._mt[aux_state][aux_value_tape][1])
            # Vejo se move a cabeça da fita para direita ou esquerda
            if self._mt[aux_state][aux_value_tape][2] == '1':  # Caso Direita
                self._tapes.move_head_to_right()
            else:  # Caso Esquerda
                if self._tapes.move_head_to_left() is False:  # Vejo se a fita não quebrou
                    return 'ERRO - A fita foi quebrada!'

    def print_tape(self):  # Apenas um print
        self._tapes.print_tape()


# EXPLICAÇÃO
# {
    # "q0": { ## Ta no estado q0
        # final: false
        # "a": ## Ler a (ou seja a cabeça da fita está lendo a)
        # [
        # "q1", ## Vai para o q1
        # "b", ## Escreve b na fita
        # "R" ## Move a cabeça da fita para direita
        # ]
    # },
    # "q1": { ## Ta no estado q1
        # final: false
        # OBS: Nesse caso ele pode ler a ou b, tudo depende de qual valor a cabeça da fita está lendo
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
    # },
    # "q2": { ## Ta no estado q2
        # final: true ## é um estado final
        # "a": ## Ler a (ou seja a cabeça da fita está lendo a)
        # [
        # "q1", ## Vai para o q1
        # "b", ## Escreve b na fita
        # "R" ## Move a cabeça da fita para direita
        # ]
        #
    # }
# }
