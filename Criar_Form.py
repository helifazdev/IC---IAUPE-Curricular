import customtkinter as ctk

def criar_formulario(root, analises, candidato_atual):
    row = 3
    widgets = {}

    for nome, detalhes in analises.items():
        label = ctk.CTkLabel(root, text=nome)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        if detalhes["tipo"] == "sim_nao":
            frame = ctk.CTkFrame(root)
            frame.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            
            selected_option = ctk.StringVar(value=candidato_atual.get(nome, ""))
            for opcao in detalhes["opcoes"]:
                radiobutton = ctk.CTkRadioButton(
                    frame, text=opcao, variable=selected_option, value=opcao
                )
                radiobutton.pack(anchor="w")
            widgets[nome] = selected_option

        elif detalhes["tipo"] == "opcoes_multiplas":
            frame = ctk.CTkFrame(root)
            frame.grid(row=row, column=1, padx=10, pady=5, sticky="w")

            selected_option = ctk.StringVar(value=candidato_atual.get(nome, ""))
            for opcao in detalhes["opcoes"]:
                radiobutton = ctk.CTkRadioButton(
                    frame, text=opcao, variable=selected_option, value=opcao
                )
                radiobutton.pack(anchor="w")
            widgets[nome] = selected_option

        elif detalhes["tipo"] == "texto_livre":
            text_entry = ctk.CTkEntry(root, width=230, height=70, placeholder_text="Digite uma observação!")
            text_entry.grid(row=row, column=1, padx=10, pady=20, sticky="w")
            text_entry.insert(0, candidato_atual.get(nome, ""))
            widgets[nome] = text_entry
        
        row += 1

    return widgets

