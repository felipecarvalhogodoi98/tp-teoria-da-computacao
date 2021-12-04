from tape import Tape
from state import State
from instance import Instance
import json
import copy

class UniversalTuringMachine:

    def __init__(self):
        # Atributo que salva o conceito lógico da minha MT (Favor ver o conceito lógico no comentário no final do arquivo)
        self._mt = dict({})
        self._dict_states = dict({}) # Dicionário para armazenar o estados e seus nomes de referência (Favor ver o conceito lógico no comentário no final do arquivo)
        self._state_origin = '1' # Nome do primeiro estado
        self._word_raw = None # Armazenar a palavra de entrada

    def read_uh(self, uh):
        # Retirando os valores de começo e fim da mt e da palavra
        uh = uh.split('000')
        # OBS: O replace de \n é para caso a entrada esteja em formato de melhor visualização para a pessoa (Facultativo)
        # Pegando a parte que representa a Maquina de Turing
        turing_machine_raw = uh[1].strip()
        # Pegando a parte que representa a palavra que será lida
        self._word_raw = uh[-2].strip().split('0')
        self.create_mt(turing_machine_raw)

    def create_mt(self, turing_machine_raw):  # Criando a MT
        # Separo todas as transições
        for transition in turing_machine_raw.split('00'):
            items = transition.strip().split('0')  # Separo cada valor da transição
            if items != ['']:
                # LEMBRETE: A ordem por ENQUANTO é: 
                # 1º estado origem, [0]
                # 2º estado origem é final ou não, [1]
                # 3º lendo x, [2]
                # 4º estado destino, [3]
                # 5º estado destino é final ou não, [4]
                # 6º escrevendo y, [5]
                # 7º movendo a cabeça para direita/esquerda [6]
                # Vejo se o estado atual não consta como chave, caso não consta eu crio uma chave com estado atual
                name_state_source, final_state_source = items[:2] # Lendo os valores de estado origem e se estado origem é final ou não
                if name_state_source not in self._dict_states.keys(): # Vejo se o estado que acabei de ler consta como chave e possui assim já um Objeto de State
                    # Adiciono uma chave e um valor no dicionário de estados, a chave será nome do estado no arquivo, e valor o Objeto do tipo State
                    self._dict_states.update(dict({name_state_source : State(name_state_source.count('1'), True if (final_state_source == '11') else False)}))
                state_source = self._dict_states[name_state_source] # Pego o Objeto do tipo State do estado origem ao qual a chave faz referência
                read_x = items[2] # Pego o valor que precisa ler quando está no estado origem
                name_state_destiny, final_state_destiny = items[3:5] # Pego os valores de estado destino e se estado destino é final ou não
                if name_state_destiny not in self._dict_states.keys(): # Vejo se o estado que acabei de ler consta como chave e possui assim já um Objeto de State
                    # Adiciono uma chave e um valor no dicionário de estados, a chave será nome do estado no arquivo, e valor o Objeto do tipo State
                    self._dict_states.update(dict({name_state_destiny : State(name_state_destiny.count('1'), True if (final_state_destiny == '11') else False)}))
                state_destiny = self._dict_states[name_state_destiny] # Pego o Objeto do tipo State do destino origem ao qual a chave faz referência
                write_y = items[5] # Pego o valor de escrita da operação
                move = items[6] # Pego o valor de movimento da operação
                if state_source not in self._mt.keys(): # Vejo se o estado de origem não consta na minha mt como chave
                    # Caso não consta cria-se uma chave com estado origem, e adiciona no dicionário que o estado faz referência um chave com valor a ser lido e uma lista
                    self._mt.update(dict({state_source : dict({read_x : list([])})}))
                elif read_x not in self._mt[state_source].keys(): # Vejo se o valor a ser lido não consta no dicionário do estado
                    # Caso não consta adiciona no dicionário que o estado faz referência um chave com valor a ser lido e uma lista
                    self._mt[state_source].update(dict({read_x : list([])}))
                self._mt[state_source][read_x].append([state_destiny, write_y, move]) # Adiciona a operação a lista de operações ao ler x no estado qi
        
        # dict_json = dict({"mt_universal" : self._mt, "list_states" : self._dict_states})
        # with open('mt.json', 'w') as json_file:
            # json.dump(dict_json, json_file, indent=4)

    def start(self):  # Função que realiza o processo da MT
        state = self._dict_states[self._state_origin] # Pego o estado inicial
        list_instances = list([]) # Crio uma lista de Instâncias
        list_instances.append(Instance(state, Tape(self._word_raw), -1)) # Adiciono a lista de instância a instância inicial
        while (list_instances != []): # Só para quando não houver mais instâncias
            instance = list_instances.pop(0) # Retiro a primeira instância do vetor para trabalhar com ela
            if(instance.get_transition() % 1000 == 0 and instance.get_transition() != 0): # Verifico se ocorreu 1000 interações, desde do começo ou desde a última verificação
                answer = input("Já foram computadas um total de " + str(instance.get_transition()) + " transições, a MT pode estar em loop, deseja continuar? (y/n) ")
                if answer == "n":
                    return "INDEFINIDO! \nA MT foi finalizada antes de computar por completo a palavra " + str(self._word_raw) + " devido a loop ou outros fatores!"
            state_inst = instance.get_state() # Pego o estado da instância
            tape_inst = instance.get_tape() # Pego a tape da instância
            
            ## Print para ver o estado da tape por instancia
            # print("O estado da fita após " + str(instance.get_transition()) + " transições é:\n" + str(tape_inst.get_tape()) + "\nE se encontra no estado: " + str(state_inst.get_name()) + "\n\n")
            
            if state_inst not in self._mt.keys(): # Vejo se o estado em que a instância se encontra realiza alguma ação
                if state_inst.get_final(): # Vejo se o estado em que a instância se encontra é final
                    return "ACEITA! \nA MT aceita a palavra " + str(self._word_raw) + ", parou no estado " + str(state_inst.get_name()) + " foi necessário um total de " + str(instance.get_transition()) + " transições. \nA fita após as operações ficou assim: " + str(tape_inst.get_tape())
            elif tape_inst.read_head() not in self._mt[state_inst].keys(): # Vejo se o estado em que a instância se encontra, ler o valor da cabeça da tape
                if state_inst.get_final(): # Vejo se o estado em que a instância se encontra é final
                    return "ACEITA! \nA MT aceita a palavra " + str(self._word_raw) + ", parou no estado " + str(state_inst.get_name()) + " foi necessário um total de " + str(instance.get_transition()) + " transições. \nA fita após as operações ficou assim: " + str(tape_inst.get_tape())
            else: # Caso exista operação a ser feita no estado em que a instância se encontra
                for operation in self._mt[state_inst][tape_inst.read_head()]: # Faço todas as operações possiveis dentro do estado qi lendo x
                    # OBS: para cada nova operação uma nova instância será criada e adicionada a lista de instâncias
                    next_state = operation[0] # Pego o estado destino
                    new_tape = copy.copy(tape_inst) # Copio a tape
                    new_tape.write_tape(operation[1]) # Escrevo na tape o valor de y na cabeça da tape
                    if operation[2] == "1": # Vejo se operação de movimento é para direita
                        new_tape.move_head_to_right() # Movo para direita
                        list_instances.append(Instance(next_state, new_tape, instance.get_transition())) # Adiciono a nova Instância na lista de Instâncias
                    elif operation[2] == "11": # Vejo se operação de movimento é para esquerda
                        if new_tape.move_head_to_left(): # Vejo se a operação de mover para esquerda deu certo
                            list_instances.append(Instance(next_state, new_tape, instance.get_transition())) # Caso sim, adiciono a nova Instância na lista de Instâncias
            del(instance)
        return "REJEITA! \nA MT não aceita a palavra " + str(self._word_raw)
        
