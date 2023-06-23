import streamlit as st
import requests

# Título do aplicativo
st.sidebar.title("Vagas para Devs")

# Criar campos para os filtros de busca na barra lateral
st.sidebar.header("Filtros de busca")
description = st.sidebar.text_input('Descrição da vaga (por exemplo, Python, JavaScript, etc.)')
location = st.sidebar.text_input('Localização')

# Inicializar o estado da sessão para as vagas salvas
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = []

# Adicionar botão de buscar
if st.sidebar.button('Buscar'):
    # Configuração da API do Adzuna
    API_URL = "https://api.adzuna.com/v1/api/jobs/br/search/1" # substitua {country} pelo código do país
    API_KEY = "f2471fc865692b0445fa6efd1f65c765" # substitua pelo sua chave de API
    APP_ID = "d0210377" # substitua pelo seu App ID

    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'results_per_page': 50,
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

        # Exibir as vagas de emprego
        for i, job in enumerate(jobs):
            # Verificar se a vaga está salva
            if job["id"] in [j['id'] for j in st.session_state.saved_jobs]:
                save_button_text = "Vaga salva"
            else:
                save_button_text = "Salvar vaga"
            
            # Criar uma seção expansível para cada vaga de emprego
            with st.expander(job["title"], expanded=True):
                st.subheader(f"Empresa: {job['company']['display_name']}")
                st.text(f"Localização: {job['location']['display_name']}")
                st.text(job["description"])  # A descrição da vaga
                st.markdown(f"[Ver detalhes da vaga]({job['redirect_url']})")
                if st.button(save_button_text, key=f'save_button_{i}'):
                    # Adicionar a vaga aos favoritos
                    st.session_state.saved_jobs.append(job)

# Seção para exibir as vagas salvas
st.sidebar.header("Vagas salvas")
for job in st.session_state.saved_jobs:
    st.sidebar.subheader(job['title'])
    st.sidebar.write(job['company']['display_name'])
    st.sidebar.write(job['location']['display_name'])
    st.sidebar.markdown(f"[Ver detalhes da vaga]({job['redirect_url']})")





 "https://api.adzuna.com/v1/api/jobs/br/search/1" # substitua {country} pelo código do país
    API_KEY = "f2471fc865692b0445fa6efd1f65c765" # substitua pelo sua chave de API
    APP_ID = "d0210377" # substitua pelo seu 