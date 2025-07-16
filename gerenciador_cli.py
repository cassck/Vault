# Arquivo: gerenciador_cli.py
# Responsabilidade: Ferramenta de linha de comando para gerenciar senhas no cofre.

import getpass
import json
from gerenciador_cofre import carregar_cofre, salvar_cofre, cofre_existe

def adicionar_credencial():
    """Fluxo para adicionar uma nova credencial ao cofre."""
    print("\n--- Adicionar Nova Credencial ---")
    site = input("Digite o nome do serviço ou site (ex: google.com): ")
    usuario = input("Digite o nome de usuário/email para este serviço: ")
    senha_servico = getpass.getpass("Digite a senha para este serviço (não aparecerá na tela): ")

    print("\nPara salvar, você precisa destravar o cofre com sua senha mestra.")
    senha_mestra = getpass.getpass("Digite sua Senha Mestra: ")

    cofre_dados = carregar_cofre(senha_mestra)

    # Se o cofre não existir, criamos um novo. Se a senha estiver errada, o carregar_cofre retorna None.
    if cofre_dados is None:
        if cofre_existe():
            print("\n[ERRO] Senha mestra incorreta!")
            return
        else:
            print("\nNenhum cofre encontrado. Criando um novo...")
            cofre_dados = {"servicos": []}

    # Adiciona a nova credencial à lista
    nova_credencial = {"site": site, "usuario": usuario, "senha": senha_servico}
    cofre_dados["servicos"].append(nova_credencial)

    # Salva o cofre atualizado
    if salvar_cofre(cofre_dados, senha_mestra):
        print(f"\n[SUCESSO] Credencial para '{site}' salva com segurança!")
    else:
        print("\n[ERRO] Falha ao salvar a credencial.")


def listar_credenciais():
    """Fluxo para listar as credenciais salvas de forma segura."""
    print("\n--- Listar Credenciais Salvas ---")
    if not cofre_existe():
        print("Nenhum cofre encontrado. Adicione uma credencial primeiro.")
        return

    senha_mestra = getpass.getpass("Digite sua Senha Mestra para ver as credenciais: ")
    cofre_dados = carregar_cofre(senha_mestra)

    if cofre_dados is None:
        print("\n[ERRO] Senha mestra incorreta ou cofre corrompido.")
        return

    servicos = cofre_dados.get("servicos", [])
    if not servicos:
        print("\nO cofre está vazio.")
        return
    
    print("\nSuas credenciais salvas:")
    print("-" * 30)
    for i, cred in enumerate(servicos):
        # NUNCA imprima a senha real no terminal.
        print(f"  {i+1}. Serviço: {cred.get('site', 'N/A')}")
        print(f"     Usuário: {cred.get('usuario', 'N/A')}")
        print(f"     Senha:   **********")
    print("-" * 30)


def main():
    """Função principal que exibe o menu."""
    while True:
        print("\n--- Gerenciador do Cofre de Senhas ---")
        print("Escolha uma opção:")
        print("  [1] Adicionar nova credencial")
        print("  [2] Listar credenciais salvas")
        print("  [S] Sair")
        
        escolha = input("> ").strip().lower()

        if escolha == '1':
            adicionar_credencial()
        elif escolha == '2':
            listar_credenciais()
        elif escolha == 's':
            print("Encerrando o gerenciador.")
            break
        else:
            print("Opção inválida, por favor tente novamente.")

if __name__ == "__main__":
    main()