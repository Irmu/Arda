# -*- coding: utf-8 -*-

from libs.tools import *
import requests

HOST = get_setting('sport_url')


def mainmenu(item):
    itemlist = list()

    itemlist.append(item.clone(
        label='Agenda S365',
        channel='s365',
        action='get_agenda',
        icon=os.path.join(image_path, 'sport365_logo.png'),
        url=HOST + '/es/events/-/1/-/-/120',
        plot='Basada en la web %s' % HOST
    ))

    itemlist.append(item.clone(
        label='En Emisión',
        channel='s365',
        action='get_agenda',
        direct=True,
        icon=os.path.join(image_path, 'live.gif'),
        url=HOST + '/es/events/1/-/-/-/120',
        plot='Basada en la web %s' % HOST
    ))

    return itemlist


def read_guide(item):
    guide = []
    guide_agrupada = dict()

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;", "", data)

    fechas = re.findall('<td colspan=9[^>]+>(\d+\.\d+\.\d+)<', data)

    for fecha in fechas:
        if fecha == fechas[-1]:
            bloque = re.findall('%s<(.*?)</table></div>' % fecha, data)[0]
        else:
            bloque = re.findall('%s<(.*?)%s' % (fecha, fechas[fechas.index(fecha) + 1]), data)[0]

        patron = 'onClick=.*?"event_([^"]+)".*?<td rowspan=2.*?src="([^"]+)".*?<td rowspan=2.*?>(\d+:\d+)<.*?<td.*?>' \
                 '([^<]+)<.*?<td.*?>(.*?)/td>.*?<tr.*?<td colspan=2.*?>([^<]+)</td><[^>]+>([^<]*)<'


        for code, thumb, hora, titulo, calidad, deporte_competicion, idioma in re.findall(patron, bloque):
            calidad = re.findall('>([\w\s?]+).*?</span>', calidad)
            if calidad:
                canales = [{'calidad': calidad[0].replace("HQ", "HD"),
                            'url': HOST + '/es/links/%s/1' % code,
                            'idioma': idioma}]
            else:
                canales = [{'calidad': 'N/A',
                            'idioma': idioma,
                            'url': HOST + '/es/links/%s/1' % code}]

            if ' / ' in deporte_competicion:
                deporte = deporte_competicion.split(' / ', 1)[0].strip()
                competicion = deporte_competicion.split(' / ', 1)[1].strip()
            else:
                deporte = deporte_competicion.strip()
                competicion = ''

            competicion = re.sub(r"World - ", "", competicion)
            if competicion.lower() in ['formula 1', 'moto gp']:
                deporte = competicion
                competicion = ''

            guide.append(Evento(fecha=fecha, hora=hora, formatTime='CEST', sport=deporte,
                                competition=competicion, title=titulo, channels=canales,
                                direct=True if "green-big.png" in thumb else False))

    for e in guide:
        key = "%s|%s" % (e.datetime, e.title)
        if key not in guide_agrupada:
            guide_agrupada[key] = e
        else:
            ev = guide_agrupada[key]
            ev.channels.extend(e.channels)

    return sorted(guide_agrupada.values(), key=lambda e: e.datetime)


def get_agenda(item, guide=None):
    itemlist = []

    if not guide:
        guide = read_guide(item)

    fechas = []
    for evento in guide:
        if item.direct and not evento.direct:
            continue

        if not item.direct and evento.fecha not in fechas:
            fechas.append(evento.fecha)
            label = '%s' % evento.fecha
            icon = os.path.join(image_path, 'logo.gif')

            itemlist.append(item.clone(
                label='[B][COLOR gold]%s[/COLOR][/B]' % label,
                icon=icon,
                action=None
            ))

        label = "[COLOR lime]" if evento.direct else "[COLOR red]"
        if evento.competition.label:
            label += "%s[/COLOR] (%s - %s)" % (evento.hora, evento.sport.label, evento.competition.label)
        else:
            label += "%s[/COLOR] (%s)" % (evento.hora, evento.sport.label)
        label = '%s %s' % (label, evento.title)

        new_item = item.clone(
            label=label,
            title=evento.title,
            icon=evento.get_icon())

        if not evento.direct:
            new_item.action = ""
        elif len(evento.channels) > 1:
            new_item.action = "ver_idiomas"
            new_item.channels = evento.channels
            new_item.label += ' [%s]' % evento.idiomas
        else:
            new_item.action = "get_enlaces"
            new_item.url = evento.channels[0]['url']
            new_item.label += ' [%s]' % evento.channels[0]['idioma']
            new_item.idioma = evento.channels[0]['idioma']
            new_item.calidad = evento.channels[0]['calidad']

        itemlist.append(new_item)

    if not itemlist:
        xbmcgui.Dialog().ok('1x2',
                            'Ups!  Parece que en estos momentos no hay eventos programados.',
                            'Intentelo mas tarde, por favor.')

    return itemlist


