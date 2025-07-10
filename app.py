import streamlit as st
from calculadora_despesas import (
    calcular_itbi,
    calcular_registro_cartorio,
    calcular_lavratura_contrato,
    calcular_escritura
)

# Função para formatar como moeda brasileira
def formatar_br(valor):
    """Formata valores como R$ 1.234,56"""
    if valor is None:
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    st.set_page_config(page_title="Calculadora de Despesas", layout="centered")
    st.title("🏠 Calculadora de Despesas Imobiliárias")

    # Seleção do tipo de operação
    tipo_operacao = st.selectbox(
        "Tipo de Operação",
        ["Compra com financiamento", "Compra à vista", "Empréstimo com imóvel de garantia"]
    )

    # Campos comuns (com tratamento seguro)
    try:
        valor_imovel = st.number_input(
            "Valor total do imóvel (R$)", 
            min_value=0.0,
            value=250000.0,
            step=1000.0,
            format="%.2f"
        )
    except:
        valor_imovel = 0.0

    primeiro_imovel = st.checkbox("Primeiro imóvel? (50% de desconto no registro)")
    
    try:
        seguro = st.number_input(
            "Seguro (R$)",
            min_value=0.0,
            value=1500.0,
            step=50.0,
            format="%.2f"
        )
    except:
        seguro = 0.0

    # Inicializa variáveis condicionais
    valor_financiado = 0.0
    tipo_financiamento = ""
    cidade = ""
    renda_bruta = None

    # Campos específicos por operação
    if tipo_operacao == "Compra com financiamento":
        try:
            valor_financiado = st.number_input(
                "Valor financiado (R$)", 
                min_value=0.0,
                max_value=valor_imovel,
                value=min(valor_imovel * 0.8, valor_imovel),
                step=1000.0,
                format="%.2f"
            )
        except:
            valor_financiado = 0.0

        tipo_financiamento = st.selectbox(
            "Tipo de financiamento", 
            ["SBPE", "MCMV", "Pro Cotista"]
        )
        
        cidade = st.selectbox(
            "Cidade", 
            ["Goiânia", "Trindade", "Aparecida de Goiânia", "Caldas Novas"]
        )
        
        if cidade == "Aparecida de Goiânia":
            try:
                renda_bruta = st.number_input(
                    "Renda bruta mensal (R$)", 
                    min_value=0.0,
                    value=5000.0,
                    step=100.0,
                    format="%.2f"
                )
            except:
                renda_bruta = 0.0

    elif tipo_operacao == "Empréstimo com imóvel de garantia":
        try:
            valor_emprestimo = st.number_input(
                "Valor do empréstimo (R$)", 
                min_value=0.0,
                max_value=valor_imovel,
                value=valor_imovel * 0.6,
                step=1000.0,
                format="%.2f"
            )
        except:
            valor_emprestimo = 0.0

        tipo_financiamento = st.selectbox(
            "Tipo de operação", 
            ["SBPE", "MCMV", "Pro Cotista"]
        )

    # Botão de cálculo
    if st.button("🟢 Calcular Despesas", type="primary"):
        try:
            if tipo_operacao == "Compra com financiamento":
                itbi = calcular_itbi(cidade, valor_imovel, valor_financiado, renda_bruta if cidade == "Aparecida de Goiânia" else None)
                lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_financiado)
                registro = calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel)
                total = itbi + lavratura + registro + seguro
                
                st.subheader("📋 Resultado para Compra com Financiamento")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Valor do Imóvel", formatar_br(valor_imovel))
                    st.metric("Entrada", formatar_br(valor_imovel - valor_financiado))
                with col2:
                    st.metric("Valor Financiado", formatar_br(valor_financiado))
                    st.metric("Tipo de Financiamento", tipo_financiamento)
                
                st.divider()
                st.subheader("📝 Detalhes das Despesas")
                st.write(f"- **ITBI:** {formatar_br(itbi)}")
                st.write(f"- **Lavratura de Contrato:** {formatar_br(lavratura)}")
                st.write(f"- **Registro:** {formatar_br(registro)}")
                st.write(f"- **Seguro:** {formatar_br(seguro)}")
                st.divider()
                st.success(f"**TOTAL DE DESPESAS:** {formatar_br(total)}")

            elif tipo_operacao == "Compra à vista":
                itbi = calcular_itbi("Goiânia", valor_imovel, 0, None)
                escritura = calcular_escritura(valor_imovel)
                registro = calcular_registro_cartorio(valor_imovel, 0, primeiro_imovel)
                total = itbi + escritura + registro + seguro
                
                st.subheader("📋 Resultado para Compra à Vista")
                st.metric("Valor do Imóvel", formatar_br(valor_imovel))
                
                st.divider()
                st.subheader("📝 Detalhes das Despesas")
                st.write(f"- **Escritura:** {formatar_br(escritura)}")
                st.write(f"- **ITBI:** {formatar_br(itbi)}")
                st.write(f"- **Registro:** {formatar_br(registro)}")
                st.write(f"- **Seguro:** {formatar_br(seguro)}")
                st.divider()
                st.success(f"**TOTAL DE DESPESAS:** {formatar_br(total)}")

            elif tipo_operacao == "Empréstimo com imóvel de garantia":
                lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_emprestimo)
                registro = calcular_registro_cartorio(valor_imovel, valor_emprestimo, primeiro_imovel)
                total = lavratura + registro + seguro
                
                st.subheader("📋 Resultado para Empréstimo com Garantia")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Valor do Imóvel", formatar_br(valor_imovel))
                with col2:
                    st.metric("Valor do Empréstimo", formatar_br(valor_emprestimo))
                
                st.divider()
                st.subheader("📝 Detalhes das Despesas")
                st.write(f"- **Lavratura de Contrato:** {formatar_br(lavratura)}")
                st.write(f"- **Registro da Garantia:** {formatar_br(registro)}")
                st.write(f"- **Seguro:** {formatar_br(seguro)}")
                st.divider()
                st.success(f"**TOTAL DE DESPESAS:** {formatar_br(total)}")

        except Exception as e:
            st.error(f"Erro ao calcular: {str(e)}")
            st.warning("Verifique os valores informados e tente novamente")

if __name__ == "__main__":
    main()
