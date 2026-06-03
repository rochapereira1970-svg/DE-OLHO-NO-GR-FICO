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


def calcular_icom_over15(
    over15_casa,
    over15_fora,
    media_gols_casa,
    media_gols_fora,
    h2h_over15
):
    pontos = 0

    # Over 1.5 mandante
    pontos += (over15_casa / 100) * 25

    # Over 1.5 visitante
    pontos += (over15_fora / 100) * 25

    # Média de gols
    media_total = media_gols_casa + media_gols_fora

    if media_total >= 3.0:
        pontos += 25
    elif media_total >= 2.5:
        pontos += 20
    elif media_total >= 2.0:
        pontos += 15
    elif media_total >= 1.8:
        pontos += 10

    # H2H
    pontos += (h2h_over15 / 100) * 25

    return round(pontos)
