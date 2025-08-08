import requests
import config
from datetime import datetime
from colorama import Fore, Style, init
import random
from bs4 import BeautifulSoup
import time

def buscar_clima(cidade, pais):
    API_KEY = config.API_KEY_CLIMA
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade},{pais}&appid={API_KEY}&units=metric&lang=pt_br"
    print(Fore.YELLOW + "\nBuscando informações do clima...")
    try:
        requisicao = requests.get(link)
        requisicao.raise_for_status()
        dados = requisicao.json()
        descricao_clima = dados['weather'][0]['description'].capitalize()
        temperatura = dados['main']['temp']
        sensacao_termica = dados['main']['feels_like']
        temp_min = dados['main']['temp_min']
        temp_max = dados['main']['temp_max']
        umidade = dados['main']['humidity']
        print(Style.BRIGHT + Fore.CYAN + f"\n--- 🌦️  CLIMA ATUAL EM {cidade.upper()}, {pais.upper()} ----------------")
        print(Fore.WHITE + f"  {descricao_clima}")
        print(f"  Temperatura: {Fore.GREEN}{temperatura:.1f}°C")
        print(f"  Sensação Térmica: {Fore.GREEN}{sensacao_termica:.1f}°C")
        print(f"  Mínima / Máxima: {Fore.BLUE}{temp_min:.1f}°C{Fore.WHITE} / {Fore.RED}{temp_max:.1f}°C")
        print(f"  Umidade: {Fore.YELLOW}{umidade}%")
        print(Style.BRIGHT + Fore.CYAN + "--------------------------------------------------\n")
    except requests.exceptions.HTTPError as errh:
        if errh.response.status_code == 404:
            print(Fore.RED + f"Cidade '{cidade}' não encontrada. Verifique o nome e a sigla do país.")
        else:
            print(Fore.RED + f"Erro HTTP: {errh}")
    except Exception as e:
        print(Fore.RED + f"Ocorreu um erro inesperado ao buscar o clima: {e}")

