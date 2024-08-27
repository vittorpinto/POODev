#%% Classes e Objetos Básicos
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def exibir_informacoes(self):
        print(f'Nome: {self.nome}, Idade: {self.idade}')


pessoa1 = Pessoa('João', 30)
pessoa1.exibir_informacoes()

pessoa2 = Pessoa('Maria', 25)
pessoa2.exibir_informacoes()

#%% Encapsulamento
class ContaBancaria:
    def __init__(self):
        self.__saldo = 0.0

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"Depositado: R${valor:.2f}")
        else:
            print("Valor de depósito inválido!")

    def sacar(self, valor):
        if 0 < valor <= self.__saldo:
            self.__saldo -= valor
            print(f"Sacado: R${valor:.2f}")
        else:
            print("Saldo insuficiente ou valor de saque inválido!")

    def consultar_saldo(self):
        print(f"Saldo atual: R${self.__saldo:.2f}")


conta = ContaBancaria()
conta.depositar(100)
conta.consultar_saldo()
conta.sacar(50)
conta.consultar_saldo()
conta.sacar(100)  

# %% Construtores
class Produto:
    def __init__(self, nome, preco, quantidade_estoque):
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

    def __str__(self):
        return f"Produto: {self.nome}, Preço: R${self.preco:.2f}, Estoque: {self.quantidade_estoque}"


produto1 = Produto("Notebook", 3500.00, 10)
produto2 = Produto("Mouse", 50.00, 150)
produto3 = Produto("Teclado", 120.00, 80)

print(produto1)
print(produto2)
print(produto3)

# %% Métodos e Sobrecarga
class Calculadora:
    def adicionar(self, *args):
        return sum(args)

    def subtrair(self, *args):
        if len(args) == 0:
            return 0
        resultado = args[0]
        for num in args[1:]:
            resultado -= num
        return resultado

    def multiplicar(self, *args):
        resultado = 1
        for num in args:
            resultado *= num
        return resultado

    def dividir(self, *args):
        if len(args) == 0:
            return 0
        resultado = args[0]
        for num in args[1:]:
            if num == 0:
                raise ValueError("Divisão por zero não é permitida.")
            resultado /= num
        return resultado

calc = Calculadora()
print(calc.adicionar(1, 2, 3))  
print(calc.subtrair(10, 5, 1))  
print(calc.multiplicar(2, 3, 4))  
print(calc.dividir(20, 2, 5)) 


# %% Herança Simples
class Veiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

class Carro(Veiculo):
    def __init__(self, marca, modelo, numero_portas):
        super().__init__(marca, modelo)
        self.numero_portas = numero_portas

    def exibir_detalhes(self):
        return f"Carro: {self.marca} {self.modelo} com {self.numero_portas} portas."

carro = Carro("Toyota", "Corolla", 4)
print(carro.exibir_detalhes())

# %% Polimorfismo
class Animal:
    def emitirSom(self):
        raise NotImplementedError("Subclasse deve implementar este método.")

class Cachorro(Animal):
    def emitirSom(self):
        return "Latido"

class Gato(Animal):
    def emitirSom(self):
        return "Miau"

animais = [Cachorro(), Gato()]
for animal in animais:
    print(animal.emitirSom()) 

# %% Composição
class Motor:
    def __init__(self, tipo):
        self.tipo = tipo

    def ligar(self):
        return f"Motor {self.tipo} ligado."

class Carro:
    def __init__(self, marca, modelo, motor):
        self.marca = marca
        self.modelo = modelo
        self.motor = motor

    def ligar_carro(self):
        return f"{self.marca} {self.modelo}: {self.motor.ligar()}"


motor = Motor("V8")
carro = Carro("Ford", "Mustang", motor)
print(carro.ligar_carro())

# %% Associação e Agregação
class Aluno:
    def __init__(self, nome, matricula, nota):
        self.nome = nome
        self.matricula = matricula
        self.nota = nota

