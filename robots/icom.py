# ICOM - Índice de Confiança de Oportunidade de Mercado

def classificar_icom(pontos):
    if pontos >= 95:
        return "ELITE"
    elif pontos >= 90:
        return "PREMIUM"
    elif pontos >= 85:
        return "FORTE"
    elif pontos >= 80:
        return "BOA"
    else:
        return "DESCARTAR"
