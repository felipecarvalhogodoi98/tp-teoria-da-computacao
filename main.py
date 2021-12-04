import sys
from universal_turing_machine import UniversalTuringMachine

def main():
    with open(sys.argv[1], 'r') as archive: ## Fazendo leitura do arquivo passado como parametro na execução do código
        uh = archive.read()
        archive.close()
    utm = UniversalTuringMachine() ## Iniciando o objeto de MTU
    utm.read_uh(uh) ## Passando o valor de UH, para que MT desejada seja criada
    print('\nResultado:', utm.start()) ## Iniciar a execução da MTU e exibir o resultado

if __name__ == '__main__':
    main()