import customtkinter as ctk

# Configurar o tema global do customtkinter
ctk.set_appearance_mode("system")  # Light, Dark, ou System (segue as configurações do sistema)
ctk.set_default_color_theme("dark-blue")  # Outras opções: "green", "dark-blue"

# Função para criar um formulário de exemplo
def criar_formulario(root):
    frame = ctk.CTkFrame(root)
    frame.pack(padx=20, pady=20)

    # Exemplo de opções sem fundo cinza
    selected_option = ctk.StringVar(value="")

    for opcao in ["Opção 1", "Opção 2", "Opção 3"]:
        radiobutton = ctk.CTkRadioButton(frame, text=opcao, variable=selected_option, value=opcao)
        radiobutton.pack(anchor="w")

# Configurar a janela principal
root = ctk.CTk()
root.title("Exemplo de Formulário")
root.geometry("300x200")

# Criar o formulário
criar_formulario(root)

# Iniciar o loop principal da interface gráfica
root.mainloop()
