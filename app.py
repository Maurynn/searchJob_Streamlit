import streamlit as st
import pandas as pd
import requests
import json
import sessionstate

st.set_page_config(page_title="Vagas para Devs", layout='wide')

# Configuração da API do Adzuna
API_URL = "https://api.adzuna.com/v1/api/jobs/br/search/1" # substitua {country} pelo código do país
API_KEY = "f2471fc865692b0445fa6efd1f65c765" # substitua pela sua chave de API
APP_ID = "d0210377" # substitua pelo seu App ID

# Título do aplicativo
st.title("Vagas para Devs")

# Criar campos para os filtros de busca no topo da página
description = st.text_input('Descrição da vaga (por exemplo, Python, JavaScript, etc.)', key='desc')
location = st.text_input('Localização', key='loc')

# Configuração de estado da sessão
state = SessionState.get(fav_jobs=[])

# Adicionar botão de buscar
if st.button('Buscar'):
    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'results_per_page': 20,
        'what': description,
        'where': location
    }

    # Fazer a requisição para a API do Adzuna com os parâmetros de busca
    response = requests.get(API_URL, params=params)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Converter os dados da resposta para JSON
        data = response.json()
        jobs = data['results']

        for job in jobs:
            # Criar uma seção expansível para cada vaga de emprego
            with st.expander(job["title"], expanded=True):
                # Exibir detalhes da vaga
                st.write(job["description"])
                st.text("Localização: " + job["location"]["display_name"])
                st.text("Empresa: " + job["company"]["display_name"])
                st.markdown(f"[Ver detalhes da vaga]({job['redirect_url']})")
                
                # Adicionar botão para salvar vaga
                if st.button("Salvar vaga", key=job["id"]):
                    fav_jobs.append(job)
                    st.success("Vaga salva com sucesso!")

# Seção para exibir as vagas salvas
st.sidebar.header("Vagas salvas")
for job in fav_jobs:
    st.sidebar.subheader(job["title"])
    st.sidebar.write(job["location"]["display_name"])
