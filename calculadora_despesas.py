def calcular_itbi(cidade, valor_imovel, valor_financiado, renda_bruta=None):
    if cidade == "Aparecida de Goiânia":
        if renda_bruta is None:
            return 0.0
        aliquota = 0.02 if renda_bruta <= 5000 else 0.03
        return valor_imovel * aliquota
    else:
        base_calculo = valor_imovel - valor_financiado
        return base_calculo * 0.02

def calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel):
    tabela_registro = [
        (625.89, 185.10),
        (1251.79, 253.52),
        (2503.58, 324.16),
        (5007.15, 432.28),
        (10014.30, 809.74),
        (15021.47, 862.71),
        (25035.77, 1079.03),
        (37553.65, 1350.52),
        (50071.55, 1785.35),
        (62589.43, 2109.81),
        (100143.09, 2756.54),
        (150214.64, 4107.37),
        (157959.89, 5007.94),
        (250357.73, 5060.56),
        (263266.45, 5961.14),
        (375536.58, 6066.46),
        (500715.44, 6967.01),
        (526532.99, 7421.70),
        (1053066.05, 7527.07),
        (float('inf'), 7737.59),
    ]

    valor_total = max(valor_imovel, valor_financiado)
    
    for limite, custo in tabela_registro:
        if valor_total <= limite:
            registro = custo
            break
    
    if primeiro_imovel:
        registro *= 0.5
    
    return round(registro, 2)

def calcular_lavratura_contrato(tipo_financiamento, valor_financiado):
    if tipo_financiamento == "SBPE":
        return max(1000, valor_financiado * 0.003)
    elif tipo_financiamento == "MCMV":
        return max(800, valor_financiado * 0.0025)
    else:  # Pro Cotista
        return max(1200, valor_financiado * 0.0035)

def calcular_escritura(valor_imovel):
    tabela_escritura = [
        (625.89, 185.10),
        (1251.79, 253.52),
        (2503.58, 324.16),
        (5007.15, 432.28),
        (10014.30, 809.74),
        (15021.47, 862.71),
        (25035.77, 1079.03),
        (37553.65, 1350.52),
        (50071.55, 1785.35),
        (62589.43, 2109.81),
        (100143.09, 2756.54),
        (150214.64, 4107.37),
        (157959.89, 5007.94),
        (250357.73, 5060.56),
        (263266.45, 5961.14),
        (375536.58, 6066.46),
        (500715.44, 6967.01),
        (526532.99, 7421.70),
        (1053066.05, 7527.07),
        (float('inf'), 7737.59),
    ]

    for limite, custo in tabela_escritura:
        if valor_imovel <= limite:
            return round(costo, 2)
    return 0.0