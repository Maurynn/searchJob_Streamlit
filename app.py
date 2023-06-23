import streamlit as st
import requests

# Título do aplicativo
st.title("Vagas para Devs")

# Criar campos para os filtros de busca
search_description, search_location = st.columns(2)
description = search_description.text_input('Descrição da vaga (por exemplo, Python, JavaScript, etc.)')
location = search_location.text_input('Localização')

# Adicionar botão de buscar
if st.button('Buscar'):

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
            
             # Criar uma seção expansível para cada vaga de emprego
            with st.expander(job["title"], expanded=False):
                # Verificar se a vaga possui informações da empresa
                if 'company' in job and 'display_name' in job['company']:
                    st.subheader(f"Empresa: {job['company']['display_name']}")
                st.text(f"Localização: {job['location']['display_name']}")
                st.write(job["description"])  # A descrição da vaga
                st.markdown(f"[Ver detalhes da vaga]({job['redirect_url']})")
  
