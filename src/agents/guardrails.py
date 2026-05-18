import re

# --- RED FLAG DETECTOR ---
# Detecta sintomas de emergência ANTES de passar para o LLM

RED_FLAG_PATTERNS = [
    r"dor.{0,20}peito",
    r"dor.{0,20}torácic",
    r"falta.{0,10}ar",
    r"dificuld.{0,10}respir",
    r"desmai",
    r"perda.{0,10}consciência",
    r"avc",
    r"derrame",
    r"paralisia.{0,20}rosto",
    r"boca.{0,10}torta",
    r"não consigo falar",
    r"visão.{0,15}embaça",
    r"pressão.{0,10}18[0-9]",  # PA >= 180
    r"sangramento.{0,15}não para",
]

RESPOSTA_EMERGENCIA = (
    "🚨 **ATENÇÃO — EMERGÊNCIA MÉDICA** 🚨\n\n"
    "Os sintomas que você descreveu podem indicar uma situação de risco de vida.\n\n"
    "**Ligue IMEDIATAMENTE para o SAMU: 192**\n"
    "ou vá à **UPA mais próxima** AGORA.\n\n"
    "Não espere. Não tente resolver sozinho."
)


def detectar_red_flag(mensagem: str) -> bool:
    """Retorna True se a mensagem contém sintomas de emergência."""
    mensagem_lower = mensagem.lower()
    return any(re.search(p, mensagem_lower) for p in RED_FLAG_PATTERNS)


# --- SCOPE VALIDATOR ---
# Detecta perguntas completamente fora do domínio de saúde

OUT_OF_SCOPE_PATTERNS = [
    r"capital.{0,10}(país|estado|cidade)",
    r"restaurante",
    r"previsão.{0,10}tempo",
    r"futebol",
    r"receita.{0,10}(culinária|bolo|comida)",
    r"traduz",
    r"programação",
    r"código.{0,10}python",
]

RESPOSTA_FORA_ESCOPO = (
    "Só posso ajudar com questões relacionadas à saúde e ao sistema CarePlus. "
    "Para outros assuntos, por favor utilize outra ferramenta. "
    "Posso ajudar com alguma questão de saúde?"
)


def detectar_fora_escopo(mensagem: str) -> bool:
    """Retorna True se a mensagem é claramente fora do domínio."""
    mensagem_lower = mensagem.lower()
    return any(re.search(p, mensagem_lower) for p in OUT_OF_SCOPE_PATTERNS)


# --- OUTPUT VALIDATOR ---
# Verifica se a resposta do LLM contém conteúdo proibido

OUTPUT_PROIBIDO_PATTERNS = [
    r"(tome|tomar|usar|use|aumentar|reduzir).{0,30}(mg|comprimido|cápsula|dose)",
    r"diagnóstico.{0,20}é",
    r"você tem.{0,30}(doença|síndrome|infarto|avc)",
    r"prescrevo",
    r"receito",
]


def validar_saida(resposta: str) -> tuple[bool, str]:
    """
    Valida a resposta do LLM.
    Retorna (True, resposta) se válida ou (False, mensagem_bloqueio) se inválida.
    """
    resposta_lower = resposta.lower()
    for pattern in OUTPUT_PROIBIDO_PATTERNS:
        if re.search(pattern, resposta_lower):
            return False, (
                "Não consigo fornecer essa informação. "
                "Para orientações sobre medicamentos ou diagnósticos, "
                "consulte seu médico responsável."
            )
    return True, resposta


print("✅ Guardrails configurados:")
print(f"   - Red flag patterns: {len(RED_FLAG_PATTERNS)}")
print(f"   - Out-of-scope patterns: {len(OUT_OF_SCOPE_PATTERNS)}")
print(f"   - Output proibido patterns: {len(OUTPUT_PROIBIDO_PATTERNS)}")

# Testes rápidos dos guardrails
print("\n🧪 Testes dos guardrails:")
print(f"   'dor no peito' → red_flag: {detectar_red_flag('dor no peito')}")
print(f"   'qual restaurante?' → out_of_scope: {detectar_fora_escopo('qual restaurante perto de mim?')}")
print(f"   'minha pressão está alta' → red_flag: {detectar_red_flag('minha pressão está alta hoje')}")