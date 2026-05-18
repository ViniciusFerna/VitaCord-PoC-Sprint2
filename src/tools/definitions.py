# Contrato das tools (JSON Schema)
tools = [
    {
        "type": "function",
        "function": {
            "name": "consultar_historico_paciente",
            "description": (
                "Consulta o histórico clínico de um paciente pelo seu ID. "
                "Retorna diagnósticos anteriores, medicamentos em uso e alergias registradas. "
                "Use esta tool sempre que precisar de informações clínicas do paciente."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "paciente_id": {
                        "type": "string",
                        "description": "ID único do paciente no sistema CarePlus"
                    }
                },
                "required": ["paciente_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_interacoes_medicamentosas",
            "description": (
                "Verifica se há interações medicamentosas entre dois ou mais medicamentos. "
                "Use esta tool quando o médico ou o sistema precisar checar compatibilidade entre medicamentos."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "medicamentos": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de medicamentos a verificar"
                    }
                },
                "required": ["medicamentos"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "agendar_teleconsulta",
            "description": (
                "Agenda uma teleconsulta entre o paciente e o médico responsável. "
                "Use esta tool apenas quando o paciente confirmar explicitamente que deseja agendar."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "paciente_id": {
                        "type": "string",
                        "description": "ID único do paciente"
                    },
                    "motivo": {
                        "type": "string",
                        "description": "Motivo da consulta"
                    },
                    "data_preferencial": {
                        "type": "string",
                        "description": "Data preferencial no formato YYYY-MM-DD (opcional)"
                    }
                },
                "required": ["paciente_id", "motivo"]
            }
        }
    }
]