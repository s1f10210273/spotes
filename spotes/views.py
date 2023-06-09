from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import reverse
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI, SPOTIFY_CLIENT_SECRET
import requests
import json
from .getStatusCode import processStatusCode
from .editJSONData import makeTrack, makeUser, makePlay, makePlaylst



# Create your views here.
def index(request):
    return render(request, 'spotes/index.html')


def spotify_login(request):
    auth_url = 'https://accounts.spotify.com/authorize'
    scopes = [
        'user-top-read',
        'user-read-currently-playing',
        'playlist-modify-private',
        'playlist-modify-public'
    ]
    scope = ' '.join(scopes)
    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': "https://spoti-quct.onrender.com/spotes/callback/",
        'scope': scope,
    }
    return redirect(f"{auth_url}?{urlencode(params)}")

def callback(request):
    code = request.GET.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "https://spoti-quct.onrender.com/spotes/callback/",
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(token_url, params)
    data = json.loads(response.text)
    access_token = data['access_token']
    request.session["access_token"] = access_token

    return redirect(reverse('play'))


def home(request):
    try:
        # アクセストークンの取得
        access_token = request.session["access_token"]
        headers = {'Authorization': 'Bearer ' + access_token,
                    'Accept-Language': 'ja'}
    except:
        # アクセストークンがない場合はログインページにリダイレクト
        return redirect(reverse('login'))

    # Spotify APIから現在再生中のトラック情報を取得
    track_data = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    track_error = processStatusCode(track_data.status_code) + " - track_data"

    if track_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、トラック情報とジャケットURLを作成
        track_data = track_data.json()
        track_data, jacket_url = makeTrack(track_data)
    elif track_data.status_code == 401:
        # ステータスコードが401の場合は認証エラーであるため、ログインページにリダイレクト
        return redirect(reverse('login'))
    else:
        # それ以外のステータスコードの場合はジャケットURLをNoneに設定
        jacket_url = None

    if track_data == 1:
        # track_dataが1の場合はポッドキャストが再生中であることを示すエラーメッセージを設定
        track_error = 'Podcast is playing.'

    # Spotify APIからユーザー情報を取得
    user_data = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_error = processStatusCode(user_data.status_code) + " - user_data"

    if user_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、ユーザー情報を作成
        user_data = user_data.json()
        user_data = makeUser(user_data)

    # コンテキストに必要なデータを追加
    context = {
        'track_data': track_data,
        'bgImageURL': jacket_url,
        'user_data': user_data,
        'track_error': track_error,
        'user_error': user_error,
    }

    # レンダリングするテンプレートとコンテキストを指定してレスポンスを返す
    return render(request, 'spotes/home.html', context)


def play(request):
    try:
        # アクセストークンの取得
        access_token = request.session["access_token"]
        headers = {'Authorization': 'Bearer ' + access_token,
                'Accept-Language': 'ja'}
    except:
        # アクセストークンがない場合はログインページにリダイレクト
        return redirect(reverse('login'))

    # Spotify APIから現在再生中のトラック情報を取得
    track_data = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    track_error = processStatusCode(track_data.status_code) + " - track_data"

    if track_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、トラック情報とジャケットURLを作成
        track_data = track_data.json()
        track_data= makePlay(track_data)

    elif track_data.status_code == 401:
        # ステータスコードが401の場合は認証エラーであるため、ログインページにリダイレクト
        return redirect(reverse('login'))
    else:
        # それ以外のステータスコードの場合はジャケットURLをNoneに設定
        jacket_url = None

    if track_data == 1:
        # track_dataが1の場合はポッドキャストが再生中であることを示すエラーメッセージを設定
        track_error = 'Podcast is playing.'

    # Spotify APIからユーザー情報を取得
    user_data = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_error = processStatusCode(user_data.status_code) + " - user_data"

    if user_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、ユーザー情報を作成
        user_data = user_data.json()
        user_data = makeUser(user_data)

    # コンテキストに必要なデータを追加
    context = {
        'data': track_data,
        'user_data': user_data,
        'track_error': track_error,
        'user_error': user_error,
    }

    # レンダリングするテンプレートとコンテキストを指定してレスポンスを返す
    return render(request, 'spotes/play.html', context)



def addplay(request):
    try:
        # アクセストークンの取得
        access_token = request.session["access_token"]
        headers = {'Authorization': 'Bearer ' + access_token,
                'Accept-Language': 'ja'}
    except:
        # アクセストークンがない場合はログインページにリダイレクト
        return redirect(reverse('login'))

    # Spotify APIから現在再生中のトラック情報を取得
    track_data = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    track_error = processStatusCode(track_data.status_code) + " - track_data"

    if track_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、トラック情報とジャケットURLを作成
        track_data = track_data.json()
        track_data= makePlay(track_data)

    elif track_data.status_code == 401:
        # ステータスコードが401の場合は認証エラーであるため、ログインページにリダイレクト
        return redirect(reverse('login'))
    else:
        # それ以外のステータスコードの場合はジャケットURLをNoneに設定
        jacket_url = None

    if track_data == 1:
        track_error = 'Podcast is playing.'

    # Spotify APIからユーザー情報を取得
    user_data = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_error = processStatusCode(user_data.status_code) + " - user_data"

    if user_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、ユーザー情報を作成
        user_data = user_data.json()


    url = "https://api.spotify.com/v1/users/" + user_data["id"] + "/playlists"
    headers = {'Authorization': 'Bearer ' + access_token,
            "Content-Type": "application/json"}
    data = {
        "name": "最近聴いてる曲リスト",
        "description": "最近聴いてる曲のリストです",
        "public": False
    }
    responce = requests.post(url, headers=headers, json=data)


    # Spotify APIから現在再生中のトラック情報を取得
    track_data = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    track_error = processStatusCode(track_data.status_code) + " - track_data"

    if track_data.status_code == 200:
        # ステータスコードが200の場合はJSONレスポンスを取得し、トラック情報とジャケットURLを作成
        track_data = track_data.json()
        track_data= makePlaylst(track_data)

    else:
        # ステータスコードが401の場合は認証エラーであるため、ログインページにリダイレクト
        return redirect(reverse('login'))


    url = "https://api.spotify.com/v1/playlists/" + responce.json()["id"] + "/tracks"
    headers = {'Authorization': 'Bearer ' + access_token,
            "Content-Type": "application/json"}
    json = {
        "uris": track_data
    ,
        "position": 0
    }
    er = requests.post(url, headers=headers, json=json)

    # コンテキストに必要なデータを追加
    context = {
        'error': "https://open.spotify.com/playlist/" + responce.json()["id"],
        'track_error': track_error,
        'user_error': user_error,
    }

    return render(request, 'spotes/addplay.html', context)

def spotify_logout(request):
    access_token = request.session["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.delete("https://accounts.spotify.com/api/token", headers=headers)
    request.session.flush()
    return redirect(reverse('index'))
