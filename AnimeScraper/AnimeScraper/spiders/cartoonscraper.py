import scrapy


class CartoonscraperSpider(scrapy.Spider):
    name = "cartoonscraper"
    allowed_domains = ["aniwatch.to"]
    start_urls = ["https://aniwatch.to"]


    def parse(self, response):
        home_page = response.css('a ::attr(href)').get()
        if home_page is not None:
            home_page_url = "https://aniwatch.to"+ home_page
            yield scrapy.Request(home_page_url,callback=self.parse_home)
        else:
            print("Error cannot go to the home page of the website")

        
    
    def parse_home(self, response):
        recently_added_page = "https://aniwatch.to"+ response.xpath("//div[@class='float-right viewmore']/a/@href").extract()[1]
        yield scrapy.Request(recently_added_page,callback=self.parse_recently_added)

    def parse_recently_added(self,response):
        # top 4 has description within them rest we have to navigate and fetch from their respective link
        # the above idea was not very optimal so we will now go into each anime respectively
        item_big_4 = response.xpath("//div[@class='flw-item flw-item-big']")
        for bigitem in item_big_4:
            # anime_name = bigitem.xpath("//div[@class='flw-item flw-item-big']").css("div.film-detail").css("h3 a::text").get()
            # anime_description = bigitem.xpath("//div[@class='flw-item flw-item-big']").css("div.film-detail").css("div.description ::text").get()
            # num_episode = bigitem.css("div.film-poster").css("div.tick-item.tick-sub::text").get()
            # duration = bigitem.css("div.film-detail").css("div.fd-infor").css("span.fdi-item.fdi-duration::text").get()

            respective_big_anime_url = 'https://aniwatch.to' + bigitem.css("div.film-poster").css("a ::attr(href)").get()
            yield scrapy.Request(respective_big_anime_url,callback=self.parse_respective_anime)

        items_remaining_36 = response.xpath("//div[@class='flw-item']")
        for items in items_remaining_36:
            respective_36_animes_url = 'https://aniwatch.to' + items.css("div.film-poster").css("a ::attr(href)").get()
            yield scrapy.Request(respective_36_animes_url,callback=self.parse_respective_anime)





    

    def parse_respective_anime(self,response):
        
        yield{
            'Name': response.xpath("//div[@class='anisc-detail']").css("h2 ::text").get(),
            "Genres":response.xpath("//div[@class='anisc-info']").css("div.item.item-list").css("a::text").getall(),
            "Description":response.xpath("//div[@class='anisc-detail']").css("div.film-description").css("div.text::text").get(),
            "Num_episodes":response.xpath("//div[@class='anisc-detail']").css("div.film-stats").css("div.tick").css("div.tick-item.tick-sub::text").get(),
            "Duration":response.xpath("//div[@class='anisc-detail']").css("div.film-stats").css("div.tick").css("span.item::text").getall()[1],
            "Type of episode":response.xpath("//div[@class='anisc-detail']").css("div.film-stats").css("div.tick").css("span.item::text").get(),
            "MAL Score":response.xpath("//div[@class='anisc-info']").css("div.item.item-title")[-3].css("span.name::text").get(),
            "Studios":response.xpath("//div[@class='anisc-info']").css("div.item.item-title")[-2].css("a::text").getall()
        }





        
#book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()

