import json
from pprint import pprint
import re

from lxml import etree

ns = {
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'mei': 'http://www.music-encoding.org/ns/mei',
}


def split_ns(tag):
    m = re.search(r'({[^}]*})?(.*)', tag)
    namespace = m.group(1)[1:-1] if m.group(1) is not None else None
    tag = m.group(2)
    return namespace, tag


def calc_image_overlays(mei):
    xml = etree.parse(mei)
    surfaces = xml.xpath('//*[local-name()="surface"]')

    overlays = []

    for i, surface in enumerate(surfaces):
        # page = int(surface.get('n'))
        page_overlays = []

        file = surface.xpath('.//*[local-name()="graphic"]')[0].get('target')

        for elem in surface:
            tag = split_ns(elem.tag)[1]
            if tag == 'zone' and elem.get('type') == 'measure':
                zone_id = elem.get('{{{ns}}}id'.format(ns=ns['xml']))
                measure = xml.xpath('//*[local-name()="measure" and @facs="#{}"]'.format(zone_id))[0]

                id = measure.get('{{{ns}}}id'.format(ns=ns['xml']))
                n = measure.get('n')
                label = measure.get('label')
                ulx = int(elem.get('ulx'))
                uly = int(elem.get('uly'))
                lrx = int(elem.get('lrx'))
                lry = int(elem.get('lry'))

                page_overlays.append({
                    'id': id,
                    'n': n,
                    'label': label,
                    'x': ulx,
                    'y': uly,
                    'width': lrx - ulx,
                    'height': lry - uly,
                })

        overlays.append({
            'file': file,
            'overlays': page_overlays
        })

    return overlays


if __name__ == '__main__':
    image_overlays = calc_image_overlays('data/combined.mei')

    data = {'images': image_overlays}
    pprint(data)

    with open('data/dataset.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