def ver_idiomas(item):
    itemlist = list()

    for i in item.channels:
        label = "   - %s" % i['idioma']
        if i['calidad'] != 'N/A':
            label += " (%s)" % i['calidad']

        itemlist.append(item.clone(
            label=label,
            action="get_enlaces",
            url=i['url'],
            idioma=i['idioma'],
            calidad=i['calidad']
        ))

    if itemlist:
        itemlist.insert(0, item.clone(action='', label='[B][COLOR gold]%s[/COLOR][/B]' % item.title))

    return itemlist


def get_enlaces(item):
    itemlist = list()

    data = httptools.downloadpage(item.url).data
    patron = "><span id='span_link_links.*?\('([^']+)"

    for n, data in enumerate(set(re.findall(patron, data))):
        url = decrypt(data)
        if url:
            itemlist.append(item.clone(
                label='    - Enlace %s' % (n + 1),
                action='play',
                url=url
            ))

    if itemlist:
        itemlist.insert(0, item.clone(
            action='',
            label='[B][COLOR gold]%s[/COLOR] [COLOR orange]%s (%s)[/COLOR][/B]' % (
                item.title, item.idioma, item.calidad)))

    return itemlist


def get_urlplay(url):
    try:
        s = requests.Session()
        header = {'User-Agent': httptools.default_headers["User-Agent"],
                  'Referer': url}

        content = s.get(url, headers=header).content
        url = re.findall('<iframe.*?src="([^"]+)', content)

        if url and not '/images/matras.jpg' in url[0]:
            link = re.sub(r'&#(\d+);', lambda x: chr(int(x.group(1))), url[0])
            data = s.get(link, headers=header).content

            post = {k: v for k, v in re.findall('<input type="hidden" name="([^"]+)" value="([^"]+)">', data)}
            action = re.findall("action', '([^']+)", data)
            data2 = httptools.downloadpage(action[0], post=post, headers=header).data
            data = re.findall("function\(\)\s*{\s*[a-z0-9]{43}\(.*?,.*?,\s*'([^']+)'", data2)[0]

            url = decrypt(data)
            if not url: raise ()

            url_head = 'User-Agent=%s&Referer=%s' % (
                urllib.quote(httptools.default_headers["User-Agent"]), urllib.quote('http://h5.adshell.net/peer5'))

            return (url, url_head)
    except:
        logger("Error in get_url", 'error')
        return (None, None)


