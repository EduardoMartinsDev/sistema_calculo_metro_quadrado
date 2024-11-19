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
    tree.insert("", "end", values=("Total", "", f"R$ {total:.2f}"), tags=("soma",))
    label_total_consolidado.config(text=f"Total Consolidado: R$ {total:.2f}")

app = tk.Tk()
app.title("Calculadora de Rateio por m²")

# Dimensões da janela
largura_janela = 600
altura_janela = 900

# Obter as dimensões da tela
largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()

# Calcular a posição central
posicao_x = (largura_tela // 2) - (largura_janela // 2)
posicao_y = (altura_tela // 2) - (altura_janela // 2)

# Configurar a geometria da janela para centralizar
app.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
app.configure(bg="#1e1e1e")

# Configuração do canvas para permitir rolagem
canvas = tk.Canvas(app, bg="#1e1e1e", highlightthickness=0, width=800)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Frame central com conteúdo
scrollable_frame = tk.Frame(canvas, bg="#1e1e1e", width=760)
canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

# Ajuste de redimensionamento do canvas conforme conteúdo
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Campos de entrada centralizados
label_descricao = tk.Label(scrollable_frame, text="Descrição do Rateio:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_descricao.pack(pady=10, anchor="center")
entry_descricao = tk.Entry(scrollable_frame, bg="#3c3c3c", fg="#C0C0C0", insertbackground="#C0C0C0", font=("Arial", 12), width=40)
entry_descricao.pack(pady=10, anchor="center")

label_total_m2 = tk.Label(scrollable_frame, text="Metragem Quadrada Total:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_total_m2.pack(pady=10, anchor="center")
entry_total_m2 = tk.Entry(scrollable_frame, bg="#3c3c3c", fg="#C0C0C0", insertbackground="#C0C0C0", font=("Arial", 12), width=40)
entry_total_m2.pack(pady=10, anchor="center")

label_valor_total = tk.Label(scrollable_frame, text="Valor Total da Conta:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_valor_total.pack(pady=10, anchor="center")
entry_valor_total = tk.Entry(scrollable_frame, bg="#3c3c3c", fg="#C0C0C0", insertbackground="#C0C0C0", font=("Arial", 12), width=40)
entry_valor_total.pack(pady=10, anchor="center")

label_m2_individual = tk.Label(scrollable_frame, text="Metragem Individual:", bg="#1e1e1e", fg="#e0e0e0", font=("Arial", 12))
label_m2_individual.pack(pady=10, anchor="center")
entry_m2_individual = tk.Entry(scrollable_frame, bg="#3c3c3c", fg="#C0C0C0", insertbackground="#C0C0C0", font=("Arial", 12), width=40)
entry_m2_individual.pack(pady=10, anchor="center")

botao_calcular = tk.Button(scrollable_frame, text="Calcular Rateio", command=calcular_rateio, bg="#3a3a3a", fg="#C0C0C0", font=("Arial", 12), width=20)
botao_calcular.pack(pady=15, anchor="center")

label_resultado = tk.Label(scrollable_frame, text="Valor do rateio: R$ 0.00", bg="#1e1e1e", fg="#b0b0b0", font=("Arial", 12, "bold"))
label_resultado.pack(pady=15, anchor="center")

# Tabela centralizada
frame_tabela = tk.Frame(scrollable_frame, bg="#2a2a2a")
frame_tabela.pack(pady=15, anchor="center")
tree = ttk.Treeview(frame_tabela, columns=("Descrição", "Metragem Individual", "Valor do Rateio"), show="headings", height=8)
tree.heading("Descrição", text="Descrição")
tree.heading("Metragem Individual", text="Metragem Individual (m²)")
tree.heading("Valor do Rateio", text="Valor do Rateio (R$)")
tree.column("Descrição", anchor="center", width=200)
tree.column("Metragem Individual", anchor="center", width=200)
tree.column("Valor do Rateio", anchor="center", width=200)
tree.tag_configure("rateio", background="#e6e6e6", font=("Arial", 11))
tree.tag_configure("soma", background="#f1c40f", font=("Arial", 12, "bold"))
tree.pack()

# Total consolidado centralizado
label_total_consolidado = tk.Label(scrollable_frame, text="Total Consolidado: R$ 0.00", font=("Arial", 16, "bold"), bg="#2a2a2a", fg="#f1c40f")
label_total_consolidado.pack(pady=20, fill="x", anchor="center")

# Botão Consolidar Rateios centralizado
botao_consolidar = tk.Button(scrollable_frame, text="Consolidar Rateios", command=consolidar_rateios, bg="#3a3a3a", fg="#C0C0C0", font=("Arial", 12), width=20)
botao_consolidar.pack(pady=25, anchor="center")

app.mainloop()
