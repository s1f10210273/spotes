def makeTrack(current_playing):
    if current_playing is None:
        return 0
    elif current_playing["currently_playing_type"] == "episode":
        return 1


    track_name = current_playing['item']['name']
    artist_name = current_playing['item']['artists'][0]['name']
    track_url = current_playing['item']['external_urls']['spotify']

    album_name = current_playing['item']['album']['name']
    album_artist = current_playing['item']['album']['artists'][0]['name']
    album_url = current_playing['item']['album']['external_urls']['spotify']
    jacket_url = current_playing['item']['album']['images'][0]['url']

    count=1
    while(True):
        try:
            artist_name+=", "+current_playing['item']['artists'][count]['name']
            count+=1
        except IndexError:
            break

    count=1
    while(True):
        try:
            album_artist+=", "+current_playing['item']['album']['artists'][count]['name']
            count+=1
        except IndexError:
            break

    track_data = {
        'track_name': track_name,
        'artist_name': artist_name,
        'track_url': track_url,
        'album_name': album_name,
        'album_artist': album_artist,
        'album_url': album_url,

    }
    
    return track_data, jacket_url

def makeUser(user_data):
    user_data = {
        'name': user_data['display_name'],
        'id' : user_data['id'],
        'icon': user_data['images'][0]['url'],
    }
    
    return user_data




def makePlay(track_data):
    if track_data is None:
        return 0
    base = track_data["items"]
    track_name_lst = []
    count=1
    while(True):
        try:
            track_name_lst.append(base[count]["name"])
            count+=1
        except IndexError:
            break

    artist_name_lst = []
    count=1
    while(True):
        try:
            artist_name_lst.append(base[count]["artists"][0]["name"])
            count+=1
        except IndexError:
            break

    track_url_lst = []
    count=1
    while(True):
        try:
            track_url_lst.append(base[count]['external_urls']['spotify'])
            count+=1
        except IndexError:
            break

    jacket_url_lst = []
    count=1
    while(True):
        try:
            jacket_url_lst.append(base[count]['album']['images'][0]['url'])
            count+=1
        except IndexError:
            break


    #twitterの投稿作成
    tweet = "https://twitter.com/share?text=Spotifyで最近聴いてる曲ランキング！！%0a%0a"
    for a, b, c in zip([1,2,3],track_name_lst[0:3],artist_name_lst[0:3]):
        tweet += str(a) + "位::" + b + "-" + c + "%0a"
    tweet += "%0a" + track_url_lst[0] + "%0a"

    track_data = {
        "data" : zip(track_name_lst,artist_name_lst,track_url_lst,jacket_url_lst),
        "data2" : tweet,
    }
    return track_data


def makePlaylst(track_data):
    if track_data is None:
        return 0
    track_uri_lst = []
    count=1
    while(True):
        try:
            track_uri_lst.append(str(track_data["items"][count]["uri"]))
            count+=1
        except IndexError:
            break
    return track_uri_lst
