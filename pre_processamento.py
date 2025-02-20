import zipfile
import os
import pandas as pd

def extrair_zip(caminho_zip, pasta_destino):
  if not os.path.exists(caminho_zip):
    print(f"Arquivo {caminho_zip} não encontrado.")
    return

  if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

  with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
    zip_ref.extractall(pasta_destino)
    print(f"Arquivos extraídos para: {pasta_destino}")

def verificar_csv(pasta):
  data_error = []
    
  for arquivo in os.listdir(pasta):
    if arquivo.endswith(".csv"):
      caminho_arquivo = os.path.join(pasta, arquivo)
      try:
        df = pd.read_csv(caminho_arquivo)
                
        if df.shape[1] != 8:
          data_error.append((arquivo, f"Número de colunas incorreto: {df.shape[1]}"))
          continue
                
        if df.isnull().any().any():
          data_error.append((arquivo, "Valores vazios encontrados"))
                    
      except Exception as e:
        data_error.append((arquivo, f"Erro ao ler o arquivo: {str(e)}"))
    
  if data_error:
    print("Arquivos com problemas encontrados:")
    print(data_error)
  else:
    print("Todos os arquivos estão OK: 8 colunas e sem valores vazios.")


def juntar_csv(pasta, destino, label):
  data_csv = pd.DataFrame()  
    
  if not os.path.exists(pasta):
    raise FileNotFoundError(f"A pasta '{pasta}' não existe.")
    
  for arquivo in os.listdir(pasta):
    if arquivo.endswith(".csv"): 
      caminho_arquivo = os.path.join(pasta, arquivo)  
      try:
        low_data = pd.read_csv(caminho_arquivo, header=None)
        data_csv = pd.concat([data_csv, low_data], ignore_index=True)
      except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {str(e)}")
    
  data_csv['results'] = int(label)

  if not os.path.exists(destino):
    os.makedirs(destino)

  nome_arquivo = f"data_{os.path.basename(pasta)}.csv"
  caminho_destino = os.path.join(destino, nome_arquivo)

  data_csv.to_csv(caminho_destino, index=False)

  print(f"Arquivo salvo: {caminho_destino}")
  return caminho_destino