class Escola:
    def __init__(self):
        self.alunos = []

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)

    def listar_alunos(self):
        for aluno in self.alunos:
            print(f"Aluno: {aluno.nome}, Matrícula: {aluno.matricula}, Nota: {aluno.nota}")


escola = Escola()
aluno1 = Aluno("João", "123", 9.5)
aluno2 = Aluno("Maria", "456", 8.7)
escola.adicionar_aluno(aluno1)
escola.adicionar_aluno(aluno2)
escola.listar_alunos()

# %% Herança Múltipla (através de interfaces)
from abc import ABC, abstractmethod

class Movimentavel(ABC):
    @abstractmethod
    def mover(self):
        pass

class Desenhavel(ABC):
    @abstractmethod
    def desenhar(self):
        pass

class Personagem(Movimentavel, Desenhavel):
    def mover(self):
        return "Personagem movendo-se para a posição X."

    def desenhar(self):
        return "Desenhando personagem na tela."

personagem = Personagem()
print(personagem.mover())  
print(personagem.desenhar())

# %% Classes Abstratas
from abc import ABC, abstractmethod
import math

class FormaGeometrica(ABC):
    @abstractmethod
    def calcularArea(self):
        pass

class Quadrado(FormaGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def calcularArea(self):
        return self.lado * self.lado

class Circulo(FormaGeometrica):
    def __init__(self, raio):
        self.raio = raio

    def calcularArea(self):
        return math.pi * (self.raio ** 2)

quadrado = Quadrado(4)
circulo = Circulo(3)
print(quadrado.calcularArea()) 
print(circulo.calcularArea()) 

# %% Métodos Estáticos
import math

class MatematicaUtil:
    @staticmethod
    def quadrado(numero):
        return numero ** 2

    @staticmethod
    def cubo(numero):
        return numero ** 3

    @staticmethod
    def raiz_quadrada(numero):
        return math.sqrt(numero)

print(MatematicaUtil.quadrado(4)) 
print(MatematicaUtil.cubo(2))  
print(MatematicaUtil.raiz_quadrada(9))  

# %% Enums
from enum import Enum

class DiasDaSemana(Enum):
    SEGUNDA = 1
    TERCA = 2
    QUARTA = 3
    QUINTA = 4
    SEXTA = 5
    SABADO = 6
    DOMINGO = 7

class Agenda:
    def __init__(self):
        self.compromissos = {}

    def adicionar_compromisso(self, dia, compromisso):
        if dia not in self.compromissos:
            self.compromissos[dia] = []
        self.compromissos[dia].append(compromisso)

    def listar_compromissos(self):
        for dia, compromissos in self.compromissos.items():
            print(f"{dia.name}: {', '.join(compromissos)}")

agenda = Agenda()
agenda.adicionar_compromisso(DiasDaSemana.SEGUNDA, "Reunião de equipe")
agenda.adicionar_compromisso(DiasDaSemana.QUARTA, "Consulta médica")
agenda.listar_compromissos()

# %% Tratamento de Exceções
class Divisao:
    def dividir(self, numerador, denominador):
        if denominador == 0:
            raise ZeroDivisionError("Não é possível dividir por zero.")
        return numerador / denominador

divisao = Divisao()
try:
    print(divisao.dividir(10, 0))
except ZeroDivisionError as e:
    print(e)

# %% Coleções (ArrayList ou equivalente)
class Livro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor

    def __str__(self):
        return f"Livro: {self.titulo}, Autor: {self.autor}"

class Biblioteca:
    def __init__(self):
        self.livros = []

    def adicionar_livro(self, livro):
        self.livros.append(livro)
        print(f"{livro.titulo} adicionado à biblioteca.")

    def remover_livro(self, titulo):
        for livro in self.livros:
            if livro.titulo == titulo:
                self.livros.remove(livro)
                print(f"{titulo} removido da biblioteca.")
                return
        print(f"Livro {titulo} não encontrado na biblioteca.")

    def listar_livros(self):
        if not self.livros:
            print("Nenhum livro na biblioteca.")
        else:
            for livro in self.livros:
                print(livro)

biblioteca = Biblioteca()
livro1 = Livro("1984", "George Orwell")
livro2 = Livro("Dom Quixote", "Miguel de Cervantes")
biblioteca.adicionar_livro(livro1)
biblioteca.adicionar_livro(livro2)
biblioteca.listar_livros()
biblioteca.remover_livro("1984")
biblioteca.listar_livros()

# %% Iteradores e Loops
class Biblioteca:
    def __init__(self):
        self.livros = []

    def adicionar_livro(self, livro):
        self.livros.append(livro)
        print(f"{livro.titulo} adicionado à biblioteca.")

    def remover_livro(self, titulo):
        for livro in self.livros:
            if livro.titulo == titulo:
                self.livros.remove(livro)
                print(f"{titulo} removido da biblioteca.")
                return
        print(f"Livro {titulo} não encontrado na biblioteca.")

    def listar_livros(self):
        if not self.livros:
            print("Nenhum livro na biblioteca.")
        else:
            for livro in self.livros:
                print(livro)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.livros):
            livro = self.livros[self._index]
            self._index += 1
            return livro
        raise StopIteration

