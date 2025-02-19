from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, r2_score
import pandas as pd
import os
from fpdf import FPDF

def data_all(pasta_datasets):
  arquivos_csv = [os.path.join(pasta_datasets, arquivo) for arquivo in os.listdir(pasta_datasets) if arquivo.endswith(".csv")]

  dataframes = []

  for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo, dtype='float32') 
    df_amostrado = df.sample(frac=0.1, random_state=42) 
    dataframes.append(df_amostrado)

  data = pd.concat(dataframes, ignore_index=True)

  data = data.astype('float32')

  os.makedirs("datasets", exist_ok=True)

  caminho_saida = "datasets/data_all.csv"
  data.to_csv(caminho_saida, index=False)
  print(f"Arquivo final salvo: {caminho_saida}")

  return data


def RNA(data, test_size=0.25, n_seeds=1):

  y = data["results"]
  X = data.drop(columns=["results"])

  best_accuracy = -np.inf
  best_f1 = -np.inf
  best_r2 = -np.inf
  best_accuracy_seed = None
  best_f1_seed = None
  best_r2_seed = None
  
  accuracy_scores = []
  f1_scores = []
  r2_scores = []
    
  for seed in range(n_seeds):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    
    print("sepração")
        
    model = Sequential()
    model.add(Dense(4, input_dim=8, activation='relu')) 
    model.add(Dense(2, activation='relu'))              
    model.add(Dense(1, activation='sigmoid'))           
        
    model.compile(optimizer=Adam(), loss='binary_crossentropy')  
        
    # Testar diferentes epochs e batch sizes
    model.fit(X_train, y_train, epochs=10, batch_size=200, verbose=1)
        
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred.round())   
    f1 = f1_score(y_test, y_pred.round(), average='weighted')
    r2 = r2_score(y_test, y_pred)
        
    if accuracy > best_accuracy:
      best_accuracy = accuracy
      best_accuracy_seed = seed
            
    if f1 > best_f1:
      best_f1 = f1
      best_f1_seed = seed
            
    if r2 > best_r2:
      best_r2 = r2
      best_r2_seed = seed
        
    print(f"Seed: {seed+1} - Accuracy: {accuracy:.4f}, F1 Score: {f1:.4f}, R²: {r2:.4f}")
    
    print("\nMelhor Accuracy encontrado:")
    print(f"Melhor Accuracy: {best_accuracy:.4f} na seed {best_accuracy_seed+1}")
    for f1, seed in f1_scores:
      print(f"Seed: {seed+1} - F1: {f1:.4f}, R²: {r2_scores[seed][0]:.4f}")

    print("\nMelhor F1 Score encontrado:")
    print(f"Melhor F1 Score: {best_f1:.4f} na seed {best_f1_seed+1}")
    for accuracy, seed in accuracy_scores:
      print(f"Seed: {seed+1} - Accuracy: {accuracy:.4f}, R²: {r2_scores[seed][0]:.4f}")

    print("\nMelhor R² encontrado:")
    print(f"Melhor R²: {best_r2:.4f} na seed {best_r2_seed+1}")
    for accuracy, seed in accuracy_scores:
      print(f"Seed: {seed+1} - Accuracy: {accuracy:.4f}, F1: {f1_scores[seed][0]:.4f}")
        
    generate_pdf(best_accuracy, best_f1, best_r2, best_accuracy_seed, best_f1_seed, best_r2_seed, accuracy_scores, f1_scores, r2_scores)


  return best_accuracy, best_f1, best_r2
    
def generate_pdf(best_accuracy, best_f1, best_r2, best_accuracy_seed, best_f1_seed, best_r2_seed, accuracy_scores, f1_scores, r2_scores):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial", size=12)

  pdf.cell(200, 10, txt="Resultados da RNA", ln=True, align="C")

  pdf.cell(200, 10, txt="\nMelhor Accuracy encontrado:", ln=True)
  pdf.cell(200, 10, txt=f"Melhor Accuracy: {best_accuracy:.4f} na seed {best_accuracy_seed + 1}", ln=True)
  for f1, seed in f1_scores:
    if seed == best_accuracy_seed:
      pdf.cell(200, 10, txt=f"Seed: {seed + 1} - F1: {f1:.4f}, R²: {r2_scores[seed][0]:.4f}", ln=True)

  pdf.cell(200, 10, txt="\nMelhor F1 Score encontrado:", ln=True)
  pdf.cell(200, 10, txt=f"Melhor F1 Score: {best_f1:.4f} na seed {best_f1_seed + 1}", ln=True)
  for accuracy, seed in accuracy_scores:
    if seed == best_f1_seed:
      pdf.cell(200, 10, txt=f"Seed: {seed + 1} - Accuracy: {accuracy:.4f}, R²: {r2_scores[seed][0]:.4f}", ln=True)

  pdf.cell(200, 10, txt="\nMelhor R² encontrado:", ln=True)
  pdf.cell(200, 10, txt=f"Melhor R²: {best_r2:.4f} na seed {best_r2_seed + 1}", ln=True)
  for accuracy, seed in accuracy_scores:
    if seed == best_r2_seed:
      pdf.cell(200, 10, txt=f"Seed: {seed + 1} - Accuracy: {accuracy:.4f}, F1: {f1_scores[seed][0]:.4f}", ln=True)

  pdf.output("resultados_rna.pdf")
  print("PDF gerado com sucesso: resultados_rna.pdf")
