from xdm.plugins import *
import os

location = os.path.abspath(os.path.dirname(__file__))


class Episode(object):
    title = ''
    airdate = 0
    number = 0
    overview = ''
    screencap_image = ''

    _orderBy = 'number'
    _orderReverse = True

    def getTemplate(self):
        fp = os.path.join(location, "episode.ji2")
        with open (fp, "r") as template:
            return template.read()

    def getSearchTerms(self):
        return ['%s s%02de%02d' % (self.parent.parent.title, self.parent.number, self.number)]

    def getName(self):
        return "%se%s %s" % (self.parent.getName(), self.number, self.title)

    def getReleaseDate(self):
        return self.airdate

    def getIdentifier(self):
        return self.number

class Show(object):
    title = ''
    id = ''
    airs = ''
    overview = ''
    year = 0
    poster_image = ''
    banner_image = ''
    fanart_image = ''
    show_status = ''
    genres = ''
    runtime = ''

    _orderBy = 'title'
    _orderReverse = True

    def getTemplate(self):
        fp = os.path.join(location, "show.ji2")
        with open (fp, "r") as template:
            return template.read()

    def getSearchTemplate(self):
        fp = os.path.join(location, "show_search.ji2")
        with open (fp, "r") as template:
            return template.read()

    def getName(self):
        return self.title

    def getIdentifier(self):
        return self.getField('id')

class Anime(MediaTypeManager):
    version = "0.1"
    single = True
    _config = {'enabled': True}
    config_meta = {'plugin_desc': 'Anime'}
    order = (Show, Episode)
    download = Episode
    identifier = 'de.lad1337.anime'
    xdm_version = (0, 5, 9)
    addConfig = {}
    addConfig[Downloader] = [{'type':'category', 'default': None, 'prefix': 'Category for', 'sufix': 'Anime'}]
    addConfig[Indexer] = [{'type':'category', 'default': None, 'prefix': 'Category for', 'sufix': 'Anime'}]
    addConfig[PostProcessor] = [{'type':'path', 'default': None, 'prefix': 'Final path for', 'sufix': 'Anime'}]

    def makeReal(self, show):
        show.parent = self.root
        show.status = common.getStatusByID(self.c.default_new_status_select)
        show.save()
        common.Q.put(('image.download', {'id': show.id}))
        for episode in list(show.children):
            episode.save()
            common.Q.put(('image.download', {'id': episode.id}))
        return True

    def headInject(self):
        return self._defaultHeadInject()

    def homeStatuses(self):
        return common.getEveryStatusBut([common.TEMP])

    def getUpdateableElements(self, asList=True):
        shows = Element.select().where(Element.type == 'Show',
                                       Element.parent == self.root)
        if asList:
            return list(shows)
        return shows

    def _episode_count(self, show, statuses=False):
        all_seasons = list(Element.select().where(Element.type == 'Season',
                                              Element.parent == show))
        seasons = [s for s in all_seasons if s.number]
        if statuses:
            return Element.select().where(Element.type == 'Episode',
                                          Element.parent << seasons,
                                          Element.status << statuses).count()
        else:
            return Element.select().where(Element.type == 'Episode',
                                          Element.parent << seasons).count()

    def _season_episode_count(self, season, statuses=False):
        if statuses:
            return Element.select().where(Element.type == 'Episode',
                                          Element.parent == season,
                                          Element.status << statuses).count()
        else:
            return Element.select().where(Element.type == 'Episode',
                                          Element.parent == season).count()
