import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from pynput import keyboard
import pyautogui

from gerenciador_cofre import carregar_cofre, cofre_existe, obter_caminho_completo_cofre

processando_atalho = False

def pedir_senha_mestra():
    """Cria um pop-up para o usuário digitar a senha mestra."""
    root = tk.Tk()
    root.withdraw()
    senha = simpledialog.askstring("Cofre de Senhas Físico", "Digite sua Senha Mestra:", show='*')
    root.destroy()
    return senha

def acao_de_preenchimento():
    """Função principal executada pelo atalho."""
    global processando_atalho
    if processando_atalho:
        return

    processando_atalho = True
    
    if not cofre_existe():
        messagebox.showerror("Erro", f"Cofre não encontrado em '{obter_caminho_completo_cofre()}'")
        processando_atalho = False
        return

    senha_mestra = pedir_senha_mestra()
    if not senha_mestra:
        processando_atalho = False
        return
    
    cofre = carregar_cofre(senha_mestra)
    if not cofre:
        messagebox.showerror("Acesso Negado", "Senha mestra incorreta ou cofre corrompido.")
        processando_atalho = False
        return
        
    # --- Lógica de preenchimento ---
    # Futuramente, podemos melhorar aqui para detectar a janela ativa e encontrar
    # a credencial correta. Por enquanto, usamos a primeira da lista.
    try:
        credencial = cofre['servicos'][0]
        usuario = credencial.get('usuario', '')
        senha = credencial.get('senha', '')
        
        pyautogui.write(usuario, interval=0.05)
        pyautogui.press('tab')
        pyautogui.write(senha, interval=0.05)
    except (IndexError, KeyError):
        messagebox.showerror("Erro no Cofre", "Nenhuma credencial encontrada ou formato inválido.")
    
    processando_atalho = False

def on_press(key):
    """Callback do listener: verifica se a tecla 'ç' foi pressionada."""
    try:
        if key.char == 'ç':
            threading.Thread(target=acao_de_preenchimento).start()
    except AttributeError:
        pass # Ignora teclas especiais

def iniciar_listener():
    """Inicia o listener de teclado e mantém o script rodando."""
    print("=" * 40)
    print("Cofre de Senhas Físico - Motor Iniciado")
    print(f"Monitorando o atalho: 'ç'")
    print(f"Cofre esperado em: '{obter_caminho_completo_cofre()}'")
    print("Pressione Ctrl+C neste terminal para encerrar.")
    print("=" * 40)
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    iniciar_listener()