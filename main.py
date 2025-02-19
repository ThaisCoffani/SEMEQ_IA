import shutil
import os
import pandas as pd
from pre_processamento import extrair_zip, verificar_csv, juntar_csv
from RNA import data_all, RNA

'''
caminho_zip = r"D:\SEMEQ\archive.zip" 
pasta_destino = r"D:\SEMEQ\extracted" 

extrair_zip(caminho_zip, pasta_destino)

pastas = {
  r"D:\SEMEQ\extracted\imbalance\imbalance\6g": 0,
  r"D:\SEMEQ\extracted\imbalance\imbalance\10g": 0,
  r"D:\SEMEQ\extracted\imbalance\imbalance\15g": 0,
  r"D:\SEMEQ\extracted\imbalance\imbalance\20g": 0,
  r"D:\SEMEQ\extracted\imbalance\imbalance\25g": 0,
  r"D:\SEMEQ\extracted\imbalance\imbalance\30g": 0,
  r"D:\SEMEQ\extracted\imbalance\imbalance\35g": 0,
  r"D:\SEMEQ\extracted\normal\normal": 1
}

pasta_datasets = r"D:\SEMEQ\datasets"

for pasta in pastas:
  verificar_csv(pasta)
  
for pasta, label in pastas.items():
  juntar_csv(pasta, pasta_datasets, label)

for pasta in pastas:
  shutil.rmtree(pasta)

def listar_arquivos(pasta_datasets):
  arquivos = []
  for arquivo in os.listdir(pasta_datasets):
    caminho_completo = os.path.join(pasta_datasets, arquivo)
    if os.path.isfile(caminho_completo) and arquivo.endswith(".csv"):
      arquivos.append(caminho_completo)
  return arquivos

arquivos_csv = listar_arquivos(pasta_datasets)

print("Arquivos encontrados:", arquivos_csv)

data_all = data_all(pasta_datasets)

RNA(data_all, test_size=0.25, n_seeds=1)

'''

data_all = r"D:\SEMEQ\datasets\data_all.csv" 

data_all = pd.read_csv(data_all)
print("começo RNA")

RNA(data_all, test_size=0.25, n_seeds=1)



