import streamlit as st
import requests
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Configuração da API do Adzuna
API_URL = "https://api.adzuna.com/v1/api/jobs/br/search/1" # substitua {country} pelo código do país
API_KEY = "f2471fc865692b0445fa6efd1f65c765" # substitua pelo sua chave de API
APP_ID = "d0210377" # substitua pelo seu App ID

# Título do aplicativo
st.markdown("<h1 style='text-align: center; color: cyan;'>Hey, Dev! 👨🏻‍💻 \nPROCURE SUA VAGA DE EMPREGO AQUI!</h1>", unsafe_allow_html=True)


# Criar campos para os filtros de busca
search_description, search_location = st.columns(2)
description = search_description.text_input('Descrição da vaga (por exemplo, Python, JavaScript, etc.)')
location = search_location.text_input('Localização')

# Adicionar botão de buscar
if st.button('Buscar'):

    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'results_per_page': 15,
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
        
        # Analisar as habilidades mais requisitadas nas descrições das vagas
        descriptions = ' '.join([job["description"] for job in jobs])
        tokens = nltk.word_tokenize(descriptions)
        tokens = [token.lower() for token in tokens if token.isalpha()]
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        token_counts = Counter(tokens)
        most_common_tokens = dict(token_counts.most_common(50))
        wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(most_common_tokens)
        fig, ax = plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(fig)

        # Exibir as vagas de emprego
        for i, job in enumerate(jobs):
            # Criar uma seção expansível para cada vaga de emprego
            with st.expander(job["title"], expanded=True):
                # Verificar se a vaga possui informações da empresa
                if 'company' in job and 'display_name' in job['company']:
                    st.subheader(f"Empresa: {job['company']['display_name']}")
                st.text(f"Localização: {job['location']['display_name']}")
                st.write(job["description"])  # A descrição da vaga
                st.markdown(f"[Ver detalhes da vaga]({job['redirect_url']})")

        # Analisar a distribuição das vagas por localização
        locations = [job['location']['display_name'] for job in jobs]
        location_counts = Counter(locations)
        fig, ax = plt.subplots()
        ax.bar(location_counts.keys(), location_counts.values())
        plt.xticks(rotation=90)
        st.pyplot(fig)

        
