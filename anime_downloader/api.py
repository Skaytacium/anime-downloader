from trackma.engine import Engine
from trackma.accounts import AccountManager
from anime_downloader.watch import Watcher

import json

class APIHandler:
    """
    APIHandler is the class used for communicating with Trackma to update
    remote anime lists based on the watch command (for now).
    """
    comparision = {
        "mal_ID": "id",
        "title": "title",
        "episodes_done": "my_progress",
        "watch_status": "my_status",
        "score": "my_score",
        "_len": "total"
    }
    watch = None
    accs = None
    engine = None
    adList = []
    tList = []

    def __init__(self):
        watch = Watcher()
        accs = AccountManager().get_accounts()
        print(accs)
        engine = accs
        engine.start()
        self.tList = list(engine.get_list())
        with open(watch.WATCH_FILE, 'r') as watch_file:
            self.adList = list(json.load(watch_file))

    def sort_lists(self, key="mal_ID"): 
        self.adList.sort(key=lambda val: val[key])
        self.tList.sort(key=lambda val: val[self.comparision[key]])

    def convert_list():
        pass
    
    def stage_changes(self):
        for i in range(len(tList)):
            if (self.adList[i]["mal_ID"] != self.tList[i]["id"]):
                print(self.engine.get_show_info(showid=self.adList[i]["mal_ID"]))
                self.engine.add_show()
                break
    """
    Trackma List
    {
        'id': 24833, 
        'title': 'Ansatsu Kyoushitsu', 
        'total': 22, 
        'my_progress': 22, 
        'my_status': 'completed', 
        'my_score': 7, 
        'url': 'https://myanimelist.net/anime/24833', 
        'aliases': ['Assassination Classroom', '暗殺教室', 'Ansatsu Kyoushitsu'], 
        'my_id': None, 
        'my_start_date': None, 
        'my_finish_date': None, 
        'type': 0, 
        'status': 2, 
        'start_date': None, 
        'end_date': None, 
        'image': 'https://api-cdn.myanimelist.net/images/anime/5/75639l.jpg', 
        'image_thumb': 'https://api-cdn.myanimelist.net/images/anime/5/75639.jpg', 
        'queued': False
    }
    AnimeDL List
    {
        'mal_ID': 24833, 
        'title': 'Ansatsu Kyoushitsu', 
        '_len': 22
        'episodes_done': 22, 
        'watch_status': 'completed', 
        'score': 7, 
        '_timestamp': 1605987725.8867319, 
        'colours': 'green', 
        'url': '4anime', 
        '_fallback_qualities': ['720p', '480p', '360p'], 
        'quality': '720p', 
        '_episode_urls': [[1, 'https://notarealwebsite.illusion/']], 
    }
    """