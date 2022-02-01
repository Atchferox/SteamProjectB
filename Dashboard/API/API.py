from lib2to3.pytree import convert
import requests
from PIL import Image
from io import BytesIO
import json


def get_appid(name: str):
    '''Haalt appid bij naam van game'''
    f = open('API/appids.json')
    dic = json.load(f)
    try:
        appid = dic[f'{name}']
    except KeyError:
        return 730
    f.close()
    return appid


def get_game_info(appid: int):
    r = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={appid}')
    r = r.json()
    prijs = r['price']
    prijs = (int(prijs) / 100)

    tags = r['tags']
    if len(tags) == 1 or len(tags) == 2:
        genrelist = list(tags.keys())[:len(tags)]
    else:
        genrelist = list(tags.keys())[:3]
    genres = ", ".join(genrelist)

    return prijs, genres


def game_list():
    f = open('API/appids.json')
    dic = json.load(f)
    all_games_list = []

    for i in dic:
        all_games_list.append(i)
    all_games_list.sort()
    return all_games_list


def get_steamspy(appid: int, data: str):
    """
    Fetches requested data from Steamspy. \n\n
    Possible data: \n
    developer; str \n
    publisher; str  \n
    reviews; tuple of int \n
    average_forever; in minutes, int \n
    average_2weeks; in minutes, int \n
    median_forever; in minutes, int \n
    median_2weeks; in minutes, int \n
    price; in cents, str \n
    initial_price; in cents, str \n
    ccu; peak concurrent players yesterday in int \n
    languages; str of languages seperated by commas \n
    owners; str of estimate of owners
    tags; dictionary of tags    
    """
    r = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={appid}')
    r = r.json()
    if data == "reviews":  # if statement since reviews is the only 'special' data
        pos = r['positive']
        neg = r['negative']

        return pos, neg
    else:
        try:
            return_data = r[data]
            return return_data
        except KeyError:  # throws an error if the data variable is not a valid choice
            raise KeyError("Requested data not found")


def get_status(steamid: int):
    response = requests.get(
        f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=F7CD5F6E51D9114EC9D9C44EEBCA6FF7&steamids={steamid}")
    data = response.json()
    userstatus = data["response"]["players"][0]["personastate"]

    if userstatus == 0:
        return 'Offline'
    if userstatus == 1:
        return 'Online'
    if userstatus == 2:
        return 'Busy'
    if userstatus == 3:
        return 'Away'
    if userstatus == 4:
        return 'Snooze'
    if userstatus == 5:
        return 'Looking to Trade'
    if userstatus == 6:
        return 'Looking to play'


def get_steamlvl(steamid: int):
    r = requests.get(
        f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=F7CD5F6E51D9114EC9D9C44EEBCA6FF7&steamid={steamid}")
    r = r.json()
    return r['response']['player_level']


def top100games():
    """
    Fetches the top 100 games on steam in the past 2 weeks as list
    """
    r = requests.get('https://steamspy.com/api.php?request=top100in2weeks')
    data = r.json()
    listofgames = []
    listofids = []

    for key in data:
        # Puts the name of the game in listofgames
        listofgames.append(data[key]['name'])
        listofids.append(data[key]['appid'])

    return listofgames[:15], listofids[:15]


def get_steamid(vanity: str):
    r = requests.get(
        f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=F7CD5F6E51D9114EC9D9C44EEBCA6FF7&vanityurl={vanity}')
    data = r.json()
    try:
        steamid = data['response']['steamid']
    except KeyError:
        return 76561198333498208
    return steamid


def get_friends(steamid: int):
    """
    Fetches list of given users friends' names
    """
    r = requests.get(
        f'https://api.steampowered.com/ISteamUser/GetFriendList/v1/?steamid={steamid}&key=2FA40FBA36691E988C1AC28FCDAE2545')
    r = r.json()

    friends = r["friendslist"]["friends"]
    friendids = [friend["steamid"] for friend in friends[:20]]  # List comprehension to get a list of IDs
    string = ",".join(friendids)  # for API CALL
    userdata = requests.get(
        f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?steamids={string}&key=2FA40FBA36691E988C1AC28FCDAE2545')
    userdata = userdata.json()
    names = [player["personaname"] for player in userdata["response"]["players"]]  # List comprehension to get a list of names

    i = 0
    name_steamid = dict(zip(names, friendids))

    return names, name_steamid


def get_games(steamid: int):
    """
    Fetches list of given users' games, returns list of gameids
    """
    r = requests.get(
        f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?steamid={steamid}&key=2FA40FBA36691E988C1AC28FCDAE2545&include_appinfo=true&include_played_free_games=true')
    r = r.json()
    try:
        gameslist = r["response"]["games"]

    except KeyError:
        gamenames = None
        gameid = None
        playingtime = None
        return gamenames, gameid, playingtime

    sortedgames = sorted(gameslist, key=lambda d: d["playtime_forever"], reverse=True)

    # laat de 10 meest gespeelde games zien
    gameids = [game["appid"] for game in sortedgames[:10]]
    gamenames = [gamename["name"] for gamename in sortedgames[:10]]
    playingtime = [playtime["playtime_forever"] for playtime in sortedgames[:10]]

    return gameids, gamenames, playingtime


def get_header(appid: int):
    """
    Fetches game header from steam API. \n
    Returns header as base64 bytes
    """
    r = requests.get(f'https://store.steampowered.com/api/appdetails/?appids={appid}')
    r = r.json()

    url = r[str(appid)]['data']['header_image']
    background = requests.get(url)
    img = Image.open(BytesIO(background.content))
    png_bio = BytesIO()
    img.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()
    return png_data


def get_user_game_stats(appid, steamid):
    r = requests.get(
        f'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key=F7CD5F6E51D9114EC9D9C44EEBCA6FF7&steamid={steamid}&appid={appid}')
    r = r.json()
    return


def get_average_playtime(appid: int):

    data = get_steamspy(appid, 'average_2weeks')
    time_format = convert_min_to_hour(data)
    return time_format


def convert_min_to_hour(minutes):
    import time
    time_seconds = minutes*60
    time_format = time.strftime('%H uur en %M minuten', time.gmtime(time_seconds))
    return time_format


def get_estimate_owners(appid: int):
    data = get_steamspy(appid, 'owners')
    return data
