from robots.icom import (
    calcular_icom_over15,
    classificar_icom
)

def testar_robo():

    icom = calcular_icom_over15(
        over15_casa=90,
        over15_fora=85,
        media_gols_casa=1.8,
        media_gols_fora=1.5,
        h2h_over15=80
    )

    classificacao = classificar_icom(icom)

    resultado = {
        "jogo": "Flamengo x Palmeiras",
        "icom": icom,
        "classificacao": classificacao
    }

    return resultado


if __name__ == "__main__":
    print(testar_robo())
