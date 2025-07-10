import streamlit as st
from calculadora_despesas import (
    calcular_itbi,
    calcular_registro_cartorio,
    calcular_lavratura_contrato,
    calcular_escritura
)

def main():
    st.set_page_config(page_title="Calculadora de Despesas", layout="centered")
    st.title("🏠 Calculadora de Despesas Imobiliárias")

    # Seleção do tipo de operação
    tipo_operacao = st.selectbox(
        "Tipo de Operação",
        ["Compra com financiamento", "Compra à vista", "Empréstimo com imóvel de garantia"]
    )

    # Campos comuns a todas as operações
    valor_imovel = st.number_input("Valor do imóvel (R$)", min_value=0.0, step=1000.0)
    primeiro_imovel = st.checkbox("Primeiro imóvel? (50% de desconto no registro)")
    seguro = st.number_input("Seguro (R$)", min_value=0.0, step=100.0, value=0.0)

    # Campos específicos por operação
    if tipo_operacao == "Compra com financiamento":
        valor_financiado = st.number_input("Valor financiado (R$)", min_value=0.0, step=1000.0, max_value=valor_imovel)
        tipo_financiamento = st.selectbox("Tipo de financiamento", ["SBPE", "MCMV", "Pro Cotista"])
        cidade = st.selectbox("Cidade", ["Goiânia", "Trindade", "Aparecida de Goiânia", "Caldas Novas"])
        
        if cidade == "Aparecida de Goiânia":
            renda_bruta = st.number_input("Renda bruta (R$)", min_value=0.0, step=100.0)

    elif tipo_operacao == "Empréstimo com imóvel de garantia":
        valor_emprestimo = st.number_input(
            "Valor do empréstimo (R$)", 
            min_value=0.0, 
            step=1000.0, 
            value=valor_imovel * 0.6,
            max_value=valor_imovel
        )
        tipo_financiamento = st.selectbox("Tipo de financiamento", ["SBPE", "MCMV", "Pro Cotista"])

    # Botão de cálculo
    if st.button("Calcular Despesas"):
        if tipo_operacao == "Compra com financiamento":
            itbi = calcular_itbi(cidade, valor_imovel, valor_financiado, renda_bruta if cidade == "Aparecida de Goiânia" else None)
            lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_financiado)
            registro = calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel)
            total = itbi + lavratura + registro + seguro
            
            st.subheader("📟 CÁLCULO PARA COMPRA DE IMÓVEL COM FINANCIAMENTO")
            st.write(f"🏡 **Valor de Compra e Venda:** R$ {valor_imovel:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"🏦 **Valor Financiado:** R$ {valor_financiado:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"💰 **Entrada:** R$ {(valor_imovel - valor_financiado):,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write("\n**💰 Despesas:**")
            st.write(f"- Lavratura: R$ {lavratura:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- ITBI: R$ {itbi:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- Registro: R$ {registro:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- Seguro: R$ {seguro:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"\n✅ **Desconto no registro:** {'Sim' if primeiro_imovel else 'Não'}")
            st.write(f"💵 **Total Estimado:** R$ {total:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

        elif tipo_operacao == "Compra à vista":
            itbi = calcular_itbi("Goiânia", valor_imovel, 0, None)  # Assume Goiânia como padrão
            escritura = calcular_escritura(valor_imovel)
            registro = calcular_registro_cartorio(valor_imovel, 0, primeiro_imovel)
            total = itbi + escritura + registro + seguro
            
            st.subheader("📟 CÁLCULO PARA COMPRA À VISTA DE IMÓVEL")
            st.write(f"🏡 **Valor de Compra e Venda:** R$ {valor_imovel:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write("\n**💰 Despesas:**")
            st.write(f"- Escritura: R$ {escritura:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- ITBI: R$ {itbi:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- Registro: R$ {registro:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- Seguro: R$ {seguro:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"\n✅ **Desconto no registro:** {'Sim' if primeiro_imovel else 'Não'}")
            st.write(f"💵 **Total Estimado:** R$ {total:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

        elif tipo_operacao == "Empréstimo com imóvel de garantia":
            lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_emprestimo)
            registro = calcular_registro_cartorio(valor_imovel, valor_emprestimo, primeiro_imovel)
            total = lavratura + registro + seguro
            
            st.subheader("📟 CÁLCULO PARA EMPRÉSTIMO COM IMÓVEL EM GARANTIA")
            st.write(f"🏡 **Valor de Avaliação do Imóvel:** R$ {valor_imovel:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"🏦 **Valor do Empréstimo (60%):** R$ {valor_emprestimo:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write("\n**💰 Despesas:**")
            st.write(f"- Lavratura do contrato: R$ {lavratura:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- Registro da garantia: R$ {registro:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"- Seguro: R$ {seguro:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
            st.write(f"\n✅ **Desconto no registro:** {'Sim' if primeiro_imovel else 'Não'}")
            st.write(f"💵 **Total Estimado:** R$ {total:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

if __name__ == "__main__":
    main()