import json
from bs4 import BeautifulSoup
import requests
import re

#GithubのAPIを使ってユーザー情報とレポジトリ情報をとる
class GithubScraper:

    def __init__(self, url):
        self.url = url
        self.user = None

    #ユーザー情報をスクレイプし、紐付いているuserに保存
    def scrape_user_info(self):

        html_content = requests.get(self.url)
        html_code = html_content.text

        user_json = json.loads(html_code)
        name = user_json["name"]
        login_id = user_json["login"]
        email = user_json["email"]
        location = user_json["location"]
        repos_url = user_json["repos_url"]
        user1 = User(name, login_id, email, location, repos_url)

        self.user = user1

    #対象のユーザーのレポジトリの情報をスクレイプし、
    #レポジトリ情報を表したdictのリストを、user.repos に格納する
    def scrape_repos(self):

        self.scrape_user_info()

        repos_url_from_github = self.user.repos_url

        html_content_of_repos = requests.get(repos_url_from_github)
        html_code_of_repos = html_content_of_repos.text
        html_content_of_repos_split = list(set(html_code_of_repos.split(",")))

        return_reposurl = ""

        for element in html_content_of_repos_split:
            if element.split(":")[0].replace('"',"") == "repos_url":
                return_reposurl = element

        result = return_reposurl[13:].replace('"',"")

        html_content_of_result = requests.get(result)
        html_code_of_result = html_content_of_result.text
        json_of_result = json.loads(html_code_of_result)

        self.user.repos = json_of_result


    def get_user(self):

        return self.user

#Githubのユーザーを表す
class User:

    def __init__(self, name, login_id, email, location, repos_url):
        self.name = name
        self.login_id = login_id
        self.email = email
        self.location = location
        self.repos_url = repos_url


githubscraper1 = GithubScraper("https://api.github.com/users/RaNxxx")

githubscraper1.scrape_repos()

#githubscraper1.userの後ろに、取りたい情報を指定すると自動的にクロールすることが可能
print(githubscraper1.user.email)
