import os
from config import MAX_RESULTS, BACK_PREVIOUS, BACK_MAIN

def display_main_menu():
    print("\n------------------------------")
    print(" Menu Principal YouTube")
    print("------------------------------")
    print("1. Pesquisar no YouTube (Geral)")
    print("2. Pesquisar no YouTube Music")
    print("3. Download por Link (Vídeo/Canal/Playlist)")
    print("4. Sair")
    print("------------------------------")
    return input("Escolha uma opção (1-4): ")

def get_search_term():
    term = input("Digite o termo de busca (0 pra voltar ao principal): ").strip()
    if term == BACK_PREVIOUS or not term:
        print("Voltando ao menu principal...")
        return None
    return term

def get_link_input():
    link = input("Cole o link (0 pra voltar ao principal): ").strip()
    if link == BACK_PREVIOUS or not link:
        print("Voltando ao menu principal...")
        return None
    return link

def display_results(results):
    if not results:
        print("\nTruta, não achei nenhum resultado. Tenta outra busca.")
        return 0
    print("\n------------------------------")
    print(f" Resultados Encontrados (Máx. {MAX_RESULTS})")
    print("------------------------------")
    for i, entry in enumerate(results[:MAX_RESULTS]):
        title = entry.get('title', 'Título Desconhecido')
        uploader = entry.get('uploader', 'Uploader Desconhecido')
        print(f"[{i+1}] {title} - ({uploader})")
    print(f"[{BACK_PREVIOUS}] Voltar ao Menu Anterior (retry busca)")
    print(f"[{BACK_MAIN}] Voltar ao Menu Principal")
    print("------------------------------")
    return len(results[:MAX_RESULTS])

def get_selection(max_index):
    while True:
        choice = input(f"Escolha (1-{max_index}, 0 menu anterior, 00 principal): ").strip()
        if choice == BACK_PREVIOUS:
            print("Voltando ao menu anterior...")
            return -1
        elif choice == BACK_MAIN:
            print("Voltando ao menu principal...")
            return -2
        try:
            index = int(choice)
            if 1 <= index <= max_index:
                return index - 1
            else:
                print("Número inválido. Tenta 1-N, 0 ou 00.")
        except ValueError:
            print("Isso não é um número. Tenta de novo.")

def display_action_menu():
    print("\n------------------------------")
    print(" O que quer fazer?")
    print("------------------------------")
    print("1. Reproduzir (MPV Streaming)")
    print("2. Baixar (MP3)")
    print(f"[{BACK_PREVIOUS}] Voltar ao Menu Anterior (lista de resultados)")
    print(f"[{BACK_MAIN}] Voltar ao Menu Principal")
    print("------------------------------")
    return input(f"Escolha (1-2, {BACK_PREVIOUS} anterior, {BACK_MAIN} principal): ")

def display_exit():
    print("\nFalou, maluco! Até mais!")

def display_cookies_warning():
    print("\n------------------------------")
    print(" AVISO: Sem Cookies.txt!")
    print("------------------------------")
    print("Porra, truta, não achei 'cookies.txt'.")
    print("Sem ele, YouTube bloqueia (auth 2025).")
    print("\nComo pegar:")
    print("1. Extensão 'Get cookies.txt LOCALLY' (Chrome).")
    print("2. Loga em music.youtube.com.")
    print("3. Export > Salva aqui.")
    print("4. Roda de novo (expira ~1 mês).")
    print("Pra ytmusicapi full: Converta pra JSON (pergunta).")
    print("------------------------------")
    input("ENTER pra voltar ao principal...")

def display_download_complete(link_type, path, count=1):
    print(f"\n------------------------------")
    print(f" Download OK! ({link_type})")
    print("------------------------------")
    print(f"Salvo em: {os.path.abspath(path)}")
    if count > 1:
        print(f"{count} itens MP3.")
    print("------------------------------")
    input("ENTER pra voltar ao principal...")
