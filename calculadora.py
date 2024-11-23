import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

rateios = []

def calcular_rateio():
    try:
        descricao = entry_descricao.get()
        total_m2 = float(entry_total_m2.get())
        valor_total = float(entry_valor_total.get())
        m2_individual = float(entry_m2_individual.get())

        if not descricao:
            messagebox.showerror("Erro", "Por favor, insira uma descrição para o rateio.")
            return

        valor_rateio = (valor_total / total_m2) * m2_individual

        rateios.append({"Descrição": descricao, "Metragem Individual": m2_individual, "Valor do Rateio": valor_rateio})
        tree.insert("", "end", values=(descricao, m2_individual, f"R$ {valor_rateio:.2f}"), tags=("rateio",))

        entry_descricao.delete(0, tk.END)
        entry_total_m2.delete(0, tk.END)
        entry_valor_total.delete(0, tk.END)
        entry_m2_individual.delete(0, tk.END)
        label_resultado.config(text="Valor do rateio: R$ 0.00")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

def consolidar_rateios():
    total = sum(item["Valor do Rateio"] for item in rateios)
    label_total_consolidado.config(text=f"Total Consolidado: R$ {total:.2f}")

def apagar_linha_selecionada():
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, "values")

        # Encontrar e remover o item correspondente no dicionário de rateios
        for rateio in rateios:
            if (rateio["Descrição"] == values[0] and
                rateio["Metragem Individual"] == float(values[1]) and
                f"R$ {rateio['Valor do Rateio']:.2f}" == values[2]):
                rateios.remove(rateio)
                break

        # Remover a linha da tabela
        tree.delete(selected_item)

        # Atualizar o total consolidado
        consolidar_rateios()
    except IndexError:
        messagebox.showerror("Erro", "Por favor, selecione uma linha para apagar.")

def reiniciar_calculos():
    # Limpar todos os campos de entrada
    entry_descricao.delete(0, tk.END)
    entry_total_m2.delete(0, tk.END)
    entry_valor_total.delete(0, tk.END)
    entry_m2_individual.delete(0, tk.END)

    # Limpar a tabela
    for item in tree.get_children():
        tree.delete(item)

    # Limpar a lista de rateios e o total consolidado
    rateios.clear()
    label_total_consolidado.config(text="Total Consolidado: R$ 0.00")
    label_resultado.config(text="Valor do rateio: R$ 0.00")

app = tk.Tk()
app.title("Calculadora de Rateio por m²")

# Dimensões da janela
largura_janela = 800
altura_janela = 600

# Obter as dimensões da tela
largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()

# Calcular a posição central
posicao_x = (largura_tela // 2) - (largura_janela // 2)
posicao_y = (altura_tela // 2) - (altura_janela // 2)

# Configurar a geometria da janela para centralizar
app.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
app.configure(bg="#1e1e1e")

# Frame principal
frame_principal = tk.Frame(app, bg="#1e1e1e")
frame_principal.pack(fill="both", expand=True)

# Campos de entrada
label_descricao = tk.Label(frame_principal, text="Descrição do Rateio:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_descricao.pack(pady=5)
entry_descricao = tk.Entry(frame_principal, bg="#3c3c3c", fg="#C0C0C0", font=("Arial", 12), width=40)
entry_descricao.pack(pady=5)

label_total_m2 = tk.Label(frame_principal, text="Metragem Quadrada Total:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_total_m2.pack(pady=5)
entry_total_m2 = tk.Entry(frame_principal, bg="#3c3c3c", fg="#C0C0C0", font=("Arial", 12), width=40)
entry_total_m2.pack(pady=5)

label_valor_total = tk.Label(frame_principal, text="Valor Total da Conta:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_valor_total.pack(pady=5)
entry_valor_total = tk.Entry(frame_principal, bg="#3c3c3c", fg="#C0C0C0", font=("Arial", 12), width=40)
entry_valor_total.pack(pady=5)

label_m2_individual = tk.Label(frame_principal, text="Metragem Individual:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_m2_individual.pack(pady=5)
entry_m2_individual = tk.Entry(frame_principal, bg="#3c3c3c", fg="#C0C0C0", font=("Arial", 12), width=40)
entry_m2_individual.pack(pady=5)

botao_calcular = tk.Button(frame_principal, text="Calcular Rateio", command=calcular_rateio, bg="#3a3a3a", fg="#C0C0C0", font=("Arial", 12))
botao_calcular.pack(pady=10)

label_resultado = tk.Label(frame_principal, text="Valor do rateio: R$ 0.00", bg="#1e1e1e", fg="#b0b0b0", font=("Arial", 12, "bold"))
label_resultado.pack(pady=10)

# Tabela
frame_tabela = tk.Frame(frame_principal, bg="#2a2a2a")
frame_tabela.pack(pady=10)
tree = ttk.Treeview(frame_tabela, columns=("Descrição", "Metragem Individual", "Valor do Rateio"), show="headings", height=8)
tree.heading("Descrição", text="Descrição")
tree.heading("Metragem Individual", text="Metragem Individual (m²)")
tree.heading("Valor do Rateio", text="Valor do Rateio (R$)")
tree.column("Descrição", anchor="center", width=200)
tree.column("Metragem Individual", anchor="center", width=200)
tree.column("Valor do Rateio", anchor="center", width=200)
tree.pack()

# Botões extras
frame_botoes = tk.Frame(frame_principal, bg="#1e1e1e")
frame_botoes.pack(pady=10)

botao_apagar_linha = tk.Button(frame_botoes, text="Apagar Linha Selecionada", command=apagar_linha_selecionada, bg="#3a3a3a", fg="#C0C0C0", font=("Arial", 12))
botao_apagar_linha.grid(row=0, column=0, padx=10)

botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar Cálculos", command=reiniciar_calculos, bg="#3a3a3a", fg="#C0C0C0", font=("Arial", 12))
botao_reiniciar.grid(row=0, column=1, padx=10)

label_total_consolidado = tk.Label(frame_principal, text="Total Consolidado: R$ 0.00", font=("Arial", 16, "bold"), bg="#2a2a2a", fg="#f1c40f")
label_total_consolidado.pack(pady=10)

botao_consolidar = tk.Button(frame_principal, text="Consolidar Rateios", command=consolidar_rateios, bg="#3a3a3a", fg="#C0C0C0", font=("Arial", 12))
botao_consolidar.pack(pady=10)

app.mainloop()
