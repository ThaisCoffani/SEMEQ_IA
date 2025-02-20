# Detecção e Classificação de Falhas Mecânicas com MAFAULDA

## Objetivo

O objetivo deste projeto é desenvolver uma solução para detectar e classificar falhas mecânicas utilizando o banco de dados **MAFAULDA**. O projeto utiliza técnicas de pré-processamento de dados e redes neurais artificiais (RNA) para analisar os sinais de sensores e identificar possíveis falhas em sistemas rotativos.

## Sobre o Dataset

O dataset **MAFAULDA** contém dados de vibração e áudio coletados de um sistema rotativo sob diferentes condições de operação, incluindo operação normal e com falhas de desbalanceamento. O dataset é composto por vários arquivos CSV, cada um contendo 8 colunas correspondentes a diferentes sensores.

### Sequências Normais
- **49 sequências** sem falhas.
- Cada sequência tem uma velocidade de rotação fixa, variando de **737 rpm** a **3686 rpm**, com incrementos de aproximadamente **60 rpm**.

### Falhas de Desbalanceamento
- As falhas foram simuladas com cargas variando de **6 g** a **35 g**.
- Para cargas abaixo de **30 g**, foram utilizadas as mesmas 49 velocidades de rotação do caso normal.
- Para cargas iguais ou acima de **30 g**, a vibração resultante limita a velocidade máxima de rotação a **3300 rpm**, reduzindo o número de frequências de rotação distintas.

A tabela abaixo mostra o número de sequências por peso:

| Peso (g) | Número de Medições |
|----------|---------------------|
| 6        | 49                  |
| 10       | 48                  |
| 15       | 48                  |
| 20       | 49                  |
| 25       | 47                  |
| 30       | 47                  |
| 35       | 45                  |
| **Total**| **333**             |

### Estrutura dos Arquivos CSV
Cada arquivo CSV contém 8 colunas, correspondentes aos seguintes sensores:

1. **Coluna 1**: Sinal do tacômetro (frequência de rotação).
2. **Colunas 2 a 4**: Acelerômetro do rolamento inferior (direções axial, radial e tangencial).
3. **Colunas 5 a 7**: Acelerômetro do rolamento superior (direções axial, radial e tangencial).
4. **Coluna 8**: Sinal do microfone.

## pre_processamento.py
Este arquivo contém funções para preparar e organizar os dados antes de serem usados no treinamento da RNA:

### extrair_zip(caminho_zip, pasta_destino):

1) Extrai os arquivos do dataset compactado (archive.zip) para uma pasta de destino.

2) Verifica se o arquivo ZIP existe e cria a pasta de destino, se necessário.

### verificar_csv(pasta):

1) Verifica a integridade dos arquivos CSV em uma pasta específica.

2) Confere se todos os arquivos têm 8 colunas e se não há valores vazios.

3) Reporta erros, como número incorreto de colunas ou valores nulos.

### juntar_csv(pasta, destino, label):

1) Combina todos os arquivos CSV de uma pasta em um único DataFrame.

2) Adiciona uma coluna results com o rótulo fornecido (0 para falhas, 1 para normal).

3) Salva o DataFrame combinado em um novo arquivo CSV na pasta de destino.

## RNA.py

Este arquivo implementa uma rede neural feedforward para classificação de falhas mecânicas. Aqui estão os principais pontos:

### Estrutura da Rede Neural:

### Camadas:

- Camada de entrada: 8 neurônios (correspondentes às 8 colunas do dataset).
- Camadas ocultas: 2 camadas com 4 e 2 neurônios, respectivamente, usando a função de ativação ReLU.
- Camada de saída: 1 neurônio com ativação sigmoid (para classificação binária).

Função de perda: binary_crossentropy (adequada para problemas de classificação binária).

Otimizador: Adam.

### Melhorias Possíveis:
- Aumentar o número de épocas e ajustar o batch size para melhorar o desempenho.
- Adicionar mais camadas ou neurônios para aumentar a capacidade de aprendizado da rede.
- Experimentar outras funções de ativação ou otimizadores.
- Implementar validação cruzada para avaliar melhor a generalização do modelo.
- Aumentar o número de seeds

### Geração de Relatório:
- Um arquivo PDF (resultados_rna.pdf) é gerado com os melhores resultados encontrados (acurácia, F1 Score e R²).

## main.py
No main.py, os caminhos dos arquivos são configurados para um ambiente específico. É importante que o usuário altere esses caminhos para refletir a estrutura de diretórios do seu próprio sistema. Por exemplo:

- caminho_zip: Deve apontar para o local onde o arquivo archive.zip está armazenado.
- pasta_destino: Deve ser uma pasta onde os arquivos extraídos serão salvos.
- pastas: Contém os caminhos para as subpastas do dataset extraído, onde cada pasta corresponde a um tipo de falha ou condição normal.
- pasta_datasets: Pasta onde os datasets processados serão salvos.
