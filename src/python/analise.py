import pandas as pd

def executar_analise(arquivo):
    df = pd.read_csv(arquivo)

    
    dados = {
        "total_linhas": len(df),
        "total_colunas": len(df.columns),
        "valores_nulos": df.isnull().sum().sum(),
        "valores_duplicados": df.duplicated().sum()
    }

    return dados