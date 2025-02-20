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

'''

pasta_datasets = r"D:\SEMEQ\datasets"


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

seeds = range(10) 
results = []

for seed in seeds:
  accuracy, f1, r2 = RNA(data_all, test_size=0.25, seed=seed)
  results.append((seed, accuracy, f1, r2))

best_seed, best_accuracy, best_f1, best_r2 = max(results, key=lambda x: x[3])

print(f"Melhor seed: {best_seed}")
print(f"Accuracy: {best_accuracy:.4f}, F1 Score: {best_f1:.4f}, R²: {best_r2:.4f}")


