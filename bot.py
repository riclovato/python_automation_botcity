"""
passos:
 - acessar página web do FlowGPT e inicar chat
 - gerar os dados no formato JSON contendo as informações de produtos aleatórios
 - extrair os dados da página web
 - tratar o conteúdo que foi extraído no formato JSON e converter os dados para uma planilha do Excel utilizando pandas
 - utilizar os dados para fazer o cadastro de todos os produtos no aplicativo desktop 'Fakturama'
"""
import pandas
import pandas as pd
from botcity.web import WebBot, Browser, By
from botcity.web.browsers.firefox import default_options
from botcity.core import DesktopBot

user_dir = "C:/Users/riicl/AppData/Roaming/Mozilla/Firefox/Profiles/bacw97z8.default-release"
entrada = 'Você poderia gerar no formato json com nome "produtos" os dados de 3 produtos eletrôncios ' \
          'contendo as informações de nome, categoria, código, identificador,preço e quantidade? '


def coleta_dados_produtos():
    # iniciando o webBot
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.FIREFOX
    bot.driver_path = "C:/temp/Python/botcity/geckodriver.exe"

    #Configurando opções customizadas
    def_options =default_options(headless=bot.headless, user_data_dir=user_dir)
    bot.options = def_options

    #Acessando o site para iniciar o chat
    bot.browse("https://flowgpt.com/chat")
    bot.maximize_window()
    bot.wait(2000)
    input_texto = bot.find_element(selector="#scrollableDiv > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)",
                                   by=By.CSS_SELECTOR)
    input_texto.send_keys(entrada)
    botao_enviar = bot.find_element(selector="#scrollableDiv > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > button:nth-child(2)",
                                    by=By.CSS_SELECTOR)
    botao_enviar.click()

    bot.wait(3000)
    while botao_enviar.get_attribute("disabled") == "true":
        print('Aguardando os dados serem gerados ...')
        bot.wait(2000)

    dados = bot.find_element("language-json", By.CLASS_NAME).get_attribute("textContent")
    print(dados)

    dados = pd.read_json(dados)
    df = pd.json_normalize(dados["produtos"])
    print(df)

    df.to_excel("produtos.xlsx",index=False)

    bot.wait(2000)
    bot.stop_browser()

    return df

def cadastra_produtos(data_frame: pandas.DataFrame):
    bot = DesktopBot()

    bot.execute("C:/Fakturama2/Fakturama.exe")


def main():
   dados_produtos=(coleta_dados_produtos())
   cadastra_produtos(dados_produtos)


if __name__ == "__main__":
    main()