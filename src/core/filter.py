import pandas as pd

# Dicionário inteligente mapeando cada região a todos os seus estados (siglas e nomes)
REGIOES_ESTADOS = {
    "norte": ["ac", "acre", "ap", "amapá", "amapa", "am", "amazonas", "pa", "pará", "para", "ro", "rondônia", "rondonia", "rr", "roraima", "to", "tocantins"],
    "nordeste": ["al", "alagoas", "ba", "bahia", "ce", "ceará", "ceara", "ma", "maranhão", "maranhao", "pb", "paraíba", "paraiba", "pe", "pernambuco", "pi", "piauí", "piaui", "rn", "rio grande do norte", "se", "sergipe"],
    "centrooeste": ["go", "goiás", "goias", "mt", "mato grosso", "ms", "mato grosso do sul", "df", "distrito federal"],
    "sudeste": ["es", "espírito santo", "espirito santo", "mg", "minas gerais", "rj", "rio de janeiro", "sp", "são paulo", "sao paulo"],
    "sul": ["pr", "paraná", "parana", "rs", "rio grande do sul", "sc", "santa catarina"]
}

def processar_e_filtrar(dados, filtros, regiao="nacional"):
    df = pd.DataFrame(dados)
    if df.empty:
        return df

    if regiao != "nacional" and regiao in REGIOES_ESTADOS:
        termos_regiao = REGIOES_ESTADOS[regiao]
        mascara_regiao = pd.Series(False, index=df.index)

        for termo in termos_regiao:
            if len(termo) == 2:
                padrao = rf"\b{termo}\b"
                mascara_regiao = mascara_regiao | df['titulo'].str.contains(padrao, case=False, regex=True, na=False)
            else:
                mascara_regiao = mascara_regiao | df['titulo'].str.contains(termo, case=False, regex=False, na=False)

        is_pci = df['fonte'] == 'PCI'
        df = df[is_pci | mascara_regiao]

    if filtros and len(filtros) > 0:
        mascara_filtros = pd.Series(False, index=df.index)
        for termo in filtros:
            termo = termo.strip().lower()
            if len(termo) == 2:
                padrao = rf"\b{termo}\b"
                mascara = df['titulo'].str.contains(padrao, case=False, regex=True, na=False)
            else:
                mascara = df['titulo'].str.contains(termo, case=False, regex=False, na=False)
            mascara_filtros = mascara_filtros | mascara

        df = df[mascara_filtros]

    return df