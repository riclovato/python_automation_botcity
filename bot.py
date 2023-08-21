
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
from botcity.maestro import *

user_dir = "C:/Users/riicl/AppData/Roaming/Mozilla/Firefox/Profiles/bacw97z8.default-release"
entrada = 'Você poderia gerar no formato json com nome "produtos" os dados de 3 produtos eletrôncios ' \
          'contendo as informações de nome, categoria, codigo, identificador, descricao, preço e quantidade? '


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
    bot.wait(10000)
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
    
    if bot.find( "fakturama_logo2", matching=0.97, waiting_time=120000):
        for index, linha in data_frame.iterrows():
            nome = linha["nome"]
            categoria = linha["categoria"]
            codigo = linha["codigo"]
            identificador = linha["identificador"]
            descricao = linha["descricao"]
            preco = str(linha["preco"]).replace('.',',')
            preco_custo = str(linha["preco"]  * 0.6).replace('.',',')
            estoque = linha["quantidade"]
            
            if bot.find( "new_product2", matching=0.97, waiting_time=10000):
                bot.click()
                bot.wait(1000)
           
            if bot.find( "item_number2", matching=0.97, waiting_time=10000): 
                bot.click_relative(150, 5)
                bot.kb_type(str(index))
                bot.tab()

                #Nome
                bot.paste(nome)
                bot.tab()

                # Category
                bot.paste(categoria)
                bot.tab()

                #GTIN
                bot.paste(codigo)
                bot.tab()

                #Supplier code
                bot.paste(identificador)
                bot.tab()

                #Description
                bot.paste(descricao)
                bot.tab()

                #Preço
                bot.control_a()
                bot.paste(preco)
                bot.tab()

                #Cost Price
                bot.control_a()
                bot.paste(preco_custo)
                bot.tab()

                #Allowance
                bot.tab()

                #Vat
                bot.tab()

                #Stock
                bot.control_a()
                bot.paste(estoque)


                if bot.find( "saveButton2", matching=0.97, waiting_time=10000):
                    bot.click()
                    bot.wait(1000)
                    print('Sucesso!')
                    bot.control_w()
        bot.wait(2000)
        bot.alt_f4()
        


def main():
   maestro = BotMaestroSDK().from_sys_args()
   execution = maestro.get_execution()

   maestro.alert(
       task_id=execution.task_id,
       title="Inicio do processo",
       message='Processo de casdastro dos produtos foi iniciado!',
       alert_type = AlertType.INFO
   )
   maestro.finish_task(
        task_id=execution.task_id,
        message="Processo Finalizado",
        status=AutomationTaskFinishStatus.SUCCESS
   )

   dados_produtos=(coleta_dados_produtos())
   cadastra_produtos(dados_produtos)


if __name__ == "__main__":
    main()












