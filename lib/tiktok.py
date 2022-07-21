from ffmpeg_progress_yield import FfmpegProgress
from playwright.sync_api import sync_playwright
from pathlib import Path
from time import sleep
from tqdm import tqdm

import requests
import sys
import os

TiktokHeader = {
    'user-agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.146.3-Gen4_12000410) '
    'AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true'
}


class Tiktok:

    def __init__(self) -> None:
        pass

    # Retorna o link do video
    def get_link_video(url):

        with sync_playwright() as pw:

            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            video_raw_link = page.locator('video').get_attribute('src')

            browser.close()

        return video_raw_link  # Retorna o link do video
    # Retorna o id do video da url
    def return_video_id(url):
        get_id = requests.get(url, headers=TiktokHeader).url  # pega a url

        if 'video/' in get_id:  # se video/ estiver na url
            video_id = get_id.split('video/')[1].split('?')[0]
            # divida-o por video/ e pegue o segundo[1] valor desse list
            # Se tiver apenas isso teremos o id mas o id com o query param junto de outra coisa entt pegaremos e dividir pelo query param [?] e pegaremos o primeiro valor [0]

        # pego o id e concaterno com _water.mp4 para assim saber qual video precisa limpar a marca d'agua e o id tbm para não haver subscrição de video ou conflito com ffmpeg
        video_original = f'{video_id}_water.mp4'

        # o nome do video apos a remoção da marca d'agua
        new_video = f'{video_id}.mp4'

        directory_saved = './Videos Saved TTK/'
        if not os.path.exists(directory_saved):
            directory_saved = os.mkdir('./Videos Saved TTK/')
            print('Directory as created!')
        
        path_file = str(directory_saved) + video_original
        path_new_file = str(directory_saved) + new_video
        return video_original, path_file, path_new_file  # retorna esses valores a serem usados

    def spin_cursor(timer, msg):

        chars = '\\|/-'

        while timer:
            if timer < 10:
                for cursor in chars:
                    sleep(0.1)
                    
                    sys.stdout.write(f'\r{cursor} {msg}')
                    sys.stdout.flush()
                timer += 1
            else:
                break 

    def clean_terminal():
        
        if os.system('clear') == 1:
            os.system('cls')
            

    # Baixa o video
    def download_video(url, video_original, path_file):
        video_raw_link = Tiktok.get_link_video(url)  # pega o link do video

        download_req = requests.get(
            video_raw_link,
            headers=TiktokHeader,
            stream=True
        )  # Requisita a esse link no modo stream em fluxo de dados e bytes

        # retorna o tamanho do arquivo em bytes
        size_file = int(download_req.headers.get('content-length', 0))

        # Abre o video, e vai escrever em bytes nele
        # Usando o tqdm() que ira exibir a barra de progresso enquanto o download esta sendo feito
        print(path_file)
        with open(path_file, 'wb') as out_file, tqdm(
                desc=video_original,
                total=size_file,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024) as download_progress:

            for data in download_req.iter_content(chunk_size=1024):

                size = out_file.write(data)
                download_progress.update(size)

        # Message dialog response
        print('Download Complete!')
        Tiktok.clean_terminal()

    # Remove marca d'agua
    def remove_watermark(path_file, path_new_file):

        check_existence = Path(path_file)
        check_existence_new = Path(path_new_file)
        if check_existence_new.is_file() == True:
            print('This video exists!')
            sleep(1)
        else:
            command = [
                'ffmpeg',
                '-i', path_file,
                '-filter:v',
                'crop=in_w:in_h-185',
                '-c:a', 'copy',
                path_new_file
            ]

            ff = FfmpegProgress(command)
            with tqdm(total=100, position=1, desc='Removing Watermark :: ') as wm_remover:
                for progress in ff.run_command_with_progress():
                    wm_remover.update(progress - wm_remover.n)

            Tiktok.clean_terminal()
            print('\tWATERMARK AS REMOVED!')
        
        if check_existence.is_file() == True:
            os.remove(path_file)

    # executa toda a operação acima
    def exec_operation(url):

        # Retorna o nome do video e o novo nome do video
        [video_original, path_file, path_new_file] = Tiktok.return_video_id(url)

        # Baixa o arquivo passado pelo client
        Tiktok.spin_cursor(1, '[ Starting download ]')
        Tiktok.download_video(url, video_original, path_file)

        # Com base na desestruturação pega os valores e passa como parametros para a remoção de marca d'agua
        Tiktok.spin_cursor(5, '[ Starting Remove Watermark ]')
        Tiktok.remove_watermark(path_file, path_new_file)

    # Função principal onde iniciara a operação
    def main():
        user = input('Link do video: ')

        url = requests.get(user)
        # Link https://vm.tiktok.com/ZMNxFJMnb/?k=1
        Tiktok.clean_terminal()
        
        Tiktok.exec_operation(url.url)