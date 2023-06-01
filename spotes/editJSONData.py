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
        'icon': user_data['images'][0]['url'],
    }
    
    return user_data




def makePlay(current_playing):
    if current_playing is None:
        return 0
    else:
        album = current_playing['item']["album"]
        track_name = current_playing['item']["name"]
        artist_name = current_playing['item']["artists"][0]["name"]
        track_url = current_playing['item']["external_urls"]["spotify"]

        album_name = album["name"]
        album_artist = album["artists"][0]["name"]
        album_url = album["external_urls"]["spotify"]
        jacket_url = album["images"][0]["url"]

        count = 1
        while True:
            try:
                artist_name += ", " + current_playing['item']["artists"][count]["name"]
                count += 1
            except IndexError:
                break

        count = 1
        while True:
            try:
                album_artist += ", " + album["artists"][count]["name"]
                count += 1
            except IndexError:
                break

        track_data = {
            "track_name": track_name,
            "artist_name": artist_name,
            "track_url": track_url,
            "album_name": album_name,
            "album_artist": album_artist,
            "album_url": album_url,
        }

        return track_data, jacket_url