def buscar_fato_historico():
    try:
        agora = datetime.now()
        dia = agora.day
        meses = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
        mes_nome = meses[agora.month]
        url = f"https://pt.wikipedia.org/wiki/{dia}_de_{mes_nome}"
        print(Fore.YELLOW + "Buscando um fato interessante do dia...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        SECOES_PARA_PROCURAR = ['Eventos históricos', 'Feriados e eventos cíclicos', 'Nascimentos', 'Mortes']
        fatos_encontrados = None
        titulo_secao_encontrada = None
        todos_os_h2 = soup.find_all('h2')
        for h2 in todos_os_h2:
            titulo_limpo = h2.get_text(strip=True).replace('[editar]', '').strip()
            if titulo_limpo in SECOES_PARA_PROCURAR:
                lista_fatos = h2.find_next('ul')
                if lista_fatos:
                    fatos_encontrados = [item.get_text(strip=True) for item in lista_fatos.find_all('li')]
                    titulo_secao_encontrada = titulo_limpo
                    break
        if fatos_encontrados:
            fato_do_dia = random.choice(fatos_encontrados)
            print(Style.BRIGHT + Fore.CYAN + f"\n--- 📜 VOCÊ SABIA? ({titulo_secao_encontrada}) -----------")
            print(Style.NORMAL + Fore.WHITE + f"  🗓️  Aconteceu em {dia} de {mes_nome.capitalize()}:")
            print(Style.NORMAL + Fore.WHITE + f"  {fato_do_dia}")
            print(Style.BRIGHT + Fore.CYAN + "--------------------------------------------------\n")
        else:
            print(Fore.RED + "Nenhuma seção de fatos diários foi encontrada na página da Wikipédia de hoje.")
    except Exception as e:
        print(Fore.RED + f"Não foi possível buscar o fato histórico do dia: {e}")

def _buscar_e_exibir_noticias(params):
    API_KEY = config.API_KEY_NOTICIAS
    params['token'] = API_KEY
    params['lang'] = 'pt'
    params['max'] = 3
    link = "https://gnews.io/api/v4/search"
    try:
        response = requests.get(link, params=params)
        response.raise_for_status() 
        dados = response.json()
        artigos = dados.get('articles', [])
        if not artigos:
            print(Fore.WHITE + "  -> Nenhuma notícia encontrada para esta busca.")
            return
        for artigo in artigos:
            print(Fore.WHITE + f"  - {artigo['title']}")
            print(Fore.BLUE + f"    {artigo['url']}\n")
    except Exception as e:
        print(Fore.RED + f"  -> Erro ao buscar notícias: {e}")
    finally:
        time.sleep(1.1)

def buscar_noticias(categorias_escolhidas, cidade_regional):
    for dados_categoria in categorias_escolhidas.values():
        nome_exibicao = dados_categoria['exibicao']
        termo_api = dados_categoria['api']  
        print(Style.BRIGHT + Fore.GREEN + f"\n--- 📰 NOTÍCIAS DE {nome_exibicao.upper()} -----------------")

        print(Fore.CYAN + Style.BRIGHT + "\nInternacional:")
        params_internacional = {'q': termo_api}
        _buscar_e_exibir_noticias(params_internacional)


        print(Fore.CYAN + Style.BRIGHT + "\nBrasil:")
        query_brasil = f'{termo_api} Brasil'
        params_brasil = {'q': query_brasil}
        _buscar_e_exibir_noticias(params_brasil)


        print(Fore.CYAN + Style.BRIGHT + f"\nRegião de {cidade_regional}:")
        query_regional = f'{cidade_regional} {termo_api}'
        params_regional = {'q': query_regional}
        _buscar_e_exibir_noticias(params_regional)
        
    print(Style.BRIGHT + Fore.GREEN + "--------------------------------------------------\n")

if __name__ == "__main__":
    init(autoreset=True)
    agora = datetime.now()
    print(Style.BRIGHT + Fore.MAGENTA + "==================================================")
    print(f"     SEU RESUMO MATINAL - {agora.strftime('%d/%m/%Y %H:%M')} ")
    print(Style.BRIGHT + Fore.MAGENTA + "==================================================")
    cidade_usuario = input("Para qual cidade você gostaria de ver o clima? ")
    pais_usuario = input("Qual a sigla do país (ex: BR, US, PT)? ").strip().upper()
    if cidade_usuario and pais_usuario:
        buscar_clima(cidade_usuario, pais_usuario)
    else:
        print("Cidade ou país inválido.")
    buscar_fato_historico()

    CATEGORIAS_NOTICIAS = {
    '1': {'exibicao': 'Tecnologia', 'api': 'technology'},
    '2': {'exibicao': 'Entretenimento', 'api': 'entertainment'},
    '3': {'exibicao': 'Esportes', 'api': 'sports'},
    '4': {'exibicao': 'Negócios', 'api': 'business'},
    '5': {'exibicao': 'Saúde', 'api': 'health'},
    '6': {'exibicao': 'Ciência', 'api': 'science'},
    '7': {'exibicao': 'Notícias do Mundo', 'api': 'world'},
    '8': {'exibicao': 'Notícias Nacionais', 'api': 'nation'}
}
    
    print(Style.BRIGHT + Fore.CYAN + "\n--- ESCOLHA SUAS CATEGORIAS DE NOTÍCIAS ----------")
    for chave, dados_categoria in CATEGORIAS_NOTICIAS.items():
        print(f"  [{chave}] {dados_categoria['exibicao']}")
    escolhas_str = input("Digite os númros das categorias que deseja (separados por vírgula, ex: 1,3): ")
    categorias_selecionadas = {}
    numeros_escolhidos = escolhas_str.split(',')
    for num in numeros_escolhidos:
        num = num.strip()
        if num in CATEGORIAS_NOTICIAS:
            categorias_selecionadas[num] = CATEGORIAS_NOTICIAS[num]
    if categorias_selecionadas:
        buscar_noticias(categorias_selecionadas, cidade_usuario)
    else:
        print(Fore.YELLOW + "\nNenhuma categoria de notícia válida foi selecionada.")
    input("\nPressione Enter para sair.")