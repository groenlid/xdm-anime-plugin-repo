
from xdm.plugins import *
import os

location = os.path.abspath(os.path.dirname(__file__))

class Episode(object):
    number = 0
    title = ''
    
    _orderBy = 'number'

    def getTemplate(self):
        return '<li class="bORw"><span class="songPosition bORw">{{this.number}}</span><span class="songTitle bORw">{{this.title}}</span><span class="length bORw">{{this.length}}</span></li>'

class Show(object):
    title = ''
    description = ''
    poster_image = ''
    fanart_image = ''

    _orderBy = 'title'

    def getName(self):
        return self.title

    def getTemplate(self):
	fp = os.path.join(location, "show.ji2")
	with open (fp, "r") as template:
		return template.read()

    def getSearcTemplate(self):
	fp = os.path.join(location, "show_search.ji2")
	with open (fp, "r") as template:
		return template.read()

   

class Anime(MediaTypeManager):
    version = "0.1"
    single = True
    _config = {'enabled': True}
    config_meta = {'plugin_desc': 'Anime support'}
    order = (Show, Episode)
    download = Show
    identifier = 'de.uranime.anime'
    addConfig = {}
    addConfig[Downloader] = [{'type':'category', 'default': None, 'prefix': 'Category for', 'sufix': 'Anime'}]
    addConfig[Indexer] = [{'type':'category', 'default': None, 'prefix': 'Category for', 'sufix': 'Anime'}]
    addConfig[PostProcessor] = [{'type':'path', 'default': None, 'prefix': 'Final path for', 'sufix': 'Anime'}]

    def makeReal(self, show):
        show.parent = self.root
        show.status = common.getStatusByID(self.c.default_new_status_select)
        show.save()
        common.Q.put(('image.download', {'id': show.id}))
        #for season in list(show.children):
        #    season.save()
        #    common.Q.put(('image.download', {'id': season.id}))
        #    for episode in list(season.children):
        #        episode.save()
        #        common.Q.put(('image.download', {'id': episode.id}))
        return True    


    def headInject(self):
        return self._defaultHeadInject()