biblioteca = Biblioteca()
livro1 = Livro("1984", "George Orwell")
livro2 = Livro("Dom Quixote", "Miguel de Cervantes")
biblioteca.adicionar_livro(livro1)
biblioteca.adicionar_livro(livro2)

for livro in biblioteca:
    print(livro)

# %% Generics
class Caixa:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)
        print(f"Item {item} adicionado à caixa.")

    def remover_item(self):
        if self.itens:
            item = self.itens.pop(0)
            print(f"Item {item} removido da caixa.")
            return item
        print("A caixa está vazia.")
        return None

    def listar_itens(self):
        if not self.itens:
            print("A caixa está vazia.")
        else:
            for item in self.itens:
                print(item)

caixa = Caixa()
caixa.adicionar_item("Livro A")
caixa.adicionar_item(123)
caixa.listar_itens()
caixa.remover_item()
caixa.listar_itens()

# %% Desenvolvimento de um Sistema de Gestão de Funcionários
class Funcionario:
    def __init__(self, id, nome, cargo, salario):
        self.id = id
        self.nome = nome
        self.cargo = cargo
        self.salario = salario

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Cargo: {self.cargo}, Salário: {self.salario}"

class SistemaGestaoFuncionarios:
    def __init__(self):
        self.funcionarios = {}

    def adicionar_funcionario(self, funcionario):
        self.funcionarios[funcionario.id] = funcionario
        print(f"Funcionário {funcionario.nome} adicionado com sucesso.")

    def remover_funcionario(self, id):
        if id in self.funcionarios:
            del self.funcionarios[id]
            print(f"Funcionário com ID {id} removido com sucesso.")
        else:
            print(f"Funcionário com ID {id} não encontrado.")

    def atualizar_funcionario(self, id, nome=None, cargo=None, salario=None):
        if id in self.funcionarios:
            funcionario = self.funcionarios[id]
            if nome:
                funcionario.nome = nome
            if cargo:
                funcionario.cargo = cargo
            if salario:
                funcionario.salario = salario
            print(f"Funcionário com ID {id} atualizado com sucesso.")
        else:
            print(f"Funcionário com ID {id} não encontrado.")

    def listar_funcionarios(self):
        if not self.funcionarios:
            print("Nenhum funcionário cadastrado.")
        else:
            for funcionario in self.funcionarios.values():
                print(funcionario)

sistema = SistemaGestaoFuncionarios()
func1 = Funcionario(1, "Alice", "Engenheira", 7000)
func2 = Funcionario(2, "Bob", "Designer", 5000)
sistema.adicionar_funcionario(func1)
sistema.adicionar_funcionario(func2)
sistema.listar_funcionarios()
sistema.atualizar_funcionario(1, salario=7500)
sistema.remover_funcionario(2)
sistema.listar_funcionarios()

# %%