# EXPLICAÇÃO
# q0, q1 ... qn, são forma usadas para identificar um Objeto do tipo State
# As chaves mais externas (no caso q0 e q1) serão Objetos do tipo State, e o valor dessas chaves será outro dicionário
# As chaves mais internas serão o que conseguem ler na tape, quando se encontra num estado x, 
# e o valor desta chaves é uma a lista contendo as operações possiveis ao ler a o valor da chave na tape
# self._mt:
# {
    # q0:{ 
        # "11":[[q1, "111", "1"]],
        # "111":[[q1, "111", "1"], [q2, "1", "1"]]
    # },
    # q1:{
        # "111":[[q1, "111", "1"]]
    # }
# }
#################################################################################
# q0, q1 ... qn, são forma usadas para identificar um Objeto do tipo State
# As chaves são os nomes dos estados e como encontramos eles no arquvios
# Os valor serão os Objetos do tipo State ao qual cada chave faz referência
# self._dict_states:
# {
    # "1" : q0,
    # "11" : q1,
    # "111" : q2
# }
#################################################################################
## Informações de leitura:

## Elementos do alfabeto e seu respectivo parâmetro
# a = 1
# b = 11
# B = 111 

## Elementos de deslocação de cabeça e seu respectivo parâmetro
# R = 1
# L = 11

