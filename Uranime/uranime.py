from xdm.plugins import *
import datetime
from lib import requests
import json
import re
from lib.dateutil.parser import parser as dateParser

class Uranime(Provider):
    version = "0.2"
    identifier = "de.uranime.uranime"
    _tag = 'uranime'
    _additional_tags = ['anime']
    single = True
    types = ['de.uranime.anime']
    _config = {'enabled': True}
    config_meta = {'plugin_desc': 'Anime info from http://urani.me.'}
    _resize_url = "http://urani.me/api/imageresize/"

    def searchForElement(self, term=''):
        self.progress.reset()
        
        mt = MediaType.get(MediaType.identifier == 'de.uranime.anime')
        mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
        rootElement = mtm.getFakeRoot(term)
        payload = {}
        url = 'http://groenlid.no-ip.org/api/search'
        payload['q'] = term
        r = requests.get(url, params=payload)
        
        log('uranime search url ' + r.url)
        
        searchresult = r.json()
        self.progress.total = len(searchresult)

        # This is to support the old api
        for item in searchresult:
            self.progress.addItem()
            log("found item: {}".format(item))
            self._createAnime(rootElement, mt, item)

        log("%s found %s anime" % (self.name, self.progress.count))

        return rootElement
    
    def getElement(self, id, element=None):
        log("GETELEMENT with id: {}".format(id))
	mt = MediaType.get(MediaType.identifier == 'de.uranime.anime')
	mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
	rootElement = mtm.getFakeRoot("{}{}".format(self._tag, id))
		

    def _createAnime(self, rootElement, mediaType, item):
        showElement = Element()
        showElement.mediaType = mediaType
        showElement.parent = rootElement
        showElement.type = 'Show'
        showElement.setField('title', item['title'], self._tag)
        showElement.setField('id', item['id'], self._tag)
 	showElement.setField('poster_image', self._resize_url + item['image'], self._tag)
 	showElement.setField('fanart_image', self._resize_url + item['fanart'], self._tag)
   
        showElement.saveTemp()

