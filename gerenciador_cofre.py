# Arquivo: gerenciador_cofre.py
# Responsabilidade: Salvar e carregar o arquivo do cofre no SD Card.

import os
import json
from seguranca import criptografar, descriptografar

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! IMPORTANTE: CONFIGURE O CAMINHO DO SEU SD CARD AQUI !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Verifique a letra da unidade no seu explorador de arquivos (ex: "E:/", "F:/").
CAMINHO_SD_CARD = "E:/" 
NOME_ARQUIVO_COFRE = "cofre.dat" 

def obter_caminho_completo_cofre() -> str:
    """Retorna o caminho completo para o arquivo do cofre."""
    return os.path.join(CAMINHO_SD_CARD, NOME_ARQUIVO_COFRE)

def cofre_existe() -> bool:
    """Verifica se o arquivo do cofre já existe no local configurado."""
    return os.path.exists(obter_caminho_completo_cofre())

def salvar_cofre(dados_cofre: dict, senha_mestra: str) -> bool:
    """Converte, criptografa e salva o cofre. Retorna True em sucesso."""
    caminho_cofre = obter_caminho_completo_cofre()
    dados_em_bytes = json.dumps(dados_cofre, indent=4).encode('utf-8')
    dados_criptografados = criptografar(dados_em_bytes, senha_mestra)
    
    try:
        with open(caminho_cofre, "wb") as f:
            f.write(dados_criptografados)
        return True
    except IOError as e:
        print(f"ERRO DE E/S: Não foi possível escrever no caminho '{caminho_cofre}'. Detalhe: {e}")
        return False

def carregar_cofre(senha_mestra: str) -> dict | None:
    """Carrega, descriptografa e converte o cofre. Retorna um dicionário ou None."""
    caminho_cofre = obter_caminho_completo_cofre()
    
    if not cofre_existe():
        return None
        
    try:
        with open(caminho_cofre, "rb") as f:
            dados_criptografados = f.read()
    except IOError as e:
        print(f"ERRO DE E/S: Não foi possível ler o arquivo '{caminho_cofre}'. Detalhe: {e}")
        return None

    dados_descriptografados = descriptografar(dados_criptografados, senha_mestra)
    
    if dados_descriptografados:
        return json.loads(dados_descriptografados)
    
    return None