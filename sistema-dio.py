from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco  
        self.contas = [] 
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco, email, telefone):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone

class Conta(ABC):
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0.0
        self.historico = Historico()

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        self.saldo -= valor
        return True
    
    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False
        self.saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente,limite=1000, limite_saques=3):
        super().__init__(numero, cliente)
        
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if valor > self.limite:
            print("Valor excede o limite de saque.")
            return False
        sucesso = super().sacar(valor)
        if sucesso:
            self.saques_realizados += 1
        return sucesso

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
          data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          conta.historico.adicionar_transacao(f"{data} - Depósito: R${self.valor}")

class Saque(Transacao):

    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
          data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          conta.historico.adicionar_transacao(f"{data} - Saque: R${self.valor}")

class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, descricao):
        self.transacoes.append(descricao)

    def exibir(self):
        print("\n======Extrato Bancário======")

        if not self.transacoes:
            print("Nenhuma transação realizada.")
        
        else:
            for transacao in self.transacoes:
                print(transacao)
       
def criar_cliente_conta(clientes, contas):
        nome = input("Digite o nome do cliente: ")
        cpf = input("Digite o CPF do cliente: ")    
        data_nascimento = input("Digite a data de nascimento:")
        endereco = input("Endereço do cliente: ")
        email = input("Email do cliente: ")
        telefone = input("Telefone do cliente: ")
        cliente = PessoaFisica(nome, cpf, data_nascimento, endereco, email, telefone)
        numero_conta = len(contas) + 1
        conta = ContaCorrente(numero_conta, cliente)
        cliente.adicionar_conta(conta)
        clientes.append(cliente)   
        contas.append(conta)
        print("Conta criada com sucesso!")



def criar_conta(clientes, contas):
        cpf = input("Cpf do cliente: ")
        for cliente in clientes:
            if cliente.cpf == cpf:
                numero_conta = len(contas) + 1
                conta = ContaCorrente(numero_conta, cliente)
                cliente.adicionar_conta(conta)
                contas.append(conta)
                print("Conta criada com sucesso!")
                return
        print("Cliente não encontrado.")

def depositar(clientes):
        cpf = input("Cpf do cliente: ")
        valor = float(input("Valor do depósito: "))
        for cliente in clientes:
            if cliente.cpf == cpf:
               if not cliente.contas:
                print("Cliente não possui conta. Crie uma conta primeiro.")
                return
            conta = cliente.contas[0]  
            transacao = Deposito(valor)    
            cliente.realizar_transacao(conta, transacao)
            print("Depósito realizado com sucesso!")
            return 
        print("Cliente não encontrado.")    

def sacar(clientes):
        cpf = input("Cpf do cliente: ")
        valor = float(input("Valor do saque: "))
        for cliente in clientes:
            if cliente.cpf == cpf:
                if not cliente.contas:
                    print("Cliente não possui conta. Crie uma conta primeiro.")
                    return
            conta = cliente.contas[0]
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)
            print("Saque realizado com sucesso!")
            return
        print("Cliente não encontrado.")

def exibir_extrato(clientes):
        cpf = input("Cpf do cliente: ")
        for cliente in clientes:
            if cliente.cpf == cpf:
                conta = cliente.contas[0]
                conta.historico.exibir()
                print(f"Saldo atual: R${conta.saldo:.2f}")
                return
        print("Cliente não encontrado.")

clientes = []
contas = [] 

while True: 
        print("\n=== Sistema Bancário ===")
        print("1. Criar cliente e conta:")
        print("2. Depositar:")
        print("3. Sacar:")
        print("4. Exibir extrato:")
        print("5. Sair:")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_cliente_conta(clientes, contas)
        elif opcao == "2":
            depositar(clientes)
        elif opcao == "3":
            sacar(clientes)
        elif opcao == "4":
            exibir_extrato(clientes)
        elif opcao == "5":
            print("Saindo do sistema. Obrigado por usar!")
            break
        else:
            print("Opção inválida. Tente novamente.")


             