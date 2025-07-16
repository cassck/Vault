# Arquivo: seguranca.py
# Responsabilidade: Lógica de criptografia e segurança.

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# --- Constantes de Segurança ---
SALT_SIZE = 16
ITERATIONS = 480000 
KEY_SIZE = 32
NONCE_SIZE = 12

backend = default_backend()

def derivar_chave(senha_mestra: str, salt: bytes) -> bytes:
    """Deriva uma chave criptográfica segura a partir da senha mestra usando PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=backend
    )
    return kdf.derive(senha_mestra.encode('utf-8'))

def criptografar(dados: bytes, senha_mestra: str) -> bytes:
    """
    Criptografa os dados usando AES-GCM, empacotando salt, nonce e o texto cifrado.
    """
    salt = os.urandom(SALT_SIZE)
    chave = derivar_chave(senha_mestra, salt)
    nonce = os.urandom(NONCE_SIZE)
    
    aesgcm = AESGCM(chave)
    dados_criptografados = aesgcm.encrypt(nonce, dados, None)
    
    return salt + nonce + dados_criptografados

def descriptografar(dados_criptografados_completos: bytes, senha_mestra: str) -> bytes | None:
    """
    Descriptografa o bloco de dados, validando a senha e a integridade.
    Retorna os dados originais ou None em caso de falha.
    """
    try:
        salt = dados_criptografados_completos[:SALT_SIZE]
        nonce = dados_criptografados_completos[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
        dados_reais_criptografados = dados_criptografados_completos[SALT_SIZE + NONCE_SIZE:]
        
        chave = derivar_chave(senha_mestra, salt)
        
        aesgcm = AESGCM(chave)
        dados_descriptografados = aesgcm.decrypt(nonce, dados_reais_criptografados, None)
        return dados_descriptografados
    except Exception:
        # A exceção pode ser por senha incorreta (InvalidTag) ou qualquer outro problema.
        # Não damos detalhes do erro por segurança.
        return None