from xdm.plugins import *
from xdm.tasks import updateElement
from json import loads
import os

location = os.path.abspath(os.path.dirname(__file__))

class Episode(object):
    number = 0
    title = ''
    special = False
    overview = ''
    screencap_image = ''

    _orderBy = 'number'

    def getSearchTerms(self):
    	return ['%s %02d' % (self.parent.title, self.number)]

        """ The user should be able to choose which anime-synonym to search for
        return ['%s %02d' % (s, self.number) for s in loads(self.parent.synonyms)]
        """


    def getTemplate(self):
        fp = os.path.join(location, "episode.ji2")
        with open (fp, "r") as template:
            return template.read()

    def getName(self):
        return "%s e%02d %s" % (self.parent.getName(), self.number, self.title)

    def getReleaseDate(self):
        return self.airdate

    def getIdentifier(self):
        return self.number

class Show(object):
    title = ''
    description = ''
    poster_image = ''
    fanart_image = ''
    runtime = ''
    classification = ''
    id = ''
    synonyms = ''
    _orderBy = 'title'

    def getName(self):
        return self.title

    def getIdentifier(self):
        return self.getField('id')

    def getTemplate(self):
        fp = os.path.join(location, "show.ji2")
        with open (fp, "r") as template:
            return template.read()

    def getSearchTemplate(self):
        fp = os.path.join(location, "show_search.ji2")
        with open (fp, "r") as template:
            return template.read()

class Anime(MediaTypeManager):
    version = "0.4"
    single = True
    _config = {'enabled': True}

    config_meta = {'plugin_desc': 'Anime support'}
    order = (Show, Episode)
    download = Episode
    identifier = 'de.uranime.anime'
    addConfig = {}
    addConfig[Downloader] = [{'type':'category', 'default': None, 'prefix': 'Category for', 'sufix': 'Anime'}]
    addConfig[Indexer] = [{'type':'category', 'default': None, 'prefix': 'Category for', 'sufix': 'Anime'}]
    addConfig[PostProcessor] = [{'type':'path', 'default': None, 'prefix': 'Final path for', 'sufix': 'Anime'}]

    def makeReal(self, show, status):
        show.parent = self.root
        log("{}{}{}".format(show, status, common.getStatusByID(self.c.default_new_status_select)))
        show.status = common.getStatusByID(self.c.default_new_status_select)
        show.save()
        common.Q.put(('image.download', {'id': show.id}))
        for episode in list(show.children):
            episode.save()
            common.Q.put(('image.download', {'id': episode.id}))
        updateElement(show)
        return True


    def headInject(self):
        return self._defaultHeadInject()
