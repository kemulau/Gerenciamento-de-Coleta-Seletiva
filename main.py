import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from datetime import datetime


class Residuo:
    tipos_validos = ["Plástico", "Vidro", "Metal", "Papel"]

    def __init__(self, tipo, quantidade, data):
        self.tipo = tipo
        self.quantidade = quantidade
        self.data = data

    @staticmethod
    def validar_tipo(tipo):
        return tipo in Residuo.tipos_validos


class Cooperativa:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco


class Historico:
    def __init__(self):
        self.lista_residuos = []
        self.lista_cooperativas = []
        self.lista_agendamentos = []

    def adicionar_residuo(self, residuo):
        self.lista_residuos.append(residuo)

    def listar_residuos(self):
        return [(r.tipo, r.quantidade, r.data) for r in self.lista_residuos]

    def adicionar_cooperativa(self, cooperativa):
        self.lista_cooperativas.append(cooperativa)

    def listar_cooperativas(self):
        return [(c.nome, c.endereco) for c in self.lista_cooperativas]

    def agendar_coleta(self, cooperativa, data):
        self.lista_agendamentos.append((cooperativa, data))

    def listar_agendamentos(self):
        return [(a[0].nome, a[0].endereco, a[1]) for a in self.lista_agendamentos]


# Funções da Interface
def registrar_residuo():
    tipo = tipo_var.get()
    try:
        quantidade = float(entry_quantidade.get())
    except ValueError:
        messagebox.showerror("❌ Erro", "Quantidade inválida.")
        return

    if Residuo.validar_tipo(tipo):
        # Formata a data para o formato brasileiro (DD/MM/AAAA HH:MM:SS)
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        novo_residuo = Residuo(tipo, quantidade, data)
        historico.adicionar_residuo(novo_residuo)
        atualizar_lista_residuos()
        messagebox.showinfo("✅ Sucesso", "Resíduo registrado com sucesso!")
    else:
        messagebox.showerror("❌ Erro", "Tipo de resíduo inválido.")


def atualizar_lista_residuos():
    lista_residuos.delete(0, tk.END)
    for tipo, quantidade, data in historico.listar_residuos():
        lista_residuos.insert(tk.END, f"{data} - {tipo}: {quantidade} kg")


def cadastrar_cooperativa():
    nome = entry_nome_cooperativa.get()
    endereco = entry_endereco_cooperativa.get()
    if nome and endereco:
        nova_cooperativa = Cooperativa(nome, endereco)
        historico.adicionar_cooperativa(nova_cooperativa)
        atualizar_lista_cooperativas()
        atualizar_dropdown_cooperativas()
        messagebox.showinfo("✅ Sucesso", "Cooperativa cadastrada com sucesso!")
    else:
        messagebox.showerror("❌ Erro", "Preencha todos os campos.")


def atualizar_lista_cooperativas():
    lista_cooperativas.delete(0, tk.END)
    for nome, endereco in historico.listar_cooperativas():
        lista_cooperativas.insert(tk.END, f"{nome} - {endereco}")


def atualizar_dropdown_cooperativas():
    cooperativa_var.set("")
    menu_cooperativas['menu'].delete(0, 'end')
    for nome, _ in historico.listar_cooperativas():
        menu_cooperativas['menu'].add_command(label=nome, command=tk._setit(cooperativa_var, nome))


def agendar_coleta():
    cooperativa_nome = cooperativa_var.get()
    data = calendar.get_date()

    if not cooperativa_nome:
        messagebox.showerror("❌ Erro", "Selecione uma cooperativa para agendar.")
        return

    cooperativa = next((c for c in historico.lista_cooperativas if c.nome == cooperativa_nome), None)
    if cooperativa:
        historico.agendar_coleta(cooperativa, data)
        atualizar_lista_agendamentos()
        messagebox.showinfo("✅ Sucesso", "Coleta agendada com sucesso!")


def atualizar_lista_agendamentos():
    lista_agendamentos.delete(0, tk.END)
    for nome, endereco, data in historico.listar_agendamentos():
        lista_agendamentos.insert(tk.END, f"{data} - {nome}: {endereco}")


