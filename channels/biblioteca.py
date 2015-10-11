# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Ricerca "Biblioteca"
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import base64
import json
import re
import datetime
import urllib

from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "biblioteca"
__category__ = "F"
__type__ = "generic"
__title__ = "biblioteca"
__language__ = "IT"

host = "http://www.ibs.it"

DEBUG = config.get_setting("debug")

tmdb_key = base64.urlsafe_b64decode('NTc5ODNlMzFmYjQzNWRmNGRmNzdhZmI4NTQ3NDBlYTk=')
dttime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
systime = dttime.strftime('%Y%m%d%H%M%S%f')
today_date = dttime.strftime('%Y-%m-%d')
month_date = (dttime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
month2_date = (dttime - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
year_date = (dttime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
tmdb_image = 'http://image.tmdb.org/t/p/original'
tmdb_poster = 'http://image.tmdb.org/t/p/w500'


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.biblioteca mainlist")
    itemlist = [  # Item(channel=__channel__,
                  # title="[COLOR azure]Indice Registi [A-Z][/COLOR]",
                  # action="cat_lettera_registi",
                  # url="http://www.ibs.it/dvd/lista+registi.html",
                  # thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"),
                  # Item(channel=__channel__,
                  # title="[COLOR azure]Indice Attori/Attrici [A-Z][/COLOR]",
                  # action="cat_lettera_attori",
                  # url="http://www.ibs.it/dvd-film/lista-attori.html",
                  # thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"),
                  # Item(channel="buscador",
                  # title="[COLOR yellow]Cerca per canale...[/COLOR]",
                  # action="mainlist",
                  # thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                  Item(channel="buscador",
                       title="[COLOR yellow]Cerca nei Canali...[/COLOR]",
                       action="mainlist",
                       thumbnail="http://i.imgur.com/pE5WSZp.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Cerca Film TMDB...[/COLOR]",
                       action="search",
                       extra="tmdb_mov",
                       thumbnail="http://i.imgur.com/B1H1G8U.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Cerca Attori/Registi TMDB...[/COLOR]",
                       action="search",
                       extra="tmdb_att_reg",
                       thumbnail="http://i.imgur.com/efuEeNu.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Cerca Film simili TMDB...[/COLOR]",
                       action="search",
                       extra="tmdb_film_sim",
                       thumbnail="http://i.imgur.com/JmcvZDL.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Cerca Serie TV TMDB...[/COLOR]",
                       action="search",
                       extra="tmdb_tv",
                       thumbnail="https://i.imgur.com/2ZWjLn5.jpg?1"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Al Cinema[/COLOR]",
                       action="tmdb_list",
                       url='http://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=it&page=1' % tmdb_key,
                       thumbnail="http://i.imgur.com/B16HnVh.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Più richiesti[/COLOR]",
                       action="tmdb_list",
                       url='http://api.themoviedb.org/3/movie/popular?api_key=%s&language=it&page=1' % tmdb_key,
                       thumbnail="http://i.imgur.com/8IBjyzw.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Più visti[/COLOR]",
                       action="tmdb_list",
                       url='http://api.themoviedb.org/3/movie/top_rated?api_key=%s&language=it&page=1' % tmdb_key,
                       thumbnail="http://www.clipartbest.com/cliparts/RiG/6qn/RiG6qn79T.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Più votati[/COLOR]",
                       action="tmdb_list",
                       url='http://api.themoviedb.org/3/discover/movie?api_key=%s&certification_country=US&language=it&page=1&sort_by=vote_count.desc' % tmdb_key,
                       thumbnail="http://i.imgur.com/5ShnO8w.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Ultimi 2 mesi[/COLOR]",
                       action="tmdb_list",
                       url='http://api.themoviedb.org/3/discover/movie?api_key=%s&primary_release_date.gte=%s&primary_release_date.lte=%s&language=it&page=1' % (
                           tmdb_key, year_date, month2_date),
                       thumbnail="http://i.imgur.com/CsizqUI.png"),
                  Item(channel=__channel__,
                       title="[COLOR yellow]Genere[/COLOR]",
                       action="tmdb_genre_list",
                       url='http://api.themoviedb.org/3/genre/movie/list?api_key=%s&language=it' % tmdb_key,
                       thumbnail="http://i.imgur.com/uotyBbU.png")
                  ]

    return itemlist


def search(item, texto):
    logger.info("[biblioteca.py] " + item.url + " search " + texto)

    try:
        if item.extra == "reg":
            item.url = "http://www.ibs.it/dvd/ser/serpge.asp?A=&I6.x=83&I6.y=18&P=" + texto + "&SEQ=Q&SL=&T=&dep=0&dh=25&ls=&shop=&ty=kw"
            return cat_filmografia(item)
        if item.extra == "att":
            item.url = "http://www.ibs.it/dvd/ser/serpge.asp?A=" + texto + "&I6.x=0&I6.y=0&P=&SEQ=Q&SL=&T=&dep=0&dh=25&ls=&shop=&ty=kw"
            return cat_filmografia(item)
        if item.extra == "mov":
            item.url = "http://www.ibs.it/dvd/ser/serpge.asp?A=&I6.x=72&I6.y=13&P=&SEQ=Q&SL=&T=" + texto + "&dep=0&dh=25&ls=&shop=&ty=kw"
            return cat_filmografia(item)
        if item.extra == "tmdb_mov":
            item.url = 'http://api.themoviedb.org/3/search/movie?api_key=%s&query=%s&language=it&page=1' % (
            tmdb_key, texto)
            return tmdb_list(item)
        if item.extra == "tmdb_tv":
            item.url = 'http://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&language=it&page=1' % (
            tmdb_key, texto)
            return tmdb_serie_list(item)
        if item.extra == "tmdb_film_sim":
            item.url = 'http://api.themoviedb.org/3/search/movie?api_key=%s&query=%s&append_to_response=similar_movies,alternative_title&language=it&page=1' % (
            tmdb_key, texto)
            return tmdb_list(item)
        if item.extra == "tmdb_att_reg":
            item.url = 'http://api.themoviedb.org/3/search/person?api_key=%s&query=%s&include_adult=false&language=it&page=1' % (
                tmdb_key, texto)
            return tmdb_person_list(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def cat_lettera_registi(item):
    logger.info("streamondemand.biblioteca cat_registi")
    itemlist = []

    matches = [("A", "/dvd/ser/serreg.asp?q=A"),
               ('B', '/dvd/ser/serreg.asp?q=B'),
               ('C', '/dvd/ser/serreg.asp?q=C'),
               ('D', '/dvd/ser/serreg.asp?q=D'),
               ('E', '/dvd/ser/serreg.asp?q=E'),
               ('F', '/dvd/ser/serreg.asp?q=F'),
               ('G', '/dvd/ser/serreg.asp?q=G'),
               ('H', '/dvd/ser/serreg.asp?q=H'),
               ('I', '/dvd/ser/serreg.asp?q=I'),
               ('J', '/dvd/ser/serreg.asp?q=J'),
               ('K', '/dvd/ser/serreg.asp?q=K'),
               ('L', '/dvd/ser/serreg.asp?q=L'),
               ('M', '/dvd/ser/serreg.asp?q=M'),
               ('N', '/dvd/ser/serreg.asp?q=N'),
               ('O', '/dvd/ser/serreg.asp?q=O'),
               ('P', '/dvd/ser/serreg.asp?q=P'),
               ('Q', '/dvd/ser/serreg.asp?q=Q'),
               ('R', '/dvd/ser/serreg.asp?q=R'),
               ('S', '/dvd/ser/serreg.asp?q=S'),
               ('T', '/dvd/ser/serreg.asp?q=T'),
               ('U', '/dvd/ser/serreg.asp?q=U'),
               ('V', '/dvd/ser/serreg.asp?q=V'),
               ('W', '/dvd/ser/serreg.asp?q=W'),
               ('X', '/dvd/ser/serreg.asp?q=X'),
               ('Y', '/dvd/ser/serreg.asp?q=Y'),
               ('Z', '/dvd/ser/serreg.asp?q=Z')]

    for scrapedtitle, scrapedurl in matches:
        url = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="cat_ruolo",
                 title="[COLOR azure]%s[/COLOR]" % scrapedtitle,
                 url=url,
                 folder=True))

    return itemlist


def cat_lettera_attori(item):
    logger.info("streamondemand.biblioteca cat_attori")
    itemlist = []

    matches = [('A', '/dvd/ser/seratt.asp?q=A'),
               ('B', '/dvd/ser/seratt.asp?q=B'),
               ('C', '/dvd/ser/seratt.asp?q=C'),
               ('D', '/dvd/ser/seratt.asp?q=D'),
               ('E', '/dvd/ser/seratt.asp?q=E'),
               ('F', '/dvd/ser/seratt.asp?q=F'),
               ('G', '/dvd/ser/seratt.asp?q=G'),
               ('H', '/dvd/ser/seratt.asp?q=H'),
               ('I', '/dvd/ser/seratt.asp?q=I'),
               ('J', '/dvd/ser/seratt.asp?q=J'),
               ('K', '/dvd/ser/seratt.asp?q=K'),
               ('L', '/dvd/ser/seratt.asp?q=L'),
               ('M', '/dvd/ser/seratt.asp?q=M'),
               ('N', '/dvd/ser/seratt.asp?q=N'),
               ('O', '/dvd/ser/seratt.asp?q=O'),
               ('P', '/dvd/ser/seratt.asp?q=P'),
               ('Q', '/dvd/ser/seratt.asp?q=Q'),
               ('R', '/dvd/ser/seratt.asp?q=R'),
               ('S', '/dvd/ser/seratt.asp?q=S'),
               ('T', '/dvd/ser/seratt.asp?q=T'),
               ('U', '/dvd/ser/seratt.asp?q=U'),
               ('V', '/dvd/ser/seratt.asp?q=V'),
               ('W', '/dvd/ser/seratt.asp?q=W'),
               ('X', '/dvd/ser/seratt.asp?q=X'),
               ('Y', '/dvd/ser/seratt.asp?q=Y'),
               ('Z', '/dvd/ser/seratt.asp?q=Z')]

    for scrapedtitle, scrapedurl in matches:
        url = host + scrapedurl
        itemlist.append(
            Item(channel=__channel__,
                 action="cat_ruolo",
                 title="[COLOR azure]%s[/COLOR]" % scrapedtitle,
                 url=url,
                 folder=True))

    return itemlist


def cat_ruolo(item):
    logger.info("streamondemand.biblioteca cat_registi")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    patron = r'<td bgColor=#ffffff width="33%"><table width="100%"><tr><td bgcolor="eeeee4">(.*?)</font></td></tr></table></td>'
    bloques = re.compile(patron, re.DOTALL).findall(data)

    patron = r'<a\s*(?:rel="nofollow")?\s*href="([^"]+)">([^<]+)</a>'
    for bloque in bloques:
        # Extrae las entradas (carpetas)
        matches = re.compile(patron, re.DOTALL).findall(bloque)

        for scrapedurl, scrapedtitle in matches:
            scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
            url = host + scrapedurl
            itemlist.append(
                Item(channel=__channel__,
                     action="cat_filmografia",
                     title="[COLOR azure]%s[/COLOR]" % scrapedtitle,
                     url=url,
                     folder=True))

    return itemlist


def cat_filmografia(item):
    logger.info("streamondemand.biblioteca cat_registi")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patron = r'<td width="90" valign="middle" height="120"><a href="[^"]+"><img alt="([^"]+)" border="0" src="([^"]+)"></a></td>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        titolo = urllib.quote_plus(scrapedtitle)
        itemlist.append(
            Item(channel=__channel__,
                 action="do_search",
                 extra=titolo,
                 title="[COLOR azure]%s[/COLOR]" % scrapedtitle,
                 fulltitle=scrapedtitle,
                 thumbnail=scrapedthumbnail,
                 folder=True))

    return itemlist


def tmdb_list(item):
    try:
        result = scrapertools.cache_page(item.url)
        result = json.loads(result)
        items = result['results']
    except:
        return

    try:
        next = str(result['page'])
        total = str(result['total_pages'])
        if next == total: raise Exception()
        if 'page=' not in item.url: raise Exception()
        next = '%s&page=%s' % (item.url.split('&page=', 1)[0], str(int(next) + 1))
        next = next.encode('utf-8')
    except:
        next = ''

    itemlist = []
    for item in items:
        try:
            title = item['title']
            title = scrapertools.decodeHtmlentities(title)
            title = title.encode('utf-8')

            poster = item['poster_path']
            if poster == '' or poster == None:
                raise Exception()
            else:
                poster = '%s%s' % (tmdb_poster, poster)
            poster = poster.encode('utf-8')

            fanart = item['backdrop_path']
            if fanart == '' or fanart is None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (tmdb_image, fanart)
            fanart = fanart.encode('utf-8')

            plot = item['overview']
            if plot == '' or plot is None: plot = '0'
            plot = scrapertools.decodeHtmlentities(plot)
            plot = plot.encode('utf-8')

            itemlist.append(
                Item(channel=__channel__,
                     action="do_search",
                     extra=urllib.quote_plus(title),
                     title="[COLOR azure]%s[/COLOR]" % title,
                     fulltitle=title,
                     plot=plot,
                     thumbnail=poster,
                     fanart=fanart,
                     folder=True))
        except:
            pass

    if next != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="tmdb_list",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def tmdb_serie_list(item):
    try:
        result = scrapertools.cache_page(item.url)
        result = json.loads(result)
        try:
            items = result['results']
        except:
            items = result['tv_credits']['cast']
    except:
        return

    try:
        next = str(result['page'])
        total = str(result['total_pages'])
        if next == total: raise Exception()
        if 'page=' not in item.url: raise Exception()
        next = '%s&page=%s' % (item.url.split('&page=', 1)[0], str(int(next) + 1))
        next = next.encode('utf-8')
    except:
        next = ''

    itemlist = []
    for item in items:
        try:
            title = item['name']
            title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
            title = scrapertools.decodeHtmlentities(title)
            title = title.encode('utf-8')

            poster = item['poster_path']
            if poster == '' or poster == None:
                raise Exception()
            else:
                poster = '%s%s' % (tmdb_poster, poster)
            poster = poster.encode('utf-8')

            try:
                fanart = item['backdrop_path']
            except:
                fanart = '0'
            if fanart == '' or fanart is None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (tmdb_image, fanart)
            fanart = fanart.encode('utf-8')

            try:
                plot = item['overview']
            except:
                plot = '0'
            if plot == '' or plot == None: plot = '0'
            plot = scrapertools.decodeHtmlentities(plot)
            plot = plot.encode('utf-8')

            itemlist.append(
                Item(channel=__channel__,
                     action="do_search",
                     extra=urllib.quote_plus(title),
                     title="[COLOR azure]%s[/COLOR]" % title,
                     fulltitle=title,
                     plot=plot,
                     thumbnail=poster,
                     fanart=fanart,
                     folder=True))
        except:
            pass

    if next != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="tmdb_serie_list",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def tmdb_person_list(item):
    try:
        result = scrapertools.cache_page(item.url)
        result = json.loads(result)
        items = result['results']
    except:
        return

    try:
        next = str(result['page'])
        total = str(result['total_pages'])
        if next == total: raise Exception()
        if 'page=' not in item.url: raise Exception()
        next = '%s&page=%s' % (item.url.split('&page=', 1)[0], str(int(next) + 1))
        next = next.encode('utf-8')
    except:
        next = ''

    itemlist = []
    for item in items:
        try:
            name = item['name']
            name = name.encode('utf-8')

            url = 'http://api.themoviedb.org/3/discover/movie?api_key=%s&with_people=%s&primary_release_date.lte=%s&sort_by=primary_release_date.desc&language=it&page=1' % (
                tmdb_key, item['id'], today_date)
            url = url.encode('utf-8')

            image = '%s%s' % (tmdb_image, item['profile_path'])
            image = image.encode('utf-8')

            itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR azure]%s[/COLOR]" % name,
                     action="tmdb_list",
                     url=url,
                     thumbnail=image,
                     folder=True))
        except:
            pass

    if next != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="tmdb_person_list",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def tmdb_genre_list(item):
    try:
        result = scrapertools.cache_page(item.url)
        result = json.loads(result)
        items = result['genres']
    except:
        return

    itemlist = []
    for item in items:
        try:
            name = item['name']
            name = name.encode('utf-8')

            url = 'http://api.themoviedb.org/3/discover/movie?api_key=%s&with_genres=%s&primary_release_date.gte=%s&primary_release_date.lte=%s&language=it&page=1' % (
                tmdb_key, item['id'], year_date, today_date)
            url = url.encode('utf-8')

            itemlist.append(
                Item(channel=__channel__,
                     title="[COLOR azure]%s[/COLOR]" % name,
                     action="tmdb_list",
                     url=url,
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search",
                     folder=True))
        except:
            pass

    return itemlist


