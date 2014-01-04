from xdm.plugins import *
from lib import requests

class Uranime(Provider):
    version = "0.3"
    identifier = "de.uranime.uranime"
    _tag = 'uranime'
    _additional_tags = ['anime']
    single = True
    types = ['de.uranime.anime']
    _config = {'enabled': True}
    config_meta = {'plugin_desc': 'Anime info from http://urani.me.'}
    _resize_url = "http://urani.me/api/imageresize/"
    _episode_image_url = "http://urani.me/attachments/episodes"
    _search_url = "http://groenlid.no-ip.org/api/search"
    _details_url = "http://groenlid.no-ip.org/api/animedetails"

    def searchForElement(self, term=''):
        self.progress.reset()
        
        mt = MediaType.get(MediaType.identifier == 'de.uranime.anime')
        mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
        rootElement = mtm.getFakeRoot(term)
        payload = {}
        payload['q'] = term
        r = requests.get(self._search_url, params=payload)
        
        log('uranime search url ' + r.url)
        
        searchresult = r.json()
        self.progress.total = len(searchresult)

        for item in searchresult:
            self.progress.addItem()
            log("found item: {}".format(item))
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
	
        _request_show = requests.get(self._details_url + '/' + str(query_id))
        self._createAnime(rootElement, mt, _request_show.json())
        
        for ele in rootElement.decendants:
            if int(ele.getField('id', self._tag)) == int(query_id):
                return ele
        
        return False	

    def _createAnime(self, rootElement, mediaType, item):
        try:
            showElement = Element.getWhereField(mediaType, 'Show', {'id': item['id']}, self._tag, rootElement)
            log("Found element")
        except Element.DoesNotExist:
            log("Creating new element")
            showElement = Element()
            showElement.mediaType = mediaType
            showElement.parent = rootElement
            showElement.type = 'Show'
        showElement.setField('title', item['title'].encode('utf-8'), self._tag)
        showElement.setField('id', item['id'], self._tag)
        showElement.setField('poster_image', self._resize_url + item['image'], self._tag)
        showElement.setField('fanart_image', self._resize_url + item['fanart'], self._tag)
        
        showElement.saveTemp()
        if 'episodes' in item:
            for _episode in item['episodes']:
                try:
                    episode = Element.getWhereField(mediaType, 'Episode', {'id': _episode['id']}, self._tag, rootElement)
                except Element.DoesNotExist:
                    episode = Element()
                    episode.mediaType = mediaType
                    episode.type = 'Episode'
		        
		episode.parent = showElement
		episode.setField('title', _episode['name'].encode('utf-8'), self.tag)
		episode.setField('number', _episode['number'], self.tag)
		episode.setField('overview', _episode['description'].encode('utf-8'), self.tag)
                episode.setField('id', _episode['id'], self.tag)
                
                if _episode['image']:
                        episode.setField('screencap_image', self._episode_image_url + '/' + str(_episode['anime_id']) + '/' + _episode['image'], self.tag)
        
                if _episode['special']:
                        episode.setField('special', True)
                episode.saveTemp()

