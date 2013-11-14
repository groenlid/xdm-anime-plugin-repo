from xdm.plugins import *
import datetime
import xml.etree.ElementTree as ET
from lib import requests
import re
from lib.dateutil.parser import parser as dateParser

import uranime

class Uranime(Provider):
    version = "0.1"
    identifier = "de.lad1337.uranime"
    _tag = 'uranime'
    _additional_tags = ['anime']
    single = True
    types = ['de.lad1337.anime']
    _config = {'enabled': True}
    config_meta = {'plugin_desc': 'Anime info from http://urani.me.'}


    def searchForElement(self, term=''):
        self.progress.reset()
        
        mt = MediaType.get(MediaType.identifier == 'de.lad1337.anime')
        mtm = common.PM.getMediaTypeManager('de.lad1337.anime')[0]
        rootElement = mtm.getFakeRoot(term)
        payload = {}
        url = 'http://api.urani.me/search'
        payload['q'] = term
        r = requests.get(url, params=payload)
        
        log('tgdb search url ' + r.url)
        root = ET.fromstring(r.text.encode('utf-8'))

        #baseImgUrlTag = root.find('baseImgUrl')
        #if baseImgUrlTag is not None:
        #    base_url = baseImgUrlTag.text
        #else:
        #    base_url = "http://thegamesdb.net/banners/"

        #for curGame in root.getiterator('Game'):
        #    self._createGameFromTag(curGame, base_url, rootElement)

        log("%s found %s games" % (self.name, self.progress.count))

        return rootElement

