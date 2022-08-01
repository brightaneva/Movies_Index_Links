import requests


class Embeded_Movies:

    def __init__(self, tmdb_id=None, imdb_id=None):
        self.tmdb_id = tmdb_id
        self.imdb_id= imdb_id

        self.base_stream_url = f"https://embedworld.xyz/public/embed/"
        self.base_download_url = f"https://embedworld.xyz/public/download/"

    def get_response(self,url):
        return requests.get(url)

    def test_availability(self):
        """if movie or tv show exits?
            return api response
        """
        check_status = self.get_response(f"https://embedworld.xyz/public/api/status?tmdb={self.tmdb_id}&type=movie").json()
        status = [None if check_status["status"] == 'failed' else True]
        print(status)
        return status

    def get_streaming_data(self):
        """ check if movie or series
            exits nd get it link
            streaming link of the
            movie or series
        """
        stream_url = f"{self.base_stream_url}movie?tmdb={self.tmdb_id}" if self.test_availability() is not None else None
        # data = [stream_url if self.test_availabilty() else None]
        return stream_url

    def get_download_data(self):
        """ check if movie or series
            exits nd get it link
            streaming link of the
            movie or series
        """
        stream_url = f"{self.base_download_url}movie?tmdb={self.tmdb_id}"
        data = [stream_url if self.test_availabilty(type) else None]
        return data


class Embeded_Series:

    def __init__(self, season, episode, tv_id):
        self.id = tv_id
        self.season = season
        self.ep = episode

        self.base_stream_url = f"https://embedworld.xyz/public/embed/"
        self.base_download_url = f"https://embedworld.xyz/public/download/"

    def get_response(self,url):
        print(url)
        return requests.get(url)

    #TODO: test availability not working
    def test_availability(self):
        """if movie or tv show exits?
            return api response
        """
        check_status = self.get_response(f"https://embedworld.xyz/public/api/status?tmdb={self.id}&sea={self.season}&epi={self.ep}&type=tv").json()
        status = [False if check_status["status"] == 'failed' else True]
        print(check_status)
        return status

    def get_streaming_data(self):
        """ check if movie or series
            exits nd get it link
            streaming link of the
            movie or series
        """
        stream_url = f"{self.base_stream_url}{self.id}/{self.season}/{self.ep}"
        return stream_url

    def get_download_data(self):
        """ check if movie or series
            exits nd get it link
            streaming link of the
            movie or series
        """
        stream_url = f"{self.base_download_url}{self.id}"
        data = [stream_url if self.test_availabilty() else None]
        return data

    def movie_embed(self):
        pass

    def series_episode_embed(self):
        pass

# def main():
#     Movie = Embeded_Movies(tmdb_id='951535').get_streaming_data()
#     Series = Embeded_Series(season='1',episode='7',tv_id='52814').get_streaming_data()
#     print(Movie)
#     print(Series)


# if __name__ == "__main__":
#     main()
