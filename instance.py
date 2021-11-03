from tape import Tape
from state import State

class Instance:

    def __init__(self, state, tape): # Construtor
        self._state = state # Pego o estado ao qual a instancia está
        self._tape = tape # Pego a fita ao qual a instancia faz referência

    def get_state(self): # Retorno o estado
        return self._state
        
    def get_tape(self): # Retorno a tape
        return self._tape