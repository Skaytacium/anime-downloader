from trackma.engine import Engine
from trackma.accounts import AccountManager
from anime_downloader.watch import Watcher

import json

class APIHandler:
	"""
	The class used to communicate with Trackma.
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

	def __init__(self, accountnum=1):
		"""
		Defaults to the first account.
		"""
		self.watch = Watcher()
		self.accs = dict(AccountManager().get_accounts())
		self.engine = Engine(self.accs.get(accountnum))
		self.engine.start()
		self.tList = list(self.engine.get_list())
		with open(self.watch.WATCH_FILE, 'r') as watch_file:
			self.adList = list(json.load(watch_file))
			watch_file.close()
		self._sort_lists()

	def _sort_lists(self, key="mal_ID"):
		"""
		Sorts lists for easier comparision.\n
		Called on initializing the class.
		Mutilates the lists.
		"""
		self.adList.sort(key=lambda val: val[key])
		self.tList.sort(key=lambda val: val[self.comparision[key]])

	def _equalize_lists(self, format=False):
		"""
		Strips both the lists to the common categories and returns it
		as two sublists with the animedl list being first.
		"""
		tempList = [[], []]

		for i in range(len(self.tList)):
			entry = [{}, {}]
			for cat in self.comparision:
				
				entry[0][self.comparision[cat] if format else cat] = self.adList[i][cat]

				entry[1][
					self.comparision[cat] if format else cat
				] = "planned" if self.tList[i][
					self.comparision[cat]
				] == "plan_to_watch" else self.tList[i][
					self.comparision[cat]
				]
			
			tempList[0].append(entry[0])
			tempList[1].append(entry[1])
		return tempList

	def _stage_changes(self, preference=True):
		"""
		Returns the modified items in the animedl list (compares to Trackma).\n
		Replaces it with the Trackma entry, to reverse this
		set preference to False.
		"""
		(sadList, stList) = self._equalize_lists()
		tempList = []
		for i in range(len(stList)):
			if (sadList[i] != stList[i]):
				tempList.append((sadList[i] if preference else stList[i]))
		return tempList
	
	def add_staged_to_trackma(self):
		"""
		Updates the Trackma queue.
		"""
		qList = self._stage_changes()
		for item in qList:
			self.engine.get_show_info(item["mal_ID"])

	"""
	{
		Trackma List {
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
		},
		AnimeDL List {
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
	}
	"""

api = APIHandler()
print(api._stage_changes())