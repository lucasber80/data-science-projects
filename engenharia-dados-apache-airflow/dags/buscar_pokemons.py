from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os

def buscar_pokemons():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=10000'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemons = data['results']
        
        lista_pokemons = [pokemon['name'] for pokemon in pokemons]

        df = pd.DataFrame(lista_pokemons, columns=['Nome'])

        output_dir = '/opt/airflow/output'
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'pokemons.xlsx')

        df.to_excel(output_path, index=False)

        print(f"Arquivo Excel salvo em: {output_path}")
    else:
        print(f"Erro ao buscar Pokémons: {response.status_code}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 26),
}

with DAG(
    dag_id='buscar_pokemons_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['pokemon'],
) as dag:

    tarefa_buscar_pokemons = PythonOperator(
        task_id='buscar_pokemons',
        python_callable=buscar_pokemons
    )
