# 🤖 Robô de Resumo Diário em Python

Uma ferramenta de linha de comando que busca informações de múltiplas fontes na internet para criar um resumo matinal personalizado, entregue diretamente no seu terminal.

## ✨ Funcionalidades

-   **Clima em Tempo Real:** Pede ao usuário uma cidade e busca a temperatura, sensação térmica e outras condições atuais usando a API da OpenWeatherMap.
-   **Fato Histórico do Dia:** Usa web scraping para extrair um fato histórico interessante da página da Wikipédia em português correspondente ao dia atual.
-   **Notícias Personalizadas:** Apresenta um menu de categorias (Tecnologia, Esportes, etc.) e permite que o usuário escolha múltiplas áreas de interesse.
-   **Busca Multi-Escopo:** Para cada categoria selecionada, busca e exibe as principais manchetes em nível Internacional, Nacional (Brasil) e Regional (baseado na cidade informada).
-   **Interface Agradável:** Utiliza a biblioteca `colorama` para uma exibição colorida e organizada no terminal.

## 🔧 Tecnologias Utilizadas

-   **Python 3**
-   **Requests:** para todas as chamadas de API e requisições web.
-   **BeautifulSoup4:** para o web scraping da página da Wikipédia.
-   **Colorama:** para a estilização da saída no terminal.
-   **PyInstaller:** para empacotar o projeto em um executável autônomo.

---

## ⚙️ Configuração (Para Rodar do Código-Fonte)

1.  Clone este repositório.
2.  Crie um arquivo chamado `config.py` na raiz do projeto.
3.  Dentro do `config.py`, cole o seguinte e adicione suas chaves de API:
    ```python
    # config.py
    API_KEY_CLIMA = "SUA_CHAVE_DA_OPENWEATHERMAP_AQUI"
    API_KEY_NOTICIAS = "SUA_CHAVE_DA_GNEWS_AQUI"
    ```
4.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```
5.  Execute o script:
    ```bash
    python noticiasclima.py
    ```

---

## 🚀 Como Usar (Versão Executável para Windows)

1.  Vá para a **[Página de Releases](https://github.com/allymonteiro/resumo-diario-python/releases)**.
2.  Baixe o arquivo `noticiasclima.exe`.
3.  **Importante:** Crie o arquivo `config.py` (como ensinado na seção acima) e coloque-o **na mesma pasta** que o `resumo_diario.exe`.
4.  Dê dois cliques no `.exe` e siga as instruções!