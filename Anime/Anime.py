from xdm.plugins import *
import os

location = os.path.abspath(os.path.dirname(__file__))

class Episode(object):
    number = 0
    title = ''
    special = False
    overview = ''
    screencap_image = ''

    _orderBy = 'number'

    def getTemplate(self):
        fp = os.path.join(location, "episode.ji2")
        with open (fp, "r") as template:
            return template.read()

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

    def getSearchTemplate(self):
	fp = os.path.join(location, "show_search.ji2")
	with open (fp, "r") as template:
		return template.read()

   

class Anime(MediaTypeManager):
    version = "0.3"
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

    def makeReal(self, show, status):
        show.parent = self.root
        show.status = status
        show.save()
        common.Q.put(('image.download', {'id': show.id}))
        for episode in list(show.children):
            episode.save()
            common.Q.put(('image.download', {'id': episode.id}))
        return True    


    def headInject(self):
        return self._defaultHeadInject()

