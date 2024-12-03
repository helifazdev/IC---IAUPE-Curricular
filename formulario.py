import customtkinter as ctk
from tkinter import messagebox
from informacoes import obter_candidatos
from processamento import salvar_informacoes
from datetime import datetime
from PIL import Image, ImageTk
from analises_config import analises
from Criar_Form import criar_formulario

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
pontuacoes = {"Especializacao": 40, "Mestrado": 60, "Doutorado": 10, "Nao possui": 0}
total_candidatos = len(candidatos)
data_hoje = datetime.now().strftime("%d/%m/%Y")
# Tipo de ordenação
candidatos.sort(key=lambda x: (x["nome"], x["cargo"]))

# Função para atualizar o formulário com os dados do candidato atual
def atualizar_formulario():
    global indice_atual
    if 0 <= indice_atual < total_candidatos:
        candidato = candidatos[indice_atual]

        # Dados pessoais do candidato
        nome_var.set(candidato.get("nome", ""))
        numero_var.set(candidato.get("inscricao", ""))
        cargo_var.set(candidato.get("cargo", ""))

        # Dados a serem analisados
        requisito_var.set(candidato.get("requisito", ""))
        avaliacao_var.set(candidato.get("avaliacao", ""))
        observacoes_text.delete("1.0", ctk.END)
        observacoes_text.insert(ctk.END, candidato.get("observacao", ""))

        justificar_frame.grid_remove()
        rodape_var.set(f"Candidato {indice_atual + 1} de {total_candidatos} | Data: {data_hoje}")

        if candidato.get("avaliacao") == "Nao possui":
            exibir_justificativa("Nao possui")
            justificativa_var.set(candidato.get("justificativa", ""))
    else:
        messagebox.showinfo("Fim", "Todos os candidatos foram analisados.")
        root.quit()

# Função para salvar as informações dos candidatos
def salvar_candidato_atual():
    global indice_atual
    candidato = candidatos[indice_atual]
    candidato["requisito"] = requisito_var.get()
    candidato["avaliacao"] = avaliacao_var.get()
    candidato["observacao"] = observacoes_text.get("1.0", ctk.END).strip()
    candidato["justificativa"] = justificativa_var.get() if avaliacao_var.get() == "Nao possui" else ""

# Função para validar o formulário
def validar_formulario():
    if not requisito_var.get():
        messagebox.showerror("Erro", "Por favor, selecione se o candidato possui requisitos para o cargo.")
        return False
    if not avaliacao_var.get():
        messagebox.showerror("Erro", "Por favor, selecione a avaliação curricular.")
        return False
    if avaliacao_var.get() == "Nao possui" and not justificativa_var.get():
        messagebox.showerror("Erro", "Por favor, forneça uma justificativa para a avaliação 'Não possui'.")
        return False
    return True

# Função para avançar para o próximo candidato
def proximo():
    global indice_atual
    if validar_formulario():
        salvar_candidato_atual()
        if requisito_var.get() == "Nao":
            messagebox.showinfo("Eliminado", "Esse candidato já está eliminado de acordo com item 5.2.6 do Edital, mas vamos continuar a análise!")
        if indice_atual < len(candidatos) - 1:
            indice_atual += 1
            atualizar_formulario()
        else:
            finalizar_analise()

# Função para voltar ao candidato anterior
def anterior():
    global indice_atual
    salvar_candidato_atual()
    if indice_atual > 0:
        indice_atual -= 1
        atualizar_formulario()

# Função para finalizar a análise
def finalizar_analise():
    # Exibir mensagem de conclusão
    messagebox.showinfo("Concluído", "Análise finalizada. Todas as informações foram salvas.")

    # Chamar função para processar e salvar informações
    for i, candidato in enumerate(candidatos):
        salvar_informacoes(
            i + 1,
            candidato.get("nome"),
            candidato.get("inscricao"),
            candidato.get("cargo"),
            candidato.get("requisito"),
            candidato.get("avaliacao"),
            candidato.get("justificativa", ""),
            candidato.get("observacao", ""),
            pontuacoes.get(candidato.get("avaliacao"), 0)
        )

    root.quit()

# Criando a janela principal
root = ctk.CTk()
root.title("IAUPE CONCURSOS - Análise curricular UPE 2025")

# Ajustar o tamanho da letra
root.option_add("*Font", "Helvetica")

# Configurar a tela para sempre abrir em tela cheia
root.state('zoomed')

# Criando o rodapé
rodape_var = ctk.StringVar()
rodape_label = ctk.CTkLabel(root, textvariable=rodape_var)
rodape_label.grid(row=20, columnspan=2, padx=10, pady=5)

# Definindo o ícone da janela
root.iconbitmap("Upe.ico")

# Dados pessoais do candidato
# Criando e posicionando os widgets
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

ctk.CTkLabel(root, text="Possui Requisitos para o cargo:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
requisito_var = ctk.StringVar()  # Variável sem valor padrão
ctk.CTkRadioButton(root, text="Sim", variable=requisito_var, value="Sim", command=lambda:
                   exibir_justificativa(requisito_var.get())).grid(row=3, column=1, padx=2, pady=0, sticky="w")
ctk.CTkRadioButton(root, text="Nao", variable=requisito_var, value="Nao", command=lambda:
                   exibir_justificativa(requisito_var.get())).grid(row=3, column=1, padx=(60, 0), pady=0, sticky="w")

ctk.CTkLabel(root, text="Avaliação curricular:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
avaliacao_var = ctk.StringVar()  # Variável sem valor padrão
avaliacoes = ["Especializacao", "Mestrado", "Doutorado", "Nao possui"]
for idx, val in enumerate(avaliacoes):
    ctk.CTkRadioButton(root, text=val, variable=avaliacao_var, value=val, command=lambda:
             exibir_justificativa(avaliacao_var.get())).grid(row=8 + idx, column=1, padx=10, pady=5, sticky="w")



# Função para exibir justificativas se necessário
def exibir_justificativa(avaliacao):
    if avaliacao == "Nao possui":
        justificar_frame.grid(row=12, column=1, padx=10, pady=5, sticky="w")
        justificativas = ["Nao enviou documentacao", "Documentacao ilegivel", "Documentacao invalida"]
        for widget in justificar_frame.winfo_children():
            widget.destroy()
        for idx, val in enumerate(justificativas):
            ctk.CTkRadioButton(justificar_frame, text=val, variable=justificativa_var, value=val).pack(anchor='w')
    else:
        justificativa_var.set("")
        justificar_frame.grid_remove()


ctk.CTkLabel(root, text="Observações:").grid(row=14, column=0, padx=10, pady=5)
observacoes_text = ctk.CTkTextbox(root, height=100, width=200)
observacoes_text.grid(row=14, column=1, padx=10, pady=5)

justificativa_var = ctk.StringVar()
justificar_frame = ctk.CTkFrame(root, fg_color="transparent")
justificar_frame.grid(row=10, column=1, padx=10, pady=5, sticky="w")
ctk.CTkLabel(root, text="").grid(row=10, column=0, padx=10, pady=5)

# Botões de navegação
anterior_button = ctk.CTkButton(root, text="Anterior", command=anterior)
anterior_button.grid(row=15, column=0, padx=0, pady=0)

proximo_button = ctk.CTkButton(root, text="Próximo", command=proximo)
proximo_button.grid(row=15, column=1, padx=0, pady=0)

# Inicializando o formulário com o primeiro candidato
atualizar_formulario()

# Iniciando o loop principal
root.mainloop()

