import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import requests

# Configuração do SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///jobs.db')

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    location = Column(String(200))
    description = Column(Text)

Base.metadata.create_all(engine)

# Criar uma sessão
session = Session(engine)

# Título do aplicativo
st.title("VAGAS PARA DEVS")

# Criar campos para os filtros de busca na barra lateral
st.sidebar.header("Filtros de busca")
description = st.sidebar.text_input('Descrição da vaga (por exemplo, Python, JavaScript, etc.)')
location = st.sidebar.text_input('Localização')

# Adicionar botão de buscar
if st.sidebar.button('Buscar'):
    # Carregar as vagas salvas
    saved_jobs = session.query(Job).all()

    # Configuração da API do Adzuna
    API_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/1" # substitua {br} pelo código do país
    API_KEY = "f2471fc865692b0445fa6efd1f65c765" # substitua pelo sua chave de API
    APP_ID = "d0210377" # substitua pelo seu App ID

    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'results_per_page': 50,  # Aumente este número para obter mais resultados
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
            if job["id"] in [j.id for j in saved_jobs]:
                save_button_text = "Vaga salva"
            else:
                save_button_text = "Salvar vaga"
            
            # Criar um contêiner para cada vaga de emprego
            with st.container():
                st.header(job["title"])
                st.text(f"Empresa: {job['company']['display_name']}")
                st.text(f"Localização: {job['location']['display_name']}")
                st.text(job["description"])  # A descrição da vaga
                st.markdown(f"[Ver detalhes da vaga]({job['redirect_url']})")
                if st.button(save_button_text, key=f'save_button_{i}'):
                    # Adicionar a vaga aos favoritos
                    new_job = Job(id=job["id"], title=job["title"], location=job["location"]["display_name"], description=job["description"])
                    session.add(new_job)
                    session.commit()

        # Seção para exibir as vagas salvas
        st.sidebar.header("Vagas salvas")
        for job in saved_jobs:
            st.sidebar.subheader(job.title)
            st.sidebar.write(job.location)

# Fechar a sessão
session.close()