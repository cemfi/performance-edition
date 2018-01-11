import re

from lxml import etree

_XML_NS = 'http://www.w3.org/XML/1998/namespace'
_MEI_NS = 'http://www.music-encoding.org/ns/mei'


def split_ns(tag):
    m = re.search(r'({[^}]*})?(.*)', tag)
    ns = None
    if m.group(1) is not None:
        ns = m.group(1)[1:-1]
    tag = m.group(2)
    return ns, tag


def annotate_measures(mei):
    xml = etree.parse(mei)
    surfaces = xml.xpath('//*[local-name()="surface"]')
    for surface in surfaces:

        for elem in surface:
            tag = split_ns(elem.tag)[1]
            if tag == 'zone' and elem.get('type') == 'measure':

                zone_id = elem.get('{{{ns}}}id'.format(ns=_XML_NS))
                points = []
                for point in elem:
                    points.append([int(point.get('x')), int(point.get('y'))])
                print(str(points) + ',')
        print()


if __name__ == '__main__':
    annotate_measures('data/aligned.mei')
