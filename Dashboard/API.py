import requests
from PIL import Image
from io import BytesIO

def get_reviews(appid: int):
    """
    Fetches positive and negative review amounts from Steamspy. \n
    Returns positive, negative as integers
    """
    r = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={appid}')
    r = r.json()

    pos = r['positive']
    neg = r['negative']

    return pos, neg

def get_background(appid: int):
    """
    Fetches game background from steam API. \n
    Returns img as PIL Image object
    """
    r = requests.get(f'https://store.steampowered.com/api/appdetails/?appids={appid}')
    r = r.json()

    background = r['background']
    img = Image.open(BytesIO(background.content))

    return img

