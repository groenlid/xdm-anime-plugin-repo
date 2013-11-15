from xdm.plugins import *
import datetime
from lib import requests
import re
from lib.dateutil.parser import parser as dateParser

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
        
        log('uranime search url ' + r.url)
        log(r.text)
        log("%s found %s anime" % (self.name, self.progress.count))

        return rootElement

