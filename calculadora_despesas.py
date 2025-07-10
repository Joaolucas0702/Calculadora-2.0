def calcular_registro_cartorio(valor_imovel, primeiro_imovel=False):
    """
    Calcula o registro conforme tabela vigente (2025) - Valores TOTAIS da tabela
    """
    tabela_registro = [
        (625.89, 73.22),
        (1251.79, 111.00),
        (2503.58, 141.69),
        (5007.15, 205.46),
        (10014.30, 403.86),
        (15021.47, 437.19),
        (25035.77, 562.09),
        (37553.65, 696.73),
        (50071.55, 923.45),
        (62589.43, 1098.21),
        (100143.09, 1539.87),
        (150214.64, 2314.53),
        (250075.67, 3117.53),  # Valor exato para R$ 250.000
        (375536.58, 4092.94),
        (500715.44, 4822.74),
        (751073.17, 5788.70),
        (1126069.75, 6936.52),
        (float('inf'), 8810.65)
    ]
    
    for limite, valor in tabela_registro:
        if valor_imovel <= limite:
            return round(valor * 0.5 if primeiro_imovel else valor, 2)
    return 0.0

def calcular_escritura(valor_imovel):
    """
    Calcula a escritura conforme tabela de notas (2025)
    """
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
        (250075.67, 5060.56),  # Valor exato para R$ 250.000
        (375536.58, 6066.46),
        (500715.44, 6967.01),
        (751073.17, 7421.70),
        (1126069.75, 7527.07),
        (float('inf'), 7737.59)
    ]
    
    for limite, valor in tabela_escritura:
        if valor_imovel <= limite:
            return round(valor, 2)
    return 0.0

def calcular_itbi(cidade, valor_imovel, valor_financiado=0, renda_bruta=None):
    """
    Calcula ITBI com alíquotas por cidade:
    - Goiânia e Trindade: 2%
    - Aparecida e Senador Canedo: 2.5%
    """
    if cidade == "Aparecida de Goiânia":
        aliquota = 0.025  # 2.5% fixo conforme solicitado
    elif cidade == "Senador Canedo":
        aliquota = 0.025  # 2.5%
    else:  # Goiânia e Trindade
        aliquota = 0.02  # 2%
    
    base_calculo = valor_imovel - valor_financiado
    return round(base_calculo * aliquota, 2)

def calcular_lavratura_contrato(tipo_financiamento, valor_operacao):
    """
    Calcula lavratura conforme tipo de operação:
    - SBPE: 0.3% (mínimo R$ 1.000)
    - MCMV: 0.25% (mínimo R$ 800)
    - Pro Cotista: 0.35% (mínimo R$ 1.200)
    """
    if tipo_financiamento == "SBPE":
        return max(1000, valor_operacao * 0.003)
    elif tipo_financiamento == "MCMV":
        return max(800, valor_operacao * 0.0025)
    else:  # Pro Cotista
        return max(1200, valor_operacao * 0.0035)
