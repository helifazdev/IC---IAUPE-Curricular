import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
from Criar_Form import criar_formulario
from informacoes import obter_candidatos

# Tela de entrada
def criar_tela_entrada():
    root = ctk.CTk()
    root.title("IAUPE Curricular")
    root.geometry("600x450")  # Define o tamanho da janela

    # Centralizar os elementos na tela
    canvas = ctk.CTkCanvas(root, width=600, height=400, bg="#f0f0f0")
    canvas.pack()

    # Configurar a tela para sempre abrir em tela cheia
    root.state('zoomed')

    # Função para redimensionar a imagem
    def resize_image(image_path, width, height):
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    # Dimensões desejadas (largura e altura)
    desired_width = 500  
    desired_height = 200  

    # Redimensionar a imagem
    logo_image = resize_image("IAUPE_Concursos.png", desired_width, desired_height)

    # Adicionar o logo usando CTkLabel
    logo_label = ctk.CTkLabel(root, image=logo_image, text="")
    logo_label.image = logo_image  # Manter uma referência da imagem
    logo_label.place(relx=0.5, rely=0.3, anchor="center")


    # Adicionar o nome da empresa
    canvas.create_text(300, 300, text="IAUPE CONCURSOS", font=("Arial", 24, "bold"), fill="blue")

    # Adicionar o nome do processo
    canvas.create_text(300, 350, text="Análise Curricular - UPE 2025", font=("Arial", 24, "bold"), fill="red")

    # Definindo o ícone da janela
    root.iconbitmap("icone_IAUPE.ico")

    # Agendar a troca de tela após 5 segundos
    root.after(3000, lambda: abrir_proxima_tela(root))
    root.mainloop()

# Função para fechar a tela de entrada e abrir a próxima
def abrir_proxima_tela(root):
    root.destroy()  # Fecha a tela de entrada

# Chama a função para criar a tela de entrada
criar_tela_entrada()

# Variáveis globais e inicialização dos candidatos
candidatos = obter_candidatos()
indice_atual = 0

total_candidatos = len(candidatos)
data_hoje = datetime.now().strftime("%d/%m/%Y")
# Tipo de ordenação
candidatos.sort(key=lambda x: (x["nome"], x["cargo"]))

# Função para atualizar o formulário com os dados do candidato atual
def atualizar_formulario():
    global indice_atual, widgets
    if 0 <= indice_atual < total_candidatos:
        candidato = candidatos[indice_atual]
        # Dados pessoais do candidato
        nome_var.set(candidato.get("nome", ""))
        numero_var.set(candidato.get("inscricao", ""))
        cargo_var.set(candidato.get("cargo", ""))

        for nome, widget in widgets.items():
            if isinstance(widget, ctk.StringVar):
                widget.set(candidato.get(nome, ""))
            else:
                widget.delete(0, ctk.END)
                widget.insert(0, candidato.get(nome, ""))

# Função para salvar os dados do formulário atual no candidato atual
def salvar_formulario():
    global indice_atual, widgets
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

root = ctk.CTk()
root.title("Análise Curricular - UPE 2025")
root.geometry("400x450")

# Campos fixos como referências
ctk.CTkLabel(root, text="Nome do candidato:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
nome_var = ctk.StringVar()
nome_entry = ctk.CTkLabel(root, textvariable=nome_var)
nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

ctk.CTkLabel(root, text="Número de inscrição:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
numero_var = ctk.StringVar()
numero_entry = ctk.CTkLabel(root, textvariable=numero_var)
numero_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

ctk.CTkLabel(root, text="Cargo/Função:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
cargo_var = ctk.StringVar()
cargo_entry = ctk.CTkLabel(root, textvariable=cargo_var)
cargo_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

analises = {
     "Requisitos": {"tipo": "sim_nao", "opcoes": ["Sim", "Não"]},
     "Análise curricular": {"tipo": "opcoes_multiplas", "opcoes": ["Especialização", "Mestrado","Doutorado", "Não Possui"], "sub_opcoes": {"Não Possui": ["Documento Inválido", "Documento Ilegível" ,"Documento não enviado" ]}},
     "Observação": {"tipo": "texto_livre"}
}

# Inicializando o formulário com o primeiro candidato
widgets = criar_formulario(root, analises, candidatos[indice_atual])

# Botões de navegação
anterior_button = ctk.CTkButton(root, text="Anterior", command=anterior)
anterior_button.grid(row=15, column=0, padx=0, pady=0)

proximo_button = ctk.CTkButton(root, text="Próximo", command=proximo)
proximo_button.grid(row=15, column=1, padx=0, pady=0)

# Alterar ícone da janela
root.iconbitmap("Upe.ico")  # Substitua pelo caminho do seu ícone

# Configuração inicial
indice_atual = 0 
atualizar_formulario()

root.mainloop()
