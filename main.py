import json
import os

class Tarefa:
    """Classe que representa uma única tarefa."""
    def __init__(self, titulo, concluida=False):
        self.titulo = titulo
        self.concluida = concluida

    def concluir(self):
        self.concluida = True

    def para_dict(self):
        """Converte a tarefa em dicionario para salvar no JSON."""
        return {"titulo": self.titulo, "concluida": self.concluida}

    def __str__(self):
        status = "[X]" if self.concluida else "[ ]"
        return f"{status} {self.titulo}"


class GerenciadorTarefas:
    """Classe que gerencia a lista de tarefas e o salvamento em arquivo."""
    def __init__(self, arquivo="tarefas.json"):
        self.arquivo = arquivo
        self.tarefas = []
        self.carregar_dados()

    def adicionar_tarefa(self, titulo):
        nova_tarefa = Tarefa(titulo)
        self.tarefas.append(nova_tarefa)
        self.salvar_dados()

    def listar_tarefas(self, status_desejado="todas"):
        """
        Lista as tarefas. 
        status_desejado pode ser: 'todas', 'pendentes' ou 'concluidas'.
        """
        if not self.tarefas:
            print("\nNenhuma tarefa cadastrada.")
            return

        print(f"\n--- LISTA DE TAREFAS ({status_desejado.upper()}) ---")
        encontrou = False

        for i, tarefa in enumerate(self.tarefas):
            if status_desejado == "pendentes" and not tarefa.concluida:
                print(f"{i + 1}. {tarefa}")
                encontrou = True
            elif status_desejado == "concluidas" and tarefa.concluida:
                print(f"{i + 1}. {tarefa}")
                encontrou = True
            elif status_desejado == "todas":
                print(f"{i + 1}. {tarefa}")
                encontrou = True

        if not encontrou:
            print(f"Nenhuma tarefa {status_desejado} encontrada.")

    def concluir_tarefa(self, numero):
        indice = numero - 1
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].concluir()
            self.salvar_dados()
            print("Tarefa marcada como concluída com sucesso!")
        else:
            print("Número de tarefa inválido.")

    def remover_tarefa(self, numero):
        indice = numero - 1
        if 0 <= indice < len(self.tarefas):
            tarefa_removida = self.tarefas.pop(indice)
            self.salvar_dados()
            print(f"Tarefa '{tarefa_removida.titulo}' removida com sucesso!")
        else:
            print("Número de tarefa inválido.")

    def salvar_dados(self):
        """Salva a lista de tarefas no arquivo JSON."""
        dados = [t.para_dict() for t in self.tarefas]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_dados(self):
        """Carrega as tarefas salvas do arquivo JSON, se ele existir."""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    for item in dados:
                        tarefa = Tarefa(item["titulo"], item["concluida"])
                        self.tarefas.append(tarefa)
            except Exception:
                self.tarefas = []


def menu_principal():
    gerenciador = GerenciadorTarefas()

    while True:
        print("\n=================================")
        print("    GERENCIADOR DE TAREFAS")
        print("=================================")
        print("1. Adicionar tarefa")
        print("2. Listar TODAS as tarefas")
        print("3. Listar tarefas PENDENTES")
        print("4. Listar tarefas CONCLUÍDAS")
        print("5. Marcar tarefa como concluída")
        print("6. Remover tarefa")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Digite a descrição da tarefa: ").strip()
            if titulo:
                gerenciador.adicionar_tarefa(titulo)
                print("Tarefa adicionada com sucesso!")
            else:
                print("O título não pode ser vazio.")

        elif opcao == "2":
            gerenciador.listar_tarefas("todas")

        elif opcao == "3":
            gerenciador.listar_tarefas("pendentes")

        elif opcao == "4":
            gerenciador.listar_tarefas("concluidas")

        elif opcao == "5":
            gerenciador.listar_tarefas("pendentes")
            if gerenciador.tarefas:
                try:
                    num = int(input("\nDigite o número da tarefa a concluir: "))
                    gerenciador.concluir_tarefa(num)
                except ValueError:
                    print("Por favor, digite um número válido.")

        elif opcao == "6":
            gerenciador.listar_tarefas("todas")
            if gerenciador.tarefas:
                try:
                    num = int(input("\nDigite o número da tarefa a remover: "))
                    gerenciador.remover_tarefa(num)
                except ValueError:
                    print("Por favor, digite um número válido.")

        elif opcao == "0":
            print("\nSaindo do programa. Até mais!")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()