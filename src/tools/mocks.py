# Mocks com dados da paciente Maria
def consultar_historico_paciente(paciente_id: str) -> dict:
    banco_mock = {
        "P001": {
            "paciente_id": "P001",
            "nome": "Maria Silva",
            "idade": 34,
            "diagnosticos": ["Hipertensão arterial (CID I10)"],
            "medicamentos_em_uso": ["Losartana 50mg"],
            "alergias": ["Dipirona"],
            "ultima_consulta": "2026-03-15",
            "medico_responsavel": "Dr. João Oliveira"
        }
    }
    return banco_mock.get(paciente_id, {"erro": "Paciente não encontrado"})


def verificar_interacoes_medicamentosas(medicamentos: list) -> dict:
    interacoes_conhecidas = {
        frozenset(["Losartana", "Ibuprofeno"]): {
            "nivel": "MODERADO",
            "descricao": "AINEs podem reduzir o efeito anti-hipertensivo da Losartana e aumentar risco renal."
        },
        frozenset(["Losartana", "Espironolactona"]): {
            "nivel": "MODERADO",
            "descricao": "Risco de hipercalemia (potássio elevado). Monitorar eletrólitos."
        }
    }
    meds_normalizados = [m.split()[0] for m in medicamentos]
    for par, info in interacoes_conhecidas.items():
        if par.issubset(set(meds_normalizados)):
            return {"interacao_encontrada": True, "detalhes": info}
    return {"interacao_encontrada": False, "mensagem": "Nenhuma interação relevante identificada."}


def agendar_teleconsulta(paciente_id: str, motivo: str, data_preferencial: str = None) -> dict:
    return {
        "agendamento_id": "AGD-2026-0055",
        "paciente_id": paciente_id,
        "medico": "Dr. João Oliveira",
        "motivo": motivo,
        "data_confirmada": data_preferencial,
        "horario": "14:00",
        "modalidade": "Teleconsulta (videochamada)",
        "status": "CONFIRMADO"
    }