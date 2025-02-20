from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, r2_score
import pandas as pd
import os
from fpdf import FPDF


# No primeiro momento utilizei essa função para a diminuição do dataset

def data_all(pasta_datasets):
  arquivos_csv = [os.path.join(pasta_datasets, arquivo) for arquivo in os.listdir(pasta_datasets) if arquivo.endswith(".csv")]

  dataframes = []

  for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo) 
    df_amostrado = df.sample(frac=0.1, random_state=42) 
    dataframes.append(df_amostrado)

  data = pd.concat(dataframes, ignore_index=True)

  os.makedirs("datasets", exist_ok=True)

  caminho_saida = "datasets/data_all.csv"
  data.to_csv(caminho_saida, index=False)
  print(f"Arquivo final salvo: {caminho_saida}")

  return data

'''
# Down Sampling -> Rodou mais de 3h e não funcionou

def data_all(pasta_datasets):
  arquivos_csv = [os.path.join(pasta_datasets, arquivo) for arquivo in os.listdir(pasta_datasets) if arquivo.endswith(".csv")]

  dataframes = []
  
  b = 10000  # Taxa de passo
  x = b  

  for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo) 
    data_decreased = []  
        
    a = 0  # Index inicial
    for _ in range(int(len(df) / x)):  # Usa `_` pois a variável `i` não é necessária
      data_decreased.append(df.iloc[a:b, :].sum() / x)
      a += x
      b += x
        
    data_decreased = pd.DataFrame(data_decreased)
    dataframes.append(data_decreased)
    
  data = pd.concat(dataframes, ignore_index=True)

  os.makedirs("datasets", exist_ok=True)

  caminho_saida = "datasets/data_all.csv"
  data.to_csv(caminho_saida, index=False)
  print(f"Arquivo final salvo: {caminho_saida}")

  return data
'''


def RNA(data, test_size=0.25, seed=42):
  y = data["results"]
  X = data.drop(columns=["results"])

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    
  model = Sequential()
  model.add(Dense(4, input_dim=8, activation='relu')) 
  model.add(Dense(2, activation='relu'))              
  model.add(Dense(1, activation='sigmoid'))           
    
  model.compile(optimizer=Adam(), loss='binary_crossentropy')  
    
  model.fit(X_train, y_train, epochs=10, batch_size=200, verbose=1)
    
  y_pred = model.predict(X_test)
  y_pred = (y_pred > 0.5).astype(int)
    
  accuracy = accuracy_score(y_test, y_pred.round())   
  f1 = f1_score(y_test, y_pred.round(), average='weighted')
  r2 = r2_score(y_test, y_pred)
    
  return accuracy, f1, r2
    