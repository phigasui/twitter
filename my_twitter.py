#! /usr/local/bin/python3

import requests
from  requests_oauthlib import OAuth1
import json
import pickle
import time


class my_twitter():

    def __init__(self, api_key, api_secret,
                 access_token, access_token_secret):

        self.auth = OAuth1(api_key, api_secret,
                           access_token, access_token_secret)
        self.followers_list = None
        self.following_list = None
        self.followers_ids = None
        self.following_ids = None

        self.followers_id_dict = None
        self.following_id_dict = None


    def get_followers_list(self):
        url = 'https://api.twitter.com/1.1/followers/list.json'

        cursor = -1
        followers_list = []
        while cursor != 0:
            params = {'skip_status': True,
                      'count': 200,
                      'cursor': cursor}
            res = requests.get(url, auth=self.auth, params=params)
            res_json = json.loads(res.text)

            followers_list.extend(res_json['users'])
            cursor = res_json['next_cursor']

        self.followers_list = followers_list


    def get_following_list(self):
        url = 'https://api.twitter.com/1.1/friends/list.json'

        cursor = -1
        following_list = []
        while cursor != 0:
            params = {'skip_status': True,
                      'count': 200,
                      'cursor': cursor}
            res = requests.get(url, auth=self.auth, params=params)
            res_json = json.loads(res.text)

            following_list.extend(res_json['users'])
            cursor = res_json['next_cursor']

        self.following_list = following_list


    def get_followers_ids(self):
        if self.followers_list == None:
            self.get_followers_list()
        self.followers_ids = [follower['id']
                              for follower in self.followers_list]


    def get_following_ids(self):
        if self.following_list == None:
            self.get_following_list()
        self.following_ids = [following['id']
                              for following in self.following_list]


    def get_followers_id_dict(self):
        if self.followers_list == None:
            self.get_followers_list()
        followers_id_dict = {follower['id']: follower
                             for follower in self.followers_list}
        self.followers_id_dict = followers_id_dict


    def get_following_id_dict(self):
        if self.following_list == None:
            self.get_following_list()
        following_id_dict = {follower['id']: follower
                             for follower in self.following_list}
        self.following_id_dict = following_id_dict


    def save_followers(self):
        if self.followers_id_dict == None:
            self.get_followers_id_dict()
        with open('followers_list' + str(time.time()) + '.pkl', 'wb') as f:
            pickle.dump(self.followers_id_dict, f)


    def get_usertimeline(self):
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        res = requests.get(url, auth=self.auth)

        return json.loads(res.text)


    def get_hometimeline(self):
        url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        res = requests.get(url, auth=self.auth)

        return json.loads(res.text)


    def search_tweets(self, word):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        params = {'q': word,
                  # 'since_id': 530704728129556480,
                  # 'max_id': 532722531099496448,
                  'count': 100}
        res = requests.get(url, auth=self.auth, params=params)
        print(res)

        return json.loads(res.text)['statuses']


    def streaming(self):
        url = 'https://stream.twitter.com/1.1/statuses/sample.json'
        res = requests.get(url, auth=self.auth)

        return json.loads(res.text)


    def save_img(url, dir):

        import os
        import urllib.request

        img = urllib.request.urlopen(url)
        f = open(dir + '/' + os.path.basename(url), 'wb')
        f.write(img.read())
        f.close()
        img.close()


    def photo_crawling(self, screen_name):
        import os
        if not os.path.exists(screen_name):
            os.mkdir(screen_name)

        tweets = self.get_user_timeline(screen_name)

        for tweet in tweets:
            if not 'media' in tweet['entities']: continue
            for media in tweet['entities']['media']:
                if media['type'] == 'photo':
                    self.save_img(media['media_url'], screen_name)


    def get_user_timeline(self, screen_name):
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {'screen_name' : screen_name, 'count' : 200}

        res = requests.get(url, auth=self.auth, params=params)

        return json.loads(res.text)


    def update(self, text):
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        params = {'status' : text}

        requests.post(url, auth=self.auth, params=params)


if __name__ == '__main__':

    api_info = json.load(open("api_info.json", 'r'))

    phigasui = my_twitter(**api_info['gashitter'])

    phigasui.save_followers()

    # tweets = []
    # tweets_without_link = []
    # for tweet in data:

    #     if 'retweeted_status' in tweet: continue

    #     tweets.append(tweet['text'])

    #     text = tweet['text']
    #     for url in tweet['entities']['urls']:
    #         text = text.replace(url['url'], '')

    #     for mention in tweet['entities']['user_mentions']:
    #         text = text.replace('@' + mention['screen_name'], '')
    #     tweets_without_link.append(text)

    # print(tweets)
    # print(tweets_without_link)

    # print(','.join(tweets_without_link))

    # word = '飯テロ'

    # # print(streaming(access_token, access_token_secret))

    # for tweet in search_tweets(access_token, access_token_secret, word):
    #     if 'media' in tweet['entities']:
    #         for m in tweet['entities']['media']:
    #             if m['type'] == 'photo':
    #                 print(m)
