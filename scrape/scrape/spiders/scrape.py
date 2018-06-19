import scrapy


class ALSpider(scrapy.Spider):
    name = "AL"
    url_prefix = 'http://amazinglanka.com'

    urlList = ['/wp/panduwasnuwara/']
    urlSet = set(urlList)
    visited = []

    skip = '/wp/heritage'

    def start_requests(self):
        yield scrapy.Request(url=self.url_prefix + self.urlList[0], callback=self.parse)

    def parse(self, response):
        self.visited.append(response.url.replace(self.url_prefix, ''))
        print('=========', response.url, 'crawl')
        for a in response.css('a::attr(href)').extract():
            a = a.replace('http://amazinglanka.com', '')
            if '/wp/' in a and '.jpg' not in a and '#' not in a and a not in self.skip:
                self.urlSet.add(a)
                self.urlList.append(a)

        # write the file here
        with open('out/' + response.url.replace(self.url_prefix, '').replace('/', '')[2:], 'a') as file:
            file.write('title:\n' + str(response.css('h1::text').extract()) + '\n\n')

            ratebox = response.css('div.rate-box')
            if len(ratebox) > 0:
                file.write('Rating:\n' + str(ratebox.css('strong::text').extract()) + '\n\n')

            file.write('Content:\n\n' + str(('\n').join(response.css('p::text').extract())))

            file.write('\n\nImages:\n')
            for img in response.css('div.post-entry').css('img::attr(src)').extract():
                if '/plugins/' not in img:
                    file.write(img + '\n')

        for x in self.urlList:
            if x not in self.visited:
                if 'p=' in x:
                    self.visited.append(x)
                # print(self.visited)
                print('---- call again', x, len(self.visited))
                yield scrapy.Request(url=self.url_prefix + x, callback=self.parse, dont_filter=True)
                break
        else:
            for i in self.urlSet:
                with open('somefile.txt', 'a') as the_file:
                    the_file.write(i + '\n')
            print('============================ done ====================')
