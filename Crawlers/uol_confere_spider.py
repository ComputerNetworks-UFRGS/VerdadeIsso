import scrapy
import json
import re

class UOLSpider(scrapy.Spider):
    name = 'uol_spider'
    start_urls = ['https://noticias.uol.com.br/confere/']
    
    def parse(self, response):
        # Encontrar o script que contém os dados das notícias
        script_data = response.xpath('//script[contains(text(), "itemListElement")]').extract_first()
        if script_data:
            # Extrair o JSON dos dados usando expressão regular
            match = re.search(r'<script type="application/ld\+json">(.*?)</script>', script_data, re.DOTALL)
            if match:
                json_data = match.group(1)
                # Carregar os dados como um objeto JSON
                data = json.loads(json_data)
                count = 0
                # Iterar sobre as notícias e extrair informações
                for item in data:
                    itemListElement = item.get('itemListElement', [])
                    for inner_item in itemListElement:
                        for element in inner_item:
                            news_title = element.get('name', '')
                            news_url = element.get('url', '')

                            # Criar um dicionário com os dados extraídos
                            if 'RS' in news_title:
                                count = count + 1
                                news_item = {
                                    'title': news_title,
                                    'url': news_url
                            }

                            yield news_item
                print("Total de notícias encontradas: ")
                print(count)
            else:
                self.logger.error("No JSON data found in script")
        else:
            self.logger.error("No script data found in the response")