def do_search(item):
    logger.info("streamondemand.channels.biblioteca do_search")

    tecleado = item.extra
    mostra = item.fulltitle

    itemlist = []

    import os
    import glob
    import imp
    from lib.fuzzywuzzy import fuzz
    import threading
    import Queue

    master_exclude_data_file = os.path.join(config.get_runtime_path(), "resources", "biblioteca.txt")
    logger.info("streamondemand.channels.buscador master_exclude_data_file=" + master_exclude_data_file)

    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.py')
    logger.info("streamondemand.channels.buscador channels_path=" + channels_path)

    excluir = ""

    if os.path.exists(master_exclude_data_file):
        logger.info("streamondemand.channels.buscador Encontrado fichero exclusiones")

        fileexclude = open(master_exclude_data_file, "r")
        excluir = fileexclude.read()
        fileexclude.close()
    else:
        logger.info("streamondemand.channels.buscador No encontrado fichero exclusiones")
        excluir = "seriesly\nbuscador\ntengourl\n__init__"

    if config.is_xbmc():
        show_dialog = True

    try:
        import xbmcgui
        progreso = xbmcgui.DialogProgressBG()
        progreso.create("Ricerca di " + mostra)
    except:
        show_dialog = False

    def worker(infile, queue):
        channel_result_itemlist = []
        try:
            basename_without_extension = os.path.basename(infile)[:-3]
            # http://docs.python.org/library/imp.html?highlight=imp#module-imp
            obj = imp.load_source(basename_without_extension, infile)
            logger.info("streamondemand.channels.buscador cargado " + basename_without_extension + " de " + infile)
            channel_result_itemlist.extend(obj.search(Item(), tecleado))
            for item in channel_result_itemlist:
                item.title = item.title + " [COLOR orange]su[/COLOR] [COLOR green]" + basename_without_extension + "[/COLOR]"
                item.viewmode = "list"
        except:
            import traceback
            logger.error(traceback.format_exc())
        queue.put(channel_result_itemlist)

    channel_files = [infile for infile in glob.glob(channels_path) if os.path.basename(infile)[:-3] not in excluir]

    result = Queue.Queue()
    threads = [threading.Thread(target=worker, args=(infile, result)) for infile in channel_files]

    for t in threads:
        t.start()

    number_of_channels = len(channel_files)

    for index, t in enumerate(threads):
        percentage = index * 100 / number_of_channels
        if show_dialog:
            progreso.update(percentage, ' Sto cercando "' + mostra + '"')
        t.join()
        itemlist.extend(result.get())

    itemlist = sorted([item for item in itemlist if fuzz.WRatio(mostra, item.fulltitle) > 85],
                      key=lambda Item: Item.title)

    if show_dialog:
        progreso.close()

    return itemlist
