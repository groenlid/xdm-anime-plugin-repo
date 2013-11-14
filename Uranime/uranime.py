from xdm.plugins import *
import datetime
from lib import dateutil

class Uranime(Provider){
    version = "0.1"
    identifier = "de.lad1337.urani.me"
    _tag = 'uranime'
    _additional_tags = ['anime']
    single = True
    types = ['de.lad1337.anime']
    _config = {'api_key': ''}
    config_meta = {'plugin_desc': 'Anime info from http://urani.me.'}

    
}
