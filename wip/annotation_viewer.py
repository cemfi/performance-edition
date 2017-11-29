import colorsys
import os
import re

from lxml import etree
from PIL import Image, ImageDraw, ImageFont

_XML_NS = 'http://www.w3.org/XML/1998/namespace'
_MEI_NS = 'http://www.music-encoding.org/ns/mei'


def split_ns(tag):
    m = re.search(r'({[^}]*})?(.*)', tag)
    namespace = m.group(1)[1:-1] if m.group(1) is not None else None
    tag = m.group(2)
    return namespace, tag


def annotate_measures(mei, oriented=False):
    xml = etree.parse(mei)
    surfaces = xml.xpath('//*[local-name()="surface"]')
    for i, surface in enumerate(surfaces):
        filename = os.path.join(os.path.dirname(mei), surface[0].get('target'))
        width = int(surface[0].get('width'))
        height = int(surface[0].get('height'))

        scale = min(width, height)
        image = Image.open(filename)
        draw = ImageDraw.Draw(image, 'RGBA')
        color = colorsys.hsv_to_rgb(0.5, 1, 0.4)
        color_outline = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255)
        color_fill = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 40)
        font = ImageFont.truetype('SourceCodePro-Bold.otf', int(scale / 40))
        line_width = int(scale / 400)

        is_annotated = False

        for elem in surface:
            tag = split_ns(elem.tag)[1]
            if tag == 'zone' and elem.get('type') == 'measure':
                is_annotated = True

                zone_id = elem.get('{{{ns}}}id'.format(ns=_XML_NS))
                n = xml.xpath('//*[local-name()="measure" and @facs="#{}"]'.format(zone_id))[0].get('n')
                ulx = int(elem.get('ulx'))
                uly = int(elem.get('uly'))
                lrx = int(elem.get('lrx'))
                lry = int(elem.get('lry'))

                if not oriented:
                    points = [(ulx, uly), (lrx, uly), (lrx, lry), (ulx, lry)]
                else:
                    points = [(int(point.get('x')), int(point.get('y'))) for point in elem]

                # Draw measure
                draw.polygon(points, fill=color_fill, outline=color_outline, width=line_width)
                # for k, _ in enumerate(points):
                #     draw.line(
                #         [points[k][0],
                #          points[k][1],
                #          points[(k + 1) % len(points)][0],
                #          points[(k + 1) % len(points)][1]],
                #         fill=color_outline, width=line_width)

                # Draw text number in center of measure
                w, h = draw.textsize(n, font=font)
                draw.rectangle(
                    [ulx + (lrx - ulx) / 2 - w / 1.2,
                     uly + (lry - uly) / 2 - h / 2,
                     ulx + (lrx - ulx) / 2 + w / 1.2,
                     uly + (lry - uly) / 2 + h / 1.2],
                    fill=color_outline)
                draw.text(
                    [ulx + (lrx - ulx) / 2 - w / 2,
                     uly + (lry - uly) / 2 - h / 2],
                    n, font=font, fill=(255, 255, 255, 255))

        if is_annotated:
            print("Schreibe Bild", i + 1, "von", len(surfaces))
            filename = os.path.join(os.path.splitext(filename)[0] + '_demad.jpg')
            image.save(filename, 'jpeg')


if __name__ == '__main__':
    annotate_measures('data/measures_mov_edit.mei', oriented=True)
