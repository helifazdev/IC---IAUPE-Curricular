import customtkinter as ctk
from tkinter import messagebox

def criar_formulario(root, analises, candidato_atual):
    row = 3
    widgets = {}
    
    def atualizar_justificativas(*args):
        for just_widget in justificativas_widgets:
            just_widget.pack_forget()
        if widgets["Análise curricular"].get() == "Não Possui":
            for just_widget in justificativas_widgets:
                just_widget.pack(anchor="w")


    for nome, detalhes in analises.items():
        label = ctk.CTkLabel(root, text=nome)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        if detalhes["tipo"] == "sim_nao":
            frame = ctk.CTkFrame(root)
            frame.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            selected_option = ctk.StringVar(value=candidato_atual.get(nome, ""))
            for opcao in detalhes["opcoes"]:
                radiobutton = ctk.CTkRadioButton(
                    frame, text=opcao, variable=selected_option, value=opcao,
                    bg_color="lightgrey"  # Adicionando cor de fundo
                )
                radiobutton.pack(anchor="w")
            widgets[nome] = selected_option

        elif detalhes["tipo"] == "opcoes_multiplas":
            frame = ctk.CTkFrame(root)
            frame.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            selected_option = ctk.StringVar(value=candidato_atual.get(nome, ""))
            for opcao in detalhes["opcoes"]:
                radiobutton = ctk.CTkRadioButton(
                    frame, text=opcao, variable=selected_option, value=opcao,
                    bg_color="lightgrey"  # Adicionando cor de fundo
                )
                radiobutton.pack(anchor="w")
            widgets[nome] = selected_option
            if nome == "Análise curricular":
                selected_option.trace("w", atualizar_justificativas)
                justificativas_widgets = []
                justificativa_var = ctk.StringVar(value=candidato_atual.get("Justificativa", ""))
                for sub_opcao in detalhes["sub_opcoes"]["Não Possui"]:
                    justificativa_radiobutton = ctk.CTkRadioButton(
                        frame, text=sub_opcao, variable=justificativa_var, value=sub_opcao,
                        bg_color="lightgrey"  # Adicionando cor de fundo
                    )
                    justificativas_widgets.append(justificativa_radiobutton)
                widgets["Justificativa"] = justificativa_var

        elif detalhes["tipo"] == "texto_livre":
            text_entry = ctk.CTkEntry(root, width=230, height=70, placeholder_text="Digite uma observação!")
            text_entry.grid(row=row, column=1, padx=10, pady=20, sticky="w")
            text_entry.insert(0, candidato_atual.get(nome, ""))
            widgets[nome] = text_entry

        row += 1

    return widgets

