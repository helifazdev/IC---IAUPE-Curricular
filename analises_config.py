# analises_config.py
analises = {
    "Requisito": {
        "tipo": "sim_nao",
        "opcoes": ["Sim", "Não"]
    },
    "Avaliação Curricular": {
        "tipo": "opcoes_multiplas",
        "opcoes": ["Especialização", "Mestrado", "Doutorado", "Não possui"],
        "sub_opcoes": {
            "Não possui": ["Não enviou Documentação", "Documento ilegível", "Documentação inválida"]
        }
    },
    "Observação": {
        "tipo": "texto_livre",
        "placeholder": "Adicione comentários aqui"
    }
}
