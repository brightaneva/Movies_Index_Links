import time
from requests_html import HTMLSession


class Spider:

    def __init__(self):
        self.session = HTMLSession()
        self.headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
        }
        self.base_url = f'https://o2tvseries.co'

    def get_page_response(self,asin,script=None):
        self.script = script
        re = self.session.get(self.base_url + str(asin), headers=self.headers)
        t1_start = time.perf_counter()
        re.html.render(sleep=2,timeout=30, script=self.script, keep_page=True)
        t1_stop = time.perf_counter()
        print("Time: ", t1_stop-t1_start)
        return re

    def get_seasons_page(self):
        nav_pg = '/search/?q=silicon+valley'
        response = self.get_page_response(nav_pg)
        seasons_page = response.html.xpath("/html/body/div[1]/div[2]/ul[1]/li/a")
        return list(seasons_page[0].links)


    def get_episodes_page(self):
        s_pg = self.get_seasons_page()
        response = self.get_page_response(s_pg[0])
        episode_page = response.html.xpath("/html/body/div[1]/div[2]/ul[1]/li[6]/a")
        return list(episode_page[0].links)

    def get_episode(self):
        eps_pg = self.get_page_response(self.get_episodes_page()[0])
        episode =  eps_pg.html.xpath("/html/body/div[1]/div[2]/ul[1]/li[8]/a")[0].links
        #show hidden link
        scripts = """
        () => {
              $(document).ready(function() {
                   $("#stream").click();
                   console.log('hl')
              })
        }
        """
        dwn_pg = self.get_page_response(list(episode)[0],scripts)
        video_link = dwn_pg.html.xpath('/html/body/div[1]/div[2]/ul[1]/div[1]/div/div/video/source')
        return video_link

def main():
    print(Spider().get_episode())

if __name__ == '__main__':
    main()
