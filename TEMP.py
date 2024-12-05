import customtkinter as ctk
from Criar_Form import criar_formulario

# Função para atualizar o formulário com os dados do candidato atual
def atualizar_formulario():
    global indice_atual, candidatos, analises, widgets
    candidato_atual = candidatos[indice_atual]
    label_candidato.config(text=f"Candidato {indice_atual + 1}")

    for nome, widget in widgets.items():
        if isinstance(widget, ctk.StringVar):
            widget.set(candidato_atual.get(nome, ""))
        else:
            widget.delete(0, ctk.END)
            widget.insert(0, candidato_atual.get(nome, ""))

# Função para salvar os dados do formulário atual no candidato atual
def salvar_formulario():
    global indice_atual, candidatos, widgets
    candidato_atual = candidatos[indice_atual]
    for nome, widget in widgets.items():
        if isinstance(widget, ctk.StringVar):
            candidato_atual[nome] = widget.get()
        else:
            candidato_atual[nome] = widget.get()

# Função para avançar para o próximo candidato
def proximo():
    global indice_atual
    salvar_formulario()
    if indice_atual < len(candidatos) - 1:
        indice_atual += 1
        atualizar_formulario()

# Função para voltar ao candidato anterior
def anterior():
    global indice_atual
    salvar_formulario()
    if indice_atual > 0:
        indice_atual -= 1
        atualizar_formulario()

# Configuração inicial
indice_atual = 0
candidatos = [
    {"Requisitos": "Sim", "Análise curricular": "Mestrado", "Observação": "Nada a observar"},
    {"Requisitos": "Não", "Análise curricular": "Doutorado", "Observação": "Precisa revisar"}
]
analises = {
    "Requisitos": {"tipo": "sim_nao", "opcoes": ["Sim", "Não"]},
    "Análise curricular": {"tipo": "opcoes_multiplas", "opcoes": ["Especialização", "Mestrado", "Doutorado", "Não Possui"]},
    "Observação": {"tipo": "texto_livre"}
}

# Configuração da interface gráfica
root = ctk.CTk()
label_candidato = ctk.CTkLabel(root, text="")
label_candidato.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

widgets = criar_formulario(root, analises, candidatos[indice_atual])

# Botões de navegação
anterior_button = ctk.CTkButton(root, text="Anterior", command=anterior)
anterior_button.grid(row=15, column=0, padx=5, pady=5)

proximo_button = ctk.CTkButton(root, text="Próximo", command=proximo)
proximo_button.grid(row=15, column=1, padx=5, pady=5)

atualizar_formulario()  # Atualiza o formulário com o primeiro candidato

root.mainloop()
