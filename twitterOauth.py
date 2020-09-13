from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import urllib
import webbrowser

request_token = dict()

def getRequestToken(consumer_key,consumer_secret):

    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = ""

    twitter = OAuth1Session(consumer_key, consumer_secret)

    response = twitter.post(
        "https://api.twitter.com/oauth/request_token",
        params={'oauth_callback': oauth_callback}
    )

    # responseからリクエストトークンを取り出す
    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    # リクエストトークンから連携画面のURLを生成
    authenticate_url = "https://api.twitter.com/oauth/authenticate"
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])

    print(authenticate_endpoint)

    webbrowser.open(authenticate_endpoint)            # ブラウザで認証ページを開く
    return request_token


def getAccessToken(pin, consumer_key, consumer_secret, request_token):
    twitter = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=request_token['oauth_token'],
        resource_owner_secret=request_token['oauth_token_secret'],
    )

    response = twitter.post(
        "https://api.twitter.com/oauth/access_token",
        params={'oauth_verifier': pin}
    )

    # responseからアクセストークンを取り出す
    access_token = dict(parse_qsl(response.content.decode("utf-8")))

    print(access_token)
    return access_token
