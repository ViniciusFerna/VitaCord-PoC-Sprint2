DOCUMENTOS_CLINICOS = [
    {
        "id": "losartana",
        "conteudo": """
        Medicamento: Losartana Potássica 50mg
        Classe: Antagonista do receptor AT1 da angiotensina II (BRA)
        Indicação: Hipertensão arterial, nefropatia diabética, insuficiência cardíaca
        Posologia típica: 50mg uma vez ao dia, podendo ser aumentada para 100mg
        Contraindicações: Gravidez (especialmente 2º e 3º trimestres), hipersensibilidade ao princípio ativo
        Interações relevantes:
          - AINEs (Ibuprofeno, Diclofenaco): reduz efeito anti-hipertensivo e aumenta risco de lesão renal
          - Diuréticos poupadores de potássio (Espironolactona): risco de hipercalemia
          - Lítio: aumento dos níveis séricos de lítio
        Efeitos adversos comuns: Tontura, hipotensão (especialmente na 1ª dose), hipercalemia, tosse (menos frequente que IECAs)
        Monitoramento: Verificar função renal e potássio sérico periodicamente
        """
    },
    {
        "id": "manchester_dor_toracica",
        "conteudo": """
        Protocolo de Manchester — Dor Torácica
        
        NÍVEL 1 — EMERGENTE (atendimento imediato):
        - Dor torácica com irradiação para braço esquerdo, mandíbula ou dorso
        - Dor associada a sudorese fria, náusea e palidez
        - Dor com dispneia intensa em repouso
        - Dor com pressão arterial muito elevada (>180/110) ou muito baixa (<90/60)
        - Suspeita de dissecção aórtica
        Conduta: Acionar SAMU (192) imediatamente
        
        NÍVEL 2 — MUITO URGENTE (até 10 minutos):
        - Dor torácica em repouso sem irradiação clássica
        - Dor com palpitações ou arritmia percebida
        Conduta: Encaminhar à UPA ou pronto-socorro com urgência
        
        NÍVEL 3 — URGENTE (até 60 minutos):
        - Dor torácica relacionada a esforço físico que cede com repouso
        - Dor atípica sem outros sinais de alarme
        Conduta: Avaliação médica em até 1 hora
        """
    },
    {
        "id": "manchester_dispneia",
        "conteudo": """
        Protocolo de Manchester — Dispneia (Falta de Ar)
        
        NÍVEL 1 — EMERGENTE (atendimento imediato):
        - Dispneia intensa em repouso com cianose (lábios ou dedos azulados)
        - Falta de ar associada a dor torácica
        - Saturação de oxigênio abaixo de 90%
        - Estridor ou sibilância intensa
        Conduta: Acionar SAMU (192) imediatamente
        
        NÍVEL 2 — MUITO URGENTE (até 10 minutos):
        - Dispneia com frequência respiratória >30 irpm
        - Falta de ar com taquicardia (>120 bpm)
        Conduta: Encaminhar à UPA com urgência
        
        NÍVEL 3 — URGENTE (até 60 minutos):
        - Dispneia aos esforços sem outros sinais
        - Piora progressiva em paciente com doença respiratória conhecida
        Conduta: Avaliação médica em até 1 hora
        """
    },
    {
        "id": "hipertensao_diretrizes",
        "conteudo": """
        Diretrizes para Hipertensão Arterial — SBH/SBC 2024
        
        Classificação pela pressão arterial (adultos):
        - Normal: < 120/80 mmHg
        - Pré-hipertensão: 120-139 / 80-89 mmHg
        - Hipertensão Estágio 1: 140-159 / 90-99 mmHg
        - Hipertensão Estágio 2: 160-179 / 100-109 mmHg
        - Hipertensão Estágio 3: ≥ 180 / ≥ 110 mmHg (crise hipertensiva)
        
        Crise hipertensiva — quando acionar emergência:
        - PA ≥ 180/120 mmHg com sintomas: dor de cabeça intensa, alteração visual, dor torácica → emergência hipertensiva
        - PA ≥ 180/120 mmHg sem sintomas → urgência hipertensiva (avaliação em horas)
        
        Monitoramento domiciliar recomendado:
        - Medição 2x ao dia (manhã e tarde)
        - Registrar valores e sintomas associados
        - Manter diário de pressão para apresentar ao médico
        """
    },
    {
        "id": "sinais_vitais_referencia",
        "conteudo": """
        Valores de Referência para Sinais Vitais — Adultos
        
        Pressão Arterial:
        - Normal: < 120/80 mmHg
        - Elevada: 120-129 / < 80 mmHg
        - Hipertensão Estágio 1: 130-139 / 80-89 mmHg
        - Hipertensão Estágio 2: ≥ 140 / ≥ 90 mmHg
        
        Frequência Cardíaca:
        - Normal em repouso: 60-100 bpm
        - Bradicardia: < 60 bpm
        - Taquicardia: > 100 bpm
        - Alerta: > 120 bpm em repouso
        
        Temperatura Corporal:
        - Normal: 36,0 – 37,4 °C
        - Febrícula: 37,5 – 37,9 °C
        - Febre: ≥ 38,0 °C
        - Hipotermia: < 35,0 °C
        
        Saturação de Oxigênio (SpO2):
        - Normal: 95-100%
        - Atenção: 90-94%
        - Emergência: < 90%
        """
    }
]

print(f"✅ {len(DOCUMENTOS_CLINICOS)} documentos clínicos definidos:")
for doc in DOCUMENTOS_CLINICOS:
    print(f"   - {doc['id']}")