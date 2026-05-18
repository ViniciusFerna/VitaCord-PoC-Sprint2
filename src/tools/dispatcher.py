import json
from src.tools.definitions import tools
from src.tools.mocks import (
    consultar_historico_paciente,
    verificar_interacoes_medicamentosas,
    agendar_teleconsulta)

def executar_tool(nome: str, argumentos: dict) -> str:
    funcoes = {
        "consultar_historico_paciente": consultar_historico_paciente,
        "verificar_interacoes_medicamentosas": verificar_interacoes_medicamentosas,
        "agendar_teleconsulta": agendar_teleconsulta
    }
    if nome not in funcoes:
        return json.dumps({"erro": f"Tool '{nome}' não encontrada."})
    resultado = funcoes[nome](**argumentos)
    return json.dumps(resultado, ensure_ascii=False)


print(f"✅ {len(tools)} tools definidas com mock da paciente Maria.")