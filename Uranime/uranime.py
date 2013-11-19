from xdm.plugins import *
import datetime
from lib import requests
import json
import re
from lib.dateutil.parser import parser as dateParser

class Uranime(Provider):
    version = "0.2"
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
        url = 'http://groenlid.no-ip.org/api/search'
        payload['q'] = term
        r = requests.get(url, params=payload)
        
        log('uranime search url ' + r.url)
        
        searchresult = r.json() #json.loads(r.text)
        
        log("content from request: {}".format(r.text))

        # This is to support the old api
        for item in searchresult:
            log("found item: {}".format(item))

        log("%s found %s anime" % (self.name, self.progress.count))

        return rootElement

