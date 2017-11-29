import sys

from lxml import etree

ns = {
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'mei': 'http://www.music-encoding.org/ns/mei',
}


def combine(mei_path, vertaktoid_path, combined_path=None):
    mei_xml = etree.parse(mei_path).getroot()
    vertaktoid_xml = etree.parse(vertaktoid_path).getroot()

    facsimile = vertaktoid_xml.xpath('//mei:mei/mei:music/mei:facsimile', namespaces=ns)[0]
    mei_music = mei_xml.xpath('//mei:mei/mei:music', namespaces=ns)[0]
    mei_music.insert(0, facsimile)

    mei_measures = mei_music.xpath('//*[local-name()="measure"]', namespaces=ns)
    vertaktoid_measures = vertaktoid_xml.xpath('//*[local-name()="measure"]', namespaces=ns)

    if len(mei_measures) == len(vertaktoid_measures):
        for i in range(len(mei_measures)):
            mei_measures[i].set('label', vertaktoid_measures[i].get('n'))
            mei_measures[i].set('facs', vertaktoid_measures[i].get('facs'))
    else:
        sys.stderr.write('Error: Numbers of measures do not match!')

    if combined_path is not None:
        etree.ElementTree(mei_xml).write(combined_path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    combine('data/source.mei', 'data/measures_final.mei', combined_path='data/combined.mei')
