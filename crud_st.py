import os
import pandas as pd
import streamlit as st

arquivo = "cadastro.txt"

# Carregar ou criar arquivo
if os.path.exists(arquivo) and os.path.getsize(arquivo) > 0:
  df = pd.read_csv(arquivo)
else:
  df = pd.DataFrame(columns=["NOME", "CARGO", "SALARIO", "CIDADE", "ESTADO"])

st.title("📋 Sistema de Cadastro de Funcionários")

# Mostrar tabela atual
st.subheader("Funcionários cadastrados")
st.dataframe(df)
if not df.empty:
    csv = df.to_csv(index=False, sep=';').encode('latin-1')
    st.download_button(
        label="⬇️ Exportar CSV",
        data=csv,
        file_name="funcionarios.csv",
        mime="text/csv"
    )


# Formulário para adicionar novo funcionário
st.subheader("Adicionar novo funcionário")
with st.form("cadastro_form"):
    nome = st.text_input("Nome").title()
    cargo = st.text_input("Cargo").title()
    salario = st.number_input("Salário", min_value=0.0, step=100.0)
    cidade = st.text_input("Cidade").title()
    estado = st.text_input("Estado").upper()

    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if nome and cargo and cidade and estado and salario > 0:
            novo = {"NOME": nome, "CARGO": cargo, "SALARIO": salario, "CIDADE": cidade, "ESTADO": estado}
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success(f"Funcionário {nome} cadastrado com sucesso!")
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos corretamente.")
            st.rerun()

# Parte para consulta e edição
st.subheader("🔎 Consultar e editar funcionário")

if not df.empty:
    indice = st.number_input(
        f"Digite o índice do funcionário (0 a {len(df) - 1})",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    if st.button("Consultar"):
        st.session_state["funcionario"] = df.iloc[indice]
        st.session_state["indice"] = int(indice)
else:
    st.info("Nenhum funcionário cadastrado ainda.")

# Edição (persistente)
if "funcionario" in st.session_state:
    dados = st.session_state["funcionario"]
    idx = st.session_state["indice"]

    st.write("Dados atuais:")
    st.write(dados)

    novo_cargo = st.text_input("Cargo", value=dados["CARGO"]).title()
    novo_salario = st.number_input("Salário", value=float(dados["SALARIO"]), min_value=0.0, step=100.0)
    nova_cidade = st.text_input("Cidade", value=dados["CIDADE"]).title()
    novo_estado = st.text_input("Estado", value=dados["ESTADO"]).upper()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Salvar alterações"):
            df.loc[idx, "CARGO"] = novo_cargo
            df.loc[idx, "SALARIO"] = novo_salario
            df.loc[idx, "CIDADE"] = nova_cidade
            df.loc[idx, "ESTADO"] = novo_estado

            df.to_csv(arquivo, index=False)
            st.success("Dados atualizados com sucesso!")
            st.session_state["funcionario"] = df.iloc[idx]
            st.rerun()

    with col2:
        if st.button("🗑️ Excluir funcionário"):
            st.session_state["confirmar_exclusao"] = True

    if st.session_state.get("confirmar_exclusao"):
        st.warning(f"Tem certeza que deseja excluir **{dados['NOME']}**?")
        if st.button("✅ Confirmar exclusão"):
            df = df.drop(index=idx).reset_index(drop=True)
            df.to_csv(arquivo, index=False)
            st.success(f"Funcionário {dados['NOME']} excluído com sucesso!")
            del st.session_state["funcionario"]
            del st.session_state["indice"]
            del st.session_state["confirmar_exclusao"]
            st.rerun()