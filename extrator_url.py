import re

class ExtratorURL:
    def __init__(self, url):
        self.url = self.sanitiza_url(url)
        self.valida_url()

    def sanitiza_url(self, url):
        if type(url) == str:
            return url.strip()
        else:
            return ""

    def valida_url(self):
        if not self.url:
            raise ValueError("A URL está vazia.")

        padrao_url = re.compile("(http(s)?://)?(www.)?bytebank.com(.br)?/cambio")
        match = padrao_url.match(url)
        if not match:
            raise ValueError("A URL não é válida.")

    def get_url_base(self):
        indice_interrogacao = self.url.find("?")
        url_base = self.url[:indice_interrogacao]
        return url_base

    def get_url_parametros(self):
        indice_interrogacao = self.url.find("?")
        url_parametros = self.url[indice_interrogacao:]
        return url_parametros

    def get_valor_parametro(self, parametro_busca):
        indice_parametro = self.get_url_parametros().find(parametro_busca)
        indice_valor = indice_parametro + len(parametro_busca) + 1
        indice_e_comercial = self.get_url_parametros().find("&", indice_valor)
        if indice_e_comercial == -1:
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_e_comercial]
        return valor

    def __len__(self):
        return len(self.url)

    def __str__(self):
        return self.url + "\n\n" + "URL Base: " + self.get_url_base() + "\n" + "URL Parâmetros: " + self.get_url_parametros()

    def __eq__(self, other):
        return self.url == other.url

#######################################################################################################################

import requests
import data_hoje

cotacao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL")
cotacao = cotacao.json()

url = "bytebank.com/cambio?moedaDestino=dolar&quantidade=100&moedaOrigem=real"
extrator_url = ExtratorURL(url)

base = extrator_url.get_url_base()
parametros = extrator_url.get_url_parametros()

valor_quantidade = extrator_url.get_valor_parametro("quantidade")
moeda_origem = extrator_url.get_valor_parametro("moedaOrigem")
moeda_destino = extrator_url.get_valor_parametro("moedaDestino")

print("\n{:=^75} \n".format(" Dados da URL fornecida "))
print(f"URL completa: {url}")
print(f"URL Base :   {base}")
print(f"Parâmetros da URL :   {parametros}")
print(f"\nMoeda de Origem :   {moeda_origem}")
print(f"Moeda de Destino :   {moeda_destino}")
print(f"Quantidade :   {valor_quantidade} unidades da moeda.")

print("\n{:=^75} \n".format(" Conversão de Valores "))

valor_dolar = cotacao["USDBRL"]["bid"]
cotacao_dolar = float(valor_dolar)
print(f"A cotação do Dolar em {data_hoje.hoje()} é R$ {cotacao_dolar:.2f}")
quantidade = int(valor_quantidade)

if moeda_origem == "real" and moeda_destino == "dolar":
    valor_conversao = quantidade / cotacao_dolar
    print(f"\nO valor de R$ {quantidade:.2f} é igual a US$ {valor_conversao:.2f}.")
elif moeda_origem == "dolar" and moeda_destino == "real":
    valor_conversao = quantidade * cotacao_dolar
    print(f"\nO valor de US$ {quantidade} é igual a R$ {valor_conversao:.2f}")
else:
    print(f"\nCâmbio de {moeda_origem} para {moeda_destino} não está disponível.")
