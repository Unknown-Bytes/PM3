import pandas as pd
import numpy as np
import os

def clean_data():
    # Caminhos
    input_path = 'dados_brutos/netflix_raw.csv'
    output_path = 'dados_intermediarios/netflix_clean.csv'
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Carregamento
    print(f"Lendo {input_path}...")
    df = pd.read_csv(input_path)
    initial_shape = df.shape
    
    # 2. Tratamento de Missing Values (Placeholders)
    print("Tratando placeholders...")
    placeholders = ['Not Given', '???', 'NULL', 'N/A', '', 'Unknown', 'nan']
    df.replace(placeholders, np.nan, inplace=True)
    
    # 3. Padronização Textual (Strip e Casing)
    print("Limpando espaços extras e padronizando texto...")
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        # Voltar NaNs que viraram 'nan' string
        df.loc[df[col] == 'nan', col] = np.nan

    # 4. Correção Estrutural (Dados Deslocados)
    print("Corrigindo colunas deslocadas (type/rating)...")
    valid_types = ['Movie', 'TV Show']
    
    # Máscara para onde 'type' parece ser um rating
    mask_shifted = df['type'].notna() & ~df['type'].str.title().isin(valid_types)
    
    # Mover rating do 'type' para a coluna 'rating' se 'rating' estiver nulo
    df.loc[mask_shifted & df['rating'].isna(), 'rating'] = df.loc[mask_shifted, 'type']
    
    # Corrigir 'type' com base na 'duration'
    def infer_type(duration):
        if pd.isna(duration): return np.nan
        d = str(duration).lower()
        if 'season' in d: return 'TV Show'
        return 'Movie'
    
    df.loc[mask_shifted, 'type'] = df.loc[mask_shifted, 'duration'].apply(infer_type)
    
    # Padronizar 'type'
    def standardize_type(val):
        if pd.isna(val): return val
        v = str(val).strip().lower()
        if 'movie' in v: return 'Movie'
        if 'tv show' in v or 'tv' in v: return 'TV Show'
        return val

    df['type'] = df['type'].apply(standardize_type)
    
    # Limpar qualquer coisa que não seja Movie ou TV Show
    df.loc[~df['type'].isin(valid_types), 'type'] = np.nan

    # 5. Tratamento de Duplicados
    print("Removendo duplicados...")
    # Duplicados exatos (ignorando show_id que pode variar)
    cols_to_check = [c for c in df.columns if c != 'show_id']
    df.drop_duplicates(subset=cols_to_check, keep='first', inplace=True)
    
    # IDs repetidos - Manter apenas o primeiro
    df.drop_duplicates(subset='show_id', keep='first', inplace=True)
    
    # 6. Padronização de Unidades (Duration)
    print("Padronizando durações...")
    def standardize_duration(d):
        if pd.isna(d): return d
        d = str(d).lower()
        # "90 minutes", "90m", "90 min" -> "90 min"
        if 'min' in d or 'minute' in d or 'm' in d:
            # Extrair apenas números
            num = ''.join(filter(str.isdigit, d))
            return f"{num} min" if num else d
        if 'season' in d:
            num = ''.join(filter(str.isdigit, d))
            suffix = "Season" if num == "1" else "Seasons"
            return f"{num} {suffix}"
        return d

    df['duration'] = df['duration'].apply(standardize_duration)

    # 7. Conversão de Tipos
    print("Convertendo tipos (datas e anos)...")
    # date_added
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    
    # release_year
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

    # 8. Correções Lógicas e de Títulos
    print("Corrigindo títulos e inconsistências temporais...")
    # Limpar sufixos de erro nos títulos (ex: #ERROR!)
    df['title'] = df['title'].str.replace(r'\s*#ERROR!.*', '', regex=True, case=False)
    
    # Corrigir viajantes do tempo: se date_added < release_year, ajustar para o ano de lançamento
    mask_traveler = df['date_added'].dt.year < df['release_year']
    df.loc[mask_traveler, 'date_added'] = pd.to_datetime(
        df.loc[mask_traveler, 'release_year'].astype(int).astype(str) + '-01-01', 
        errors='coerce'
    )
    
    print(f"Corrigidos {mask_traveler.sum()} registros de 'viagem no tempo'.")

    # 9. Salvando Resultado
    print(f"Salvando dataset limpo em {output_path}...")
    df.to_csv(output_path, index=False)
    
    final_shape = df.shape
    print(f"Processamento concluído.")
    print(f"Linhas iniciais: {initial_shape[0]} | Linhas finais: {final_shape[0]}")
    print(f"Removidos: {initial_shape[0] - final_shape[0]} registros.")

if __name__ == "__main__":
    clean_data()