def gerar_relatorio_residuos():
    totais = {tipo: 0 for tipo in Residuo.tipos_validos}
    for residuo in historico.lista_residuos:
        totais[residuo.tipo] += residuo.quantidade

    if not any(totais.values()):
        messagebox.showerror("❌ Erro", "Não há resíduos registrados para gerar o relatório.")
        return

    tipos = list(totais.keys())
    quantidades = list(totais.values())
    cores = ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f']

    plt.figure(figsize=(10, 6))
    barras = plt.bar(tipos, quantidades, color=cores, edgecolor='black', linewidth=1.5)

    for barra in barras:
        plt.text(barra.get_x() + barra.get_width() / 2,
                 barra.get_height() + 0.5,
                 f"{barra.get_height():.2f} kg",
                 ha='center', fontsize=10)

    plt.title("Distribuição de Resíduos Coletados", fontsize=16, fontweight='bold')
    plt.xlabel("Tipo de Resíduo", fontsize=14)
    plt.ylabel("Quantidade (kg)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


# Configuração da Interface Gráfica
historico = Historico()
janela = tk.Tk()
janela.title("Gerenciamento de Coleta Seletiva ♻️")

# Criação do Notebook (abas)
notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True)

# Aba: Resíduos
aba_residuos = ttk.Frame(notebook)
notebook.add(aba_residuos, text="Resíduos")

tk.Label(aba_residuos, text="Tipo de Resíduo:").grid(row=0, column=0, padx=10, pady=5)
tipo_var = tk.StringVar(value="Plástico")
tk.OptionMenu(aba_residuos, tipo_var, *Residuo.tipos_validos).grid(row=0, column=1, padx=10, pady=5)

tk.Label(aba_residuos, text="Quantidade (kg):").grid(row=1, column=0, padx=10, pady=5)
entry_quantidade = tk.Entry(aba_residuos)
entry_quantidade.grid(row=1, column=1, padx=10, pady=5)

tk.Button(aba_residuos, text="Registrar Resíduo 📝", command=registrar_residuo).grid(row=2, columnspan=2, pady=10)

tk.Label(aba_residuos, text="Histórico de Resíduos:").grid(row=3, column=0, columnspan=2)
lista_residuos = tk.Listbox(aba_residuos, width=50, height=10)
lista_residuos.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

tk.Button(aba_residuos, text="Gerar Relatório 📊", command=gerar_relatorio_residuos).grid(row=5, columnspan=2, pady=10)

# Aba: Cooperativas
aba_cooperativas = ttk.Frame(notebook)
notebook.add(aba_cooperativas, text="Cooperativas")

tk.Label(aba_cooperativas, text="Nome da Cooperativa:").grid(row=0, column=0, padx=10, pady=5)
entry_nome_cooperativa = tk.Entry(aba_cooperativas)
entry_nome_cooperativa.grid(row=0, column=1, padx=10, pady=5)

tk.Label(aba_cooperativas, text="Endereço da Cooperativa:").grid(row=1, column=0, padx=10, pady=5)
entry_endereco_cooperativa = tk.Entry(aba_cooperativas)
entry_endereco_cooperativa.grid(row=1, column=1, padx=10, pady=5)

tk.Button(aba_cooperativas, text="Cadastrar Cooperativa 🏢", command=cadastrar_cooperativa).grid(row=2, columnspan=2, pady=10)

tk.Label(aba_cooperativas, text="Cooperativas Cadastradas:").grid(row=3, column=0, columnspan=2)
lista_cooperativas = tk.Listbox(aba_cooperativas, width=50, height=10)
lista_cooperativas.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Aba: Agendamentos
aba_agendamentos = ttk.Frame(notebook)
notebook.add(aba_agendamentos, text="Agendamentos")

tk.Label(aba_agendamentos, text="Selecione a Cooperativa:").grid(row=0, column=0, padx=10, pady=5)
cooperativa_var = tk.StringVar()
menu_cooperativas = tk.OptionMenu(aba_agendamentos, cooperativa_var, "")
menu_cooperativas.grid(row=0, column=1, padx=10, pady=5)

tk.Label(aba_agendamentos, text="Selecione a Data:").grid(row=1, column=0, padx=10, pady=5)
calendar = Calendar(
    aba_agendamentos,
    selectmode="day",
    date_pattern="dd/mm/yyyy",
    locale="pt_BR"
)
calendar.grid(row=1, column=1, padx=10, pady=5)

tk.Button(aba_agendamentos, text="Agendar Coleta 📅", command=agendar_coleta).grid(row=2, columnspan=2, pady=10)

tk.Label(aba_agendamentos, text="Agendamentos:").grid(row=3, column=0, columnspan=2)
lista_agendamentos = tk.Listbox(aba_agendamentos, width=50, height=10)
lista_agendamentos.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Inicia a interface gráfica
janela.mainloop()
