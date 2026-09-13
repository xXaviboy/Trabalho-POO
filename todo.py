import json


class Tarefa:
    def __init__(self, descricao, concluida=False):
        self.descricao = descricao
        self.concluida = concluida

    def concluir(self):
        self.concluida = True

    def para_dict(self):
        return {
            "descricao": self.descricao,
            "concluida": self.concluida
        }


class ListaTarefas:
    def __init__(self, arquivo="tarefas.json"):
        self.arquivo = arquivo
        self.tarefas = []
        self.carregar()

    def adicionar_tarefa(self, descricao):
        self.tarefas.append(Tarefa(descricao))
        self.salvar()

    def listar_tarefas(self):
        if not self.tarefas:
            print("\nNenhuma tarefa cadastrada.")
            return

        print("\n=== LISTA DE TAREFAS ===")
        for i, tarefa in enumerate(self.tarefas, start=1):
            status = "✅ Concluída" if tarefa.concluida else "⏳ Pendente"
            print(f"{i}. {tarefa.descricao} - {status}")

    def concluir_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].concluir()
            self.salvar()
            print("Tarefa concluída com sucesso!")
        else:
            print("Índice inválido.")

    def remover_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            removida = self.tarefas.pop(indice)
            self.salvar()
            print(f"Tarefa '{removida.descricao}' removida.")
        else:
            print("Índice inválido.")

    def salvar(self):
        dados = [tarefa.para_dict() for tarefa in self.tarefas]

        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def carregar(self):
        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

                for item in dados:
                    self.tarefas.append(
                        Tarefa(
                            item["descricao"],
                            item["concluida"]
                        )
                    )
        except FileNotFoundError:
            pass


def menu():
    lista = ListaTarefas()

    while True:
        print("\n===== TODO LIST =====")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Remover tarefa")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            descricao = input("Descrição da tarefa: ")
            lista.adicionar_tarefa(descricao)

        elif opcao == "2":
            lista.listar_tarefas()

        elif opcao == "3":
            lista.listar_tarefas()
            indice = int(input("Número da tarefa: ")) - 1
            lista.concluir_tarefa(indice)

        elif opcao == "4":
            lista.listar_tarefas()
            indice = int(input("Número da tarefa: ")) - 1
            lista.remover_tarefa(indice)

        elif opcao == "5":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
