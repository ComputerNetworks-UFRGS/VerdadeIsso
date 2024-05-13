import scrapy
import json
import re

class AosFatosSpider(scrapy.Spider):
    name = 'aosfatos'
    start_urls = ['https://www.aosfatos.org/noticias/checamos/falso/']

    def parse(self, response):
        # Encontrar os itens de notícia na página
        news_items = response.css('.entry-item-card.entry-content')

        # Iterar sobre os itens e extrair informações
        count = 0
        for item in news_items:
            # Extrair o título da notícia
            news_title = item.css('.entry-item-card-title p::text').get()

            # Verificar se o título contém "RS"
            if news_title and 'RS' in news_title:
                # Incrementar o contador
                count += 1

                # Extrair o URL da notícia
                news_url = response.urljoin(item.css('a::attr(href)').get())

                # Criar um dicionário com os dados extraídos
                news_item = {
                    'title': news_title,
                    'url': news_url
                }

                yield news_item

        # Imprimir o total de notícias encontradas
        print("Total de notícias encontradas: ", count)
