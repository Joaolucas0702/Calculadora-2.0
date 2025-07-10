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
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    st.set_page_config(page_title="Calculadora de Despesas", layout="centered")
    st.title("🏠 Calculadora de Despesas Imobiliárias")

    # Seleção do tipo de operação
    tipo_operacao = st.selectbox(
        "Tipo de Operação",
        ["Compra com financiamento", "Compra à vista", "Empréstimo com imóvel de garantia"]
    )

    # Função para criar inputs padronizados
    def input_monetario(label, min_value=0.0, value=0.0, step=100.0, max_value=None, help_text=""):
        return st.number_input(
            label,
            min_value=min_value,
            value=value,
            step=step,
            max_value=max_value,
            help=help_text,
            format="%.2f"
        )

    # Campos comuns
    valor_imovel = input_monetario(
        "Valor total do imóvel", 
        value=250000.00,
        step=1000.00,
        help="Valor de compra do imóvel"
    )

    primeiro_imovel = st.checkbox("Primeiro imóvel? (50% de desconto no registro)")
    seguro = input_monetario("Valor do seguro", value=1500.00, step=50.00)

    # Campos específicos por operação
    if tipo_operacao == "Compra com financiamento":
        valor_financiado = input_monetario(
            "Valor financiado", 
            max_value=valor_imovel,
            value=valor_imovel * 0.8,  # Sugere 80% do valor
            help="Valor que será financiado pelo banco"
        )
        
        tipo_financiamento = st.selectbox(
            "Tipo de financiamento", 
            ["SBPE", "MCMV", "Pro Cotista"]
        )
        
        cidade = st.selectbox(
            "Cidade", 
            ["Goiânia", "Trindade", "Aparecida de Goiânia", "Caldas Novas"]
        )
        
        if cidade == "Aparecida de Goiânia":
            renda_bruta = input_monetario(
                "Renda bruta mensal", 
                value=5000.00,
                help="Renda familiar bruta"
            )

    elif tipo_operacao == "Empréstimo com imóvel de garantia":
        valor_emprestimo = input_monetario(
            "Valor do empréstimo", 
            value=valor_imovel * 0.6,  # 60% do valor
            max_value=valor_imovel,
            help="Normalmente até 60% do valor do imóvel"
        )
        tipo_financiamento = st.selectbox(
            "Tipo de operação", 
            ["SBPE", "MCMV", "Pro Cotista"]
        )

    # Botão de cálculo
    if st.button("🟢 Calcular Despesas", type="primary"):
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

if __name__ == "__main__":
    main()
