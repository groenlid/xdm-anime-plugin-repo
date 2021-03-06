from xdm.plugins import *
import requests
from dateutil import parser
from json import dumps

connection_names = {1: "anidb", # aniDB
                    2: "mal", # myanimelist
                    3: "tvdb", # TheTVDB.com
                    }

class Uranime(Provider):
    version = "0.5"
    identifier = "de.uranime.uranime"
    _tag = 'uranime'
    single = True
    types = ['de.uranime.anime']
    _config = {'enabled': True}
    config_meta = {'plugin_desc': 'Anime info from http://urani.me.'}

    _resize_url = "http://urani.me/api/imageresize/"
    _episode_image_url = "http://urani.me/attachments/episodes"
    _search_url = "http://urani.me:3000/api/anime"
    _details_url = "http://urani.me:3000/api/animedetails"

    def searchForElement(self, term=''):
        self.progress.reset()

        mt = MediaType.get(MediaType.identifier == 'de.uranime.anime')
        mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
        rootElement = mtm.getFakeRoot(term)
        payload = {}
        payload['title'] = term
        r = requests.get(self._search_url, params=payload)

        log('uranime search url ' + r.url)

        searchresult = r.json()
        self.progress.total = len(searchresult)

        for item in searchresult:
            self.progress.addItem()
            log("found item: {}".format(item))
            # _request_show = requests.get("%s/%s" % (self._details_url, item["id"]))
            self._createAnime(rootElement, mt, item)

        log("%s found %s anime" % (self.name, self.progress.count))

        return rootElement

    def getElement(self, id, element=None):
        query_id = None
        if element is not None:
            query_id = element.getField('id', self._tag)
        if id:
            query_id = id
        if query_id is None:
            return False

        log("GETELEMENT with id: {}".format(query_id))

        mt = MediaType.get(MediaType.identifier == 'de.uranime.anime')
        mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
        rootElement = mtm.getFakeRoot(str(query_id))
        _request_show = requests.get("%s/%s" % (self._details_url, query_id))
        log("getting info from %s" % _request_show.url)
        self._createAnime(rootElement, mt, _request_show.json())

        for ele in rootElement.decendants:
            if int(ele.getField('id', self._tag)) == int(query_id):
                return ele

        return False

    def _createAnime(self, rootElement, mediaType, item):
        showElement = Element()
        showElement.mediaType = mediaType
        showElement.parent = rootElement
        showElement.type = 'Show'
        showElement.setField('title', item['title'].encode('utf-8'), self.tag)
        showElement.setField('id', item['id'], self._tag)
        showElement.setField('poster_image', self._resize_url + item['image'], self.tag)
        showElement.setField('fanart_image', self._resize_url + item['fanart'], self.tag)
        showElement.setField('description', item['desc'], self.tag)
        showElement.setField('runtime', item['runtime'], self.tag)
        showElement.setField('classification', item['classification'], self.tag)

        if 'synonyms' in item:
            showElement.setField(
                'synonyms',
                dumps([s["title"] for s in item['synonyms'] if s["title"].strip()]),
                self.tag
            )

        if "connections" in item:
            for connection in item["connections"]:
                if connection["site_id"] in connection_names:
                    showElement.setField('id', connection["source_id"], connection_names[connection["site_id"]])

        showElement.saveTemp()
        if 'episodes' in item:
            for _episode in item['episodes']:
                episode = Element()
                episode.mediaType = mediaType
                episode.type = 'Episode'
                episode.parent = showElement
                episode.setField('title', _episode['name'], self.tag)
                episode.setField('number', _episode['number'], self.tag)
                episode.setField('overview', _episode['description'], self.tag)
                episode.setField('id', _episode['id'], self.tag)
                episode.setField('airdate', parser.parse(_episode['aired']), self.tag)

                if _episode['image']:
                        episode.setField('screencap_image', self._episode_image_url + '/' + str(_episode['anime_id']) + '/' + _episode['image'], self.tag)

                episode.setField('special', _episode['special'], self.tag)
                episode.saveTemp()

