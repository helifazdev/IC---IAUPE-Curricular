import customtkinter as ctk

def criar_formulario(root, analises):
    row = 3
    for nome, detalhes in analises.items():
        label = ctk.CTkLabel(root, text=nome)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        if detalhes["tipo"] == "sim_nao":
            combobox = ctk.CTkComboBox(root, values=detalhes["opcoes"])
            combobox.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        elif detalhes["tipo"] == "opcoes_multiplas":
            combobox = ctk.CTkComboBox(root, values=detalhes["opcoes"])
            combobox.grid(row=row, column=1, padx=10, pady=5, sticky="w")

            def on_combobox_change(event):
                selected = combobox.get()
                for widget in root.grid_slaves():
                    if int(widget.grid_info()["row"]) > row:
                        widget.grid_forget()

                if "sub_opcoes" in detalhes and selected in detalhes["sub_opcoes"]:
                    sub_combobox = ctk.CTkComboBox(root, values=detalhes["sub_opcoes"][selected])
                    sub_combobox.grid(row=row+1, column=1, padx=10, pady=5, sticky="w")

            combobox.bind("<<ComboboxSelected>>", on_combobox_change)

        elif detalhes["tipo"] == "texto_livre":
            text_entry = ctk.CTkEntry(root)
            text_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        row += 1

