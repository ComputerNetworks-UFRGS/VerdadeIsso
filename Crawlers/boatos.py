import scrapy

class BoatosSpider(scrapy.Spider):
    name = 'boatos'
    start_urls = ['https://www.boatos.org/']

    def parse(self, response):
        # Encontrar os itens de notícia na página
        news_items = response.css('.alternative-post.nv-ft-wrap')

        # Iterar sobre os itens e extrair informações
        count = 0
        for item in news_items:
            # Extrair o título da notícia
            news_title = item.css('.blog-entry-title.entry-title a::text').get()

            # Verificar se o título contém "RS"
            if news_title and ('RS' in news_title or 'Rio Grande do Sul' in news_title):
                # Incrementar o contador
                count += 1

                # Extrair o URL da notícia
                news_url = item.css('.blog-entry-title.entry-title a::attr(href)').get()

                # Extrair a categoria da notícia
                news_category = item.css('.meta.category a::text').get()

                # Extrair a data da notícia
                news_date = item.css('.meta.date.time::text').get()

                # Extrair o autor da notícia
                news_author = item.css('.meta.author.vcard.last span.author-name.fn a::text').get()

                # Criar um dicionário com os dados extraídos
                news_item = {
                    'title': news_title,
                    'url': news_url,
                    'category': news_category,
                    'date': news_date,
                    'author': news_author
                }

                yield news_item

        # Imprimir o total de notícias encontradas
        self.logger.info("Total de notícias encontradas: %d", count)
