import sys
import os

from ui import (
    display_main_menu,
    get_search_term,
    get_link_input,
    display_results,
    get_selection,
    display_action_menu,
    display_exit,
    display_cookies_warning,
    display_download_complete
)

from youtube_actions import (
    check_cookies_file,
    search_youtube,
    play_video,
    download_as_mp3,
    download_by_link
)

from config import BACK_PREVIOUS, BACK_MAIN

def run_main_menu():
    while True:
        choice = display_main_menu().strip()
        if choice == '1' or choice == '2':
            if not check_cookies_file():
                display_cookies_warning()
                continue
            search_loop = True
            while search_loop:
                search_term = get_search_term()
                if search_term is None:
                    break
                is_music = choice == '2'
                results = search_youtube(search_term, is_music)
                if not results:
                    input("ENTER pra retry busca...")
                    continue
                results_loop = True
                while results_loop:
                    max_index = display_results(results)
                    if max_index == 0:
                        continue
                    selected_index = get_selection(max_index)
                    if selected_index == -1:
                        continue
                    elif selected_index == -2:
                        results_loop = False
                        search_loop = False
                        break
                    selected_video = results[selected_index]
                    video_url = selected_video.get('url') or selected_video.get('webpage_url')
                    video_title = selected_video.get('title', 'Vídeo Sem Título')
                    if not video_url:
                        print("URL inválida.")
                        input("ENTER pra continuar...")
                        continue
                    action_loop = True
                    while action_loop:
                        action_choice = display_action_menu()
                        if action_choice == BACK_PREVIOUS:
                            action_loop = False
                            break
                        elif action_choice == BACK_MAIN:
                            action_loop = False
                            results_loop = False
                            search_loop = False
                            break
                        elif action_choice == '1':
                            play_video(video_url)
                            action_loop = False
                            break
                        elif action_choice == '2':
                            download_as_mp3(video_url, video_title)
                            action_loop = False
                            break
                        else:
                            print("Opção inválida.")
                            continue
                    if not results_loop:
                        break
                if not search_loop:
                    break
        elif choice == '3':
            if not check_cookies_file():
                display_cookies_warning()
                continue
            link = get_link_input()
            if link is None:
                continue
            result = download_by_link(link)
            if result:
                link_type, path, count = result
                display_download_complete(link_type, path, count)
            else:
                input("Falha. ENTER pra principal...")
        elif choice == '4':
            display_exit()
            sys.exit(0)
        else:
            print("Opção inválida.")
            input("ENTER pra continuar...")

if __name__ == '__main__':
    try:
        run_main_menu()
    except KeyboardInterrupt:
        display_exit()
        sys.exit(0)
