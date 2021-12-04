# Máquina de Turing Universal


## Descrição
Trabalho pratico Máquina de Turing Universal que implemente heurísticas para o Problema da Parada.
A Máquina de Turing Universal será chamada de UH

---

## Decodificação da UH
- Transições
  - <p>Formato δ(qi,fi, x) = [qj, fj, y, d]</p>
  
  | Transição  | Significado   |
  | ------------------- | ------------------- |
  |  qi | estado atual  |
  |  fi |  estado atual é final ou não |
  |  x |  lendo x |
  |  qj |  estado de destino |
  |  fj |  estado de destino é final ou não |
  |  y |   escrevendo y |
  |  d |  direção da cabeça de leitura |

- Codificação dos símbolos
  | Símbolo  | Codificação   |
  | ------------------- | ------------------- |
  | a | 1 |
  | b | 11 |
  | B | 111 |
  | # ou outro qualquer | 1111 ou mais |
  | q0 | 1 |
  | q1 | 11 |
  | qx | 1<sup>n+1</sup> |
  | R | 1 |
  | L | 11 |
  
---

## Como executar
  ``git clone https://github.com/felipecarvalhogodoi98/tp-teoria-da-computacao.git``<br>
  ``cd tp-teoria-da-computacao``<br>
  ``python3 main.py examples/nomeDaMquinaDeTuring/casoAexecutar.txt``<br>

  ``nomeDaMquinaDeTuring`` representa a UH para ser executada <br>
  ``casoAexecutar`` arquivo txt com a UH e palavra decodificadas

---

## Colaboradores 

- Alunos
  - <a href="https://github.com/ThiagoSallesSantos">Thiago Salles Santos</a>
  - <a href="https://github.com/felipecarvalhogodoi98">Felipe Carvalho Godoi</a>

- Professor
  - <a href="https://github.com/rdurelli">Rafael Durelli</a>


