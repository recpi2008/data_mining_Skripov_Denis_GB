import copy
import json
import re
from urllib.parse import quote

import scrapy
from scrapy.http import HtmlResponse

from instaparser.items import InstagramScraperItem


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    template_user_url = "/%s"
    post_getting_url = "/graphql/query/?query_hash=%s&variables=%s"
    post_query_hash = "8c2a529969ee035a5063f2fc8602a0fd"


    def __init__(self, login, password, user_to_parse, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.enc_password = password
        self.user_to_parse = user_to_parse

    def parse(self, response: HtmlResponse, **kwargs):
        token = self.fetch_csrf_token(response.text)
        x_instagram_ajax = self.fetch_x_instagram_ajax(response.text)
        yield scrapy.FormRequest(
            url=self.login_url,
            method="POST",
            formdata={
                "username": self.login,
                "enc_password": self.enc_password,
            },
            headers={
                "X-CSRFToken": token,
                "x-ig-app-id": "936619743392459",
                "x-instagram-ajax": x_instagram_ajax,
            },
            callback=self.user_login,
        )

    def user_login(self, response: HtmlResponse):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("Json decode error")
            print(e)
            return
        except Exception as e:
            print(e)
            return

        if data["authenticated"]:
            for i in self.user_to_parse:

                yield response.follow(
                    self.template_user_url % i,
                    callback=self.parse_data_followers,
                    cb_kwargs={"username": i},

                )

    def parse_data_followers(self, response: HtmlResponse, username: str):
        user_id = self.fetch_user_id(response.text, username)
        url_followers = "https://i.instagram.com/api/v1/friendships/%s/followers/?count=12&search_surface=follow_list_page"
        url_followers = url_followers % user_id
        url_following = "https://i.instagram.com/api/v1/friendships/%s/following/?count=12"
        url_following = url_following % user_id
        yield response.follow(
            url_followers,
            callback=self.parse_followers,
            headers={
                "x-ig-app-id": "936619743392459",
            },
            cb_kwargs={"username": username,
                       'user_id': user_id,
                       }
        )
        yield response.follow(
            url_following,
            callback=self.parse_following,
            headers={
                "x-ig-app-id": "936619743392459",
            },
            cb_kwargs={"username": username,
                       'user_id': user_id,
                       }
        )

    def parse_followers(self, response: HtmlResponse,username,user_id):
        data_f = response.json()

        if data_f.get('next_max_id'):
            max_id = data_f['next_max_id']
            url_posts = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'

            yield response.follow(
                url_posts,
                callback=self.parse_followers,
                headers={
                    "x-ig-app-id": "936619743392459",
                },
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           }
            )
        followers = data_f.get('users')
        for follower in followers:
            name = follower["username"]
            url_d = f"https://instagram.com/{name}/"

            yield response.follow(
                url_d,
                callback=self.id_follower,
                headers={
                    "x-ig-app-id": "936619743392459",
                },
                cb_kwargs={"username": username,
                           "namefollow": name,
                           'user_id': user_id,
                           'follower':follower
                           }
            )

    def id_follower(self, response: HtmlResponse,username,namefollow,user_id,follower):
        id_follower = self.fetch_user_id(response.text, namefollow)
        item = InstagramScraperItem(
            user=username,
            user_id = user_id,
            user_stutus='follower',
            namefollow = namefollow,
            id_follower = id_follower,
            user_photo=follower['profile_pic_url'],
        )
        yield item


    def parse_following(self, response: HtmlResponse,username,user_id):
        data_f = response.json()

        if data_f.get('big_list')== True:
            max_id = data_f['next_max_id']
            url_posts = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&max_id={max_id}'

            yield response.follow(
                url_posts,
                callback=self.parse_following,
                headers={
                    "x-ig-app-id": "936619743392459",
                },
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           }
            )
        followings = data_f.get('users')
        for following in followings:
            name = following["username"]
            url_d = f"https://instagram.com/{name}/"
            yield response.follow(
                url_d,
                callback=self.id_following,
                headers={
                    "x-ig-app-id": "936619743392459",
                },
                cb_kwargs={"username": username,
                           "namefollowing": name,
                           'user_id': user_id,
                           'following': following
                           }
            )


    def id_following(self, response: HtmlResponse,username,namefollowing,user_id,following):
        id_following = self.fetch_user_id(response.text, namefollowing)
        item = InstagramScraperItem(
            user=username,
            user_id = user_id,
            user_stutus='following',
            namefollow = namefollowing,
            id_follower = id_following,
            user_photo=following['profile_pic_url'],
        )
        yield item



    # get token for authorization
    def fetch_csrf_token(self, text):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # rollout_hash ; x_instagram_ajax
    def fetch_x_instagram_ajax(self, text):
        matched = re.search('"rollout_hash":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # get user_id for interesting user
    def fetch_user_id(self, text, username):
        matched = re.search('{"id":"\\d+","username":"%s"}' % username, text).group()
        return json.loads(matched).get("id")

    # encode variables dict
    def make_str_variables(self, variables):
        str_variables = quote(str(variables).replace(" ", "").replace("'", '"'))
        return str_variables