def decrypt(text):
    plaintext = ''
    exec("import base64\nfrom libs.tools import *\nif py_version.startswith('2.6'):\n\texec(base64.b64decode('aW1wb3J0I"
         "G1hcnNoYWwKZXhlYyhtYXJzaGFsLmxvYWRzKGJhc2U2NC5iNjRkZWNvZGUoIll3QUFBQUFBQUFBQUpRQUFBRUFBQUFCelBRSUFBR1FBQUdRQk"
         "FHc0FBRm9BQUdRQUFHUUJBR3NCQUZvQkFHUUFBR1FCQUdzQ0FGb0NBR1FBQUdRQkFHc0RBRm9EQUdRQUFHUUNBR3NFQUd3RkFGb0ZBQUZrQXd"
         "DRUFBQmFCZ0JrQkFDRUFBQmFCd0I1ZmdCbEFnQnBDQUJrQlFCa0JnQnBDUUJrQndDRUFBQmtDQUJrQ1FCa0NnQmtDd0JrREFCa0RRQmtEZ0Jr"
         "RHdCa0RBQmtFQUJrRVFCa0VnQmtEZ0JrQ1FCa0RBQmtEd0JrRVFCa0V3QmtEd0JrRkFCa0VRQmtGUUJrRmdCa0RBQmtGd0JuR1FCRWd3RUFnd"
         "0VBRm9NQkFHa0tBR1FZQUlNQkFGb0xBRmR1WmdFQkFRRmxBZ0JwQ0FDREFBQnBDZ0JrR1FDREFRQmtCUUJrQmdCcENRQmtHZ0NFQUFCa0NBQm"
         "tDUUJrQ2dCa0N3QmtEQUJrRFFCa0RnQmtEd0JrREFCa0VBQmtFUUJrRWdCa0RnQmtHd0JrSEFCa0hRQm5FQUJFZ3dFQWd3RUFGbW9DQUcvOEF"
         "BRjVrUUJsQndCbERBQmtCUUJrQmdCcENRQmtIZ0NFQUFCa0h3QmtDQUJrRWdCa0ZRQmtFd0JrSUFCa0lRQmtFUUJrSWdCbkNRQkVnd0VBZ3dF"
         "QUZvTUJBSU1CQUZ3Q0FGb05BRm9PQUdVRkFHa1BBR1VPQUdVTkFJTUNBR2tRQUdVUkFHa0hBR1FqQUlNQkFJTUJBRm9TQUdVVEFHa1VBR1FrQ"
         "UdVU0FJTUNBR1FsQUJscEJ3QmtJd0NEQVFCYUVnQlhjVFVDQVFFQmVVMEFaUVlBZ3dBQVhBSUFXZzBBV2c0QVpRVUFhUThBWlE0QVpRMEFnd0"
         "lBYVJBQVpSRUFhUWNBWkNNQWd3RUFnd0VBV2hJQVpSTUFhUlFBWkNRQVpSSUFnd0lBWkNVQUdWb1NBRmR4TVFJQkFRRmtCZ0JhRWdCeE1RSll"
         "jVFVDV0hFNUFnRnVBUUJZWkFFQVV5Z21BQUFBYWYvLy8vOU9LQUVBQUFCMEF3QUFBR0ZsYzJNQUFBQUFBZ0FBQURRQUFBQkRBQUFBYzJvQkFB"
         "QmtBUUJrQWdCcEFBQmtBd0NFQUFCa0JBQmtCUUJrQlFCa0JnQmtCd0JrQ0FCa0NRQmtDUUJrQ2dCa0N3QmtEQUJrRFFCa0RnQmtEd0JrQmdCa"
         "0VBQmtCd0JrQlFCa0RRQmtFUUJrRWdCa0V3QmtGQUJrQ1FCa0JBQmtEUUJrRlFCa0ZnQmtGd0JrR0FCa0dRQmtHZ0JrR3dCa0hBQmtIUUJrSG"
         "dCa0d3QmtId0JrSUFCa0VnQmtHUUJrSVFCa0lnQmtJd0JrQ3dCa0NRQmtDd0JrRUFCa0dRQm5NUUJFZ3dFQWd3RUFGbjBBQUhRQkFHa0NBSFF"
         "CQUdrREFId0FBSU1CQUlNQkFHa0VBSU1BQUgwQkFIUUZBR2tHQUdRQkFHUUNBR2tBQUdRa0FJUUFBR1FHQUdRbEFHUWJBR1FtQUdRTUFHUU9B"
         "R1FSQUdRYUFHUU1BR1FQQUdRTkFHUVRBR1FSQUdRbkFHUWlBR1FvQUdjUUFFU0RBUUNEQVFBV2d3RUFhUWNBWkFFQVpBSUFhUUFBWkNRQWhBQ"
         "UFaQWNBWkFZQVpCTUFaQXNBWkFVQVpDa0FaQllBWkEwQVpDb0Fad2tBUklNQkFJTUJBQlo4QVFDREFnQUJkQWdBZkFFQWd3RUFVeWdyQUFBQV"
         "RuTUNBQUFBSlhOMEFBQUFBR01CQUFBQUFnQUFBQU1BQUFCekFBQUFjeDhBQUFCNEdBQjhBQUJkRVFCOUFRQjBBQUI4QVFDREFRQldBWEVHQUZ"
         "ka0FBQlRLQUVBQUFCT0tBRUFBQUIwQXdBQUFHTm9jaWdDQUFBQWRBSUFBQUF1TUhRQkFBQUFlU2dBQUFBQUtBQUFBQUJ6Q0FBQUFEeHpkSEpw"
         "Ym1jK2N3a0FBQUE4WjJWdVpYaHdjajRHQUFBQWN3SUFBQUFKQUdsb0FBQUFhWFFBQUFCcGNBQUFBR2x6QUFBQWFUb0FBQUJwTHdBQUFHbG1BQ"
         "UFBYVhJQUFBQnBhUUFBQUdsbEFBQUFhVzRBQUFCcFpBQUFBR2xoQUFBQWFTNEFBQUJwWXdBQUFHbHZBQUFBYVcwQUFBQnBXQUFBQUdsckFBQU"
         "FhVWdBQUFCcFVnQUFBR2wzQUFBQWFYWUFBQUJwZFFBQUFHbE9BQUFBYVVVQUFBQnBVQUFBQUdsVkFBQUFhVFFBQUFCcE13QUFBR2w0QUFBQWF"
         "Ua0FBQUJqQVFBQUFBSUFBQUFEQUFBQWN3QUFBSE1mQUFBQWVCZ0FmQUFBWFJFQWZRRUFkQUFBZkFFQWd3RUFWZ0Z4QmdCWFpBQUFVeWdCQUFB"
         "QVRpZ0JBQUFBVWdJQUFBQW9BZ0FBQUZJREFBQUFVZ1FBQUFBb0FBQUFBQ2dBQUFBQWN3Z0FBQUE4YzNSeWFXNW5Qbk1KQUFBQVBHZGxibVY0Y"
         "0hJK0NBQUFBSE1DQUFBQUNRQnBiQUFBQUdsbkFBQUFhVEVBQUFCcE1nQUFBR2xmQUFBQWFYa0FBQUFvQ1FBQUFIUUVBQUFBYW05cGJuUUhBQU"
         "FBZFhKc2JHbGlNblFIQUFBQWRYSnNiM0JsYm5RSEFBQUFVbVZ4ZFdWemRIUUVBQUFBY21WaFpIUUpBQUFBZUdKdFkyRmtaRzl1ZEFVQUFBQkJ"
         "aR1J2Ym5RS0FBQUFjMlYwVTJWMGRHbHVaM1FHQUFBQVpHVmpiMlJsS0FJQUFBQjBBd0FBQUhWeWJIUUdBQUFBYVhaZmEyVjVLQUFBQUFBb0FB"
         "QUFBSE1JQUFBQVBITjBjbWx1Wno1MEJnQUFBR2RsZEd0bGVRVUFBQUJ6Q0FBQUFBQUJzQUVlQVpJQll3RUFBQUFDQUFBQUJ3QUFBRU1BQUFCe"
         "mJnQUFBSFFBQUh3QUFHUUJBQm1EQVFCOUFRQjhBQUJrQVFBZ2ZRQUFmQUFBWkFBQVpBQUFaQUVBaFFNQUdYMEFBSHdBQUdRQ0FDQjhBQUJrQX"
         "dBZkYzd0FBR1FDQUdRREFDRVhaQVFBZkFFQUZCZDlBQUIwQVFCcEFnQjhBQUNEQVFCOUFBQjhBQUJwQXdCa0JRQ0RBUUJUS0FZQUFBQk9hZi8"
         "vLy85cEJBQUFBR2tJQUFBQWRBRUFBQUE5ZEFFQUFBQjhLQVFBQUFCMEF3QUFBR2x1ZEhRR0FBQUFZbUZ6WlRZMGRBa0FBQUJpTmpSa1pXTnZa"
         "R1YwQlFBQUFITndiR2wwS0FJQUFBQlNEd0FBQUhRRUFBQUFjR0Z1WkNnQUFBQUFLQUFBQUFCekNBQUFBRHh6ZEhKcGJtYytVZzBBQUFBS0FBQ"
         "UFjd3dBQUFBQUFSQUJDZ0VUQVNVQkR3RnpBZ0FBQUNWelVnRUFBQUJqQVFBQUFBSUFBQUFEQUFBQVl3QUFBSE1mQUFBQWVCZ0FmQUFBWFJFQW"
         "ZRRUFkQUFBZkFFQWd3RUFWZ0Z4QmdCWFpBQUFVeWdCQUFBQVRpZ0JBQUFBVWdJQUFBQW9BZ0FBQUZJREFBQUFVZ1FBQUFBb0FBQUFBQ2dBQUF"
         "BQWN3Z0FBQUE4YzNSeWFXNW5Qbk1KQUFBQVBHZGxibVY0Y0hJK0VnQUFBSE1DQUFBQUNRQnBjQUFBQUdsc0FBQUFhWFVBQUFCcFp3QUFBR2xw"
         "QUFBQWFXNEFBQUJwTGdBQUFHbDJBQUFBYVdRQUFBQnBaUUFBQUdsdkFBQUFhWFFBQUFCcFV3QUFBR2x5QUFBQWFXSUFBQUJwWVFBQUFIUUhBQ"
         "UFBZG1WeWMybHZiblFDQUFBQWFXUmpBUUFBQUFJQUFBQURBQUFBWXdBQUFITWZBQUFBZUJnQWZBQUFYUkVBZlFFQWRBQUFmQUVBZ3dFQVZnRn"
         "hCZ0JYWkFBQVV5Z0JBQUFBVGlnQkFBQUFVZ0lBQUFBb0FnQUFBRklEQUFBQVVnUUFBQUFvQUFBQUFDZ0FBQUFBY3dnQUFBQThjM1J5YVc1blB"
         "uTUpBQUFBUEdkbGJtVjRjSEkrRkFBQUFITUNBQUFBQ1FCcE1RQUFBR2w0QUFBQWFUSUFBQUJqQVFBQUFBSUFBQUFEQUFBQVl3QUFBSE1mQUFB"
         "QWVCZ0FmQUFBWFJFQWZRRUFkQUFBZkFFQWd3RUFWZ0Z4QmdCWFpBQUFVeWdCQUFBQVRpZ0JBQUFBVWdJQUFBQW9BZ0FBQUZJREFBQUFVZ1FBQ"
         "UFBb0FBQUFBQ2dBQUFBQWN3Z0FBQUE4YzNSeWFXNW5Qbk1KQUFBQVBHZGxibVY0Y0hJK0ZnQUFBSE1DQUFBQUNRQnBjd0FBQUdsZkFBQUFhV3"
         "NBQUFCcGVRQUFBSFFEQUFBQWFHVjRjd3NBQUFBb1cyRXRaakF0T1YwcktXa0FBQUFBS0JVQUFBQlNCZ0FBQUZJVUFBQUFVZ29BQUFCMEJBQUF"
         "BSGhpYldOMEJBQUFBR3hwWW5OU0FBQUFBRklRQUFBQVVnMEFBQUJTQ3dBQUFGSUZBQUFBZEF3QUFBQm5aWFJCWkdSdmJrbHVabTkwQVFBQUFI"
         "WjBDd0FBQUdkbGRGOXpaWFIwYVc1bmRBSUFBQUJwZG5RREFBQUFhMlY1ZEJVQUFBQkJSVk5OYjJSbFQyWlBjR1Z5WVhScGIyNURRa04wQndBQ"
         "UFHUmxZM0o1Y0hSMEJBQUFBSFJsZUhSMENRQUFBSEJzWVdsdWRHVjRkSFFDQUFBQWNtVjBCd0FBQUdacGJtUmhiR3dvQUFBQUFDZ0FBQUFBS0"
         "FBQUFBQnpDQUFBQUR4emRISnBibWMrZEFnQUFBQThiVzlrZFd4bFBnRUFBQUJ6S0FBQUFBd0JEQUVZQVJBQkNRVUpCd01CZmdFREFXTUJBd0Z"
         "LQVNRQkl3RURBUU1CRHdFa0FSb0JBd0U9IikpKQ=='))\nelif py_version.startswith('2.7'):\n\texec(base64.b64decode('aW"
         "1wb3J0IG1hcnNoYWwKZXhlYyhtYXJzaGFsLmxvYWRzKGJhc2U2NC5iNjRkZWNvZGUoIll3QUFBQUFBQUFBQUhRQUFBRUFBQUFCek93SUFBR1F"
         "BQUdRQkFHd0FBRm9BQUdRQUFHUUJBR3dCQUZvQkFHUUFBR1FCQUd3Q0FGb0NBR1FBQUdRQkFHd0RBRm9EQUdRQUFHUUNBR3dFQUcwRkFGb0ZB"
         "QUZrQXdDRUFBQmFCZ0JrQkFDRUFBQmFCd0I1ZmdCbEFnQnFDQUJrQlFCa0JnQnFDUUJrQndDRUFBQmtDQUJrQ1FCa0NnQmtDd0JrREFCa0RRQ"
         "mtEZ0JrRHdCa0RBQmtFQUJrRVFCa0VnQmtEZ0JrQ1FCa0RBQmtEd0JrRVFCa0V3QmtEd0JrRkFCa0VRQmtGUUJrRmdCa0RBQmtGd0JuR1FCRW"
         "d3RUFnd0VBRm9NQkFHb0tBR1FZQUlNQkFGb0xBRmR1WkFFQkFRRmxBZ0JxQ0FDREFBQnFDZ0JrR1FDREFRQmtCUUJrQmdCcUNRQmtHZ0NFQUF"
         "Ca0NBQmtDUUJrQ2dCa0N3QmtEQUJrRFFCa0RnQmtEd0JrREFCa0VBQmtFUUJrRWdCa0RnQmtHd0JrSEFCa0hRQm5FQUJFZ3dFQWd3RUFGbXND"
         "QUhJM0FubVJBR1VIQUdVTUFHUUZBR1FHQUdvSkFHUWVBSVFBQUdRZkFHUUlBR1FTQUdRVkFHUVRBR1FnQUdRaEFHUVJBR1FpQUdjSkFFU0RBU"
         "UNEQVFBV2d3RUFnd0VBWEFJQVdnMEFXZzRBWlFVQWFnOEFaUTRBWlEwQWd3SUFhaEFBWlJFQWFnY0FaQ01BZ3dFQWd3RUFXaElBWlJNQWFoUU"
         "FaQ1FBWlJJQWd3SUFaQ1VBR1dvSEFHUWpBSU1CQUZvU0FGZHhNd0lCQVFGNVRRQmxCZ0NEQUFCY0FnQmFEUUJhRGdCbEJRQnFEd0JsRGdCbER"
         "RQ0RBZ0JxRUFCbEVRQnFCd0JrSXdDREFRQ0RBUUJhRWdCbEV3QnFGQUJrSkFCbEVnQ0RBZ0JrSlFBWldoSUFWM0V3QWdFQkFXUUdBRm9TQUhF"
         "d0FsaHhNd0pZY1RjQ2JnRUFXR1FCQUZNb0pnQUFBR24vLy8vL1RpZ0JBQUFBZEFNQUFBQmhaWE5qQUFBQUFBSUFBQUEwQUFBQVF3QUFBSE5xQ"
         "VFBQVpBRUFaQUlBYWdBQVpBTUFoQUFBWkFRQVpBVUFaQVVBWkFZQVpBY0FaQWdBWkFrQVpBa0FaQW9BWkFzQVpBd0FaQTBBWkE0QVpBOEFaQV"
         "lBWkJBQVpBY0FaQVVBWkEwQVpCRUFaQklBWkJNQVpCUUFaQWtBWkFRQVpBMEFaQlVBWkJZQVpCY0FaQmdBWkJrQVpCb0FaQnNBWkJ3QVpCMEF"
         "aQjRBWkJzQVpCOEFaQ0FBWkJJQVpCa0FaQ0VBWkNJQVpDTUFaQXNBWkFrQVpBc0FaQkFBWkJrQVp6RUFSSU1CQUlNQkFCWjlBQUIwQVFCcUFn"
         "QjBBUUJxQXdCOEFBQ0RBUUNEQVFCcUJBQ0RBQUI5QVFCMEJRQnFCZ0JrQVFCa0FnQnFBQUJrSkFDRUFBQmtCZ0JrSlFCa0d3QmtKZ0JrREFCa"
         "0RnQmtFUUJrR2dCa0RBQmtEd0JrRFFCa0V3QmtFUUJrSndCa0lnQmtLQUJuRUFCRWd3RUFnd0VBRm9NQkFHb0hBR1FCQUdRQ0FHb0FBR1FrQU"
         "lRQUFHUUhBR1FHQUdRVEFHUUxBR1FGQUdRcEFHUVdBR1FOQUdRcUFHY0pBRVNEQVFDREFRQVdmQUVBZ3dJQUFYUUlBSHdCQUlNQkFGTW9Ld0F"
         "BQUU1ekFnQUFBQ1Z6ZEFBQUFBQmpBUUFBQUFJQUFBQURBQUFBY3dBQUFITWJBQUFBZkFBQVhSRUFmUUVBZEFBQWZBRUFnd0VBVmdGeEF3QmtB"
         "QUJUS0FFQUFBQk9LQUVBQUFCMEF3QUFBR05vY2lnQ0FBQUFkQUlBQUFBdU1IUUJBQUFBZVNnQUFBQUFLQUFBQUFCekNBQUFBRHh6ZEhKcGJtY"
         "ytjd2tBQUFBOFoyVnVaWGh3Y2o0R0FBQUFjd0lBQUFBR0FHbG9BQUFBYVhRQUFBQnBjQUFBQUdsekFBQUFhVG9BQUFCcEx3QUFBR2xtQUFBQW"
         "FYSUFBQUJwYVFBQUFHbGxBQUFBYVc0QUFBQnBaQUFBQUdsaEFBQUFhUzRBQUFCcFl3QUFBR2x2QUFBQWFXMEFBQUJwV0FBQUFHbHJBQUFBYVV"
         "nQUFBQnBVZ0FBQUdsM0FBQUFhWFlBQUFCcGRRQUFBR2xPQUFBQWFVVUFBQUJwVUFBQUFHbFZBQUFBYVRRQUFBQnBNd0FBQUdsNEFBQUFhVGtB"
         "QUFCakFRQUFBQUlBQUFBREFBQUFjd0FBQUhNYkFBQUFmQUFBWFJFQWZRRUFkQUFBZkFFQWd3RUFWZ0Z4QXdCa0FBQlRLQUVBQUFCT0tBRUFBQ"
         "UJTQWdBQUFDZ0NBQUFBVWdNQUFBQlNCQUFBQUNnQUFBQUFLQUFBQUFCekNBQUFBRHh6ZEhKcGJtYytjd2tBQUFBOFoyVnVaWGh3Y2o0SUFBQU"
         "Fjd0lBQUFBR0FHbHNBQUFBYVdjQUFBQnBNUUFBQUdreUFBQUFhVjhBQUFCcGVRQUFBQ2dKQUFBQWRBUUFBQUJxYjJsdWRBY0FBQUIxY214c2F"
         "XSXlkQWNBQUFCMWNteHZjR1Z1ZEFjQUFBQlNaWEYxWlhOMGRBUUFBQUJ5WldGa2RBa0FBQUI0WW0xallXUmtiMjUwQlFBQUFFRmtaRzl1ZEFv"
         "QUFBQnpaWFJUWlhSMGFXNW5kQVlBQUFCa1pXTnZaR1VvQWdBQUFIUURBQUFBZFhKc2RBWUFBQUJwZGw5clpYa29BQUFBQUNnQUFBQUFjd2dBQ"
         "UFBOGMzUnlhVzVuUG5RR0FBQUFaMlYwYTJWNUJRQUFBSE1JQUFBQUFBR3dBUjRCa2dGakFRQUFBQUlBQUFBRUFBQUFRd0FBQUhOdUFBQUFkQU"
         "FBZkFBQVpBRUFHWU1CQUgwQkFId0FBR1FCQUNCOUFBQjhBQUJrQUFCa0FBQmtBUUNGQXdBWmZRQUFmQUFBWkFJQUlId0FBR1FEQUI4WGZBQUF"
         "aQUlBWkFNQUlSZGtCQUI4QVFBVUYzMEFBSFFCQUdvQ0FId0FBSU1CQUgwQUFId0FBR29EQUdRRkFJTUJBRk1vQmdBQUFFNXAvLy8vLzJrRUFB"
         "QUFhUWdBQUFCMEFRQUFBRDEwQVFBQUFId29CQUFBQUhRREFBQUFhVzUwZEFZQUFBQmlZWE5sTmpSMENRQUFBR0kyTkdSbFkyOWtaWFFGQUFBQ"
         "WMzQnNhWFFvQWdBQUFGSVBBQUFBZEFRQUFBQndZVzVrS0FBQUFBQW9BQUFBQUhNSUFBQUFQSE4wY21sdVp6NVNEUUFBQUFvQUFBQnpEQUFBQU"
         "FBQkVBRUtBUk1CSlFFUEFYTUNBQUFBSlhOU0FRQUFBR01CQUFBQUFnQUFBQU1BQUFCakFBQUFjeHNBQUFCOEFBQmRFUUI5QVFCMEFBQjhBUUN"
         "EQVFCV0FYRURBR1FBQUZNb0FRQUFBRTRvQVFBQUFGSUNBQUFBS0FJQUFBQlNBd0FBQUZJRUFBQUFLQUFBQUFBb0FBQUFBSE1JQUFBQVBITjBj"
         "bWx1Wno1ekNRQUFBRHhuWlc1bGVIQnlQaElBQUFCekFnQUFBQVlBYVhBQUFBQnBiQUFBQUdsMUFBQUFhV2NBQUFCcGFRQUFBR2x1QUFBQWFTN"
         "EFBQUJwZGdBQUFHbGtBQUFBYVdVQUFBQnBid0FBQUdsMEFBQUFhVk1BQUFCcGNnQUFBR2xpQUFBQWFXRUFBQUIwQndBQUFIWmxjbk5wYjI1ME"
         "FnQUFBR2xrWXdFQUFBQUNBQUFBQXdBQUFHTUFBQUJ6R3dBQUFId0FBRjBSQUgwQkFIUUFBSHdCQUlNQkFGWUJjUU1BWkFBQVV5Z0JBQUFBVGl"
         "nQkFBQUFVZ0lBQUFBb0FnQUFBRklEQUFBQVVnUUFBQUFvQUFBQUFDZ0FBQUFBY3dnQUFBQThjM1J5YVc1blBuTUpBQUFBUEdkbGJtVjRjSEkr"
         "RkFBQUFITUNBQUFBQmdCcE1RQUFBR2w0QUFBQWFUSUFBQUJqQVFBQUFBSUFBQUFEQUFBQVl3QUFBSE1iQUFBQWZBQUFYUkVBZlFFQWRBQUFmQ"
         "UVBZ3dFQVZnRnhBd0JrQUFCVEtBRUFBQUJPS0FFQUFBQlNBZ0FBQUNnQ0FBQUFVZ01BQUFCU0JBQUFBQ2dBQUFBQUtBQUFBQUJ6Q0FBQUFEeH"
         "pkSEpwYm1jK2N3a0FBQUE4WjJWdVpYaHdjajRXQUFBQWN3SUFBQUFHQUdsekFBQUFhVjhBQUFCcGF3QUFBR2w1QUFBQWRBTUFBQUJvWlhoekN"
         "3QUFBQ2hiWVMxbU1DMDVYU3NwYVFBQUFBQW9GUUFBQUZJR0FBQUFVaFFBQUFCU0NnQUFBSFFFQUFBQWVHSnRZM1FFQUFBQWJHbGljMUlBQUFB"
         "QVVoQUFBQUJTRFFBQUFGSUxBQUFBVWdVQUFBQjBEQUFBQUdkbGRFRmtaRzl1U1c1bWIzUUJBQUFBZG5RTEFBQUFaMlYwWDNObGRIUnBibWQwQ"
         "WdBQUFHbDJkQU1BQUFCclpYbDBGUUFBQUVGRlUwMXZaR1ZQWms5d1pYSmhkR2x2YmtOQ1EzUUhBQUFBWkdWamNubHdkSFFFQUFBQWRHVjRkSF"
         "FKQUFBQWNHeGhhVzUwWlhoMGRBSUFBQUJ5WlhRSEFBQUFabWx1WkdGc2JDZ0FBQUFBS0FBQUFBQW9BQUFBQUhNSUFBQUFQSE4wY21sdVp6NTB"
         "DQUFBQUR4dGIyUjFiR1UrQVFBQUFITW9BQUFBREFFTUFSZ0JFQUVKQlFrSEF3RitBUU1CWWdFREFVb0JKQUVqQVFNQkF3RVBBU1FCR2dFREFR"
         "PT0iKSkp'))\nelse:\n\tlogger('Versión de python no compatible')")

    return plaintext


def play(item):
    url, header = get_urlplay(item.url)

    if url:
        url += '|' + header
        return {'action': 'play', 'VideoPlayer': 'f4mtester', 'url': url, 'titulo': item.title,
                'iconImage': item.icon, 'callbackpath': __file__, 'callbackparam': (item.url)}

    xbmcgui.Dialog().ok('1x2',
                        'Ups!  Parece que en estos momentos no hay nada que ver en este enlace.',
                        'Intentelo mas tarde o pruebe en otro enlace, por favor.')
    return None


def f4mcallback(param, tipo, error, Cookie_Jar, url, headers):
    logger("####################### f4mcallback ########################")

    param = eval(param)
    urlnew, header = get_urlplay(param[0])

    return urlnew, Cookie_Jar
