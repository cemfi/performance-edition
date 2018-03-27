import json
import math
import os
import re
import sys

import jpype
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from lxml import etree
from scipy.spatial.distance import cdist

ns = {
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'mei': 'http://www.music-encoding.org/ns/mei',
}

a, b = np.ogrid[0:12, 0:-12:-1]
circular = a + b


def split_ns(tag):
    m = re.search(r'({[^}]*})?(.*)', tag)
    namespace = m.group(1)[1:-1] if m.group(1) is not None else None
    tag = m.group(2)
    return namespace, tag


def from_meico(xml, begin=0, end=np.inf):
    parser = etree.XMLParser(collect_ids=False)
    xml = etree.fromstring(xml, parser=parser)

    shortest_duration = np.inf
    highest_date = 0
    notes_and_rests = {}
    id_to_index = {}

    # calculate correct boundaries
    if begin != 0:
        elem = xml.xpath('//*[@xml:id=\'' + begin + '\']',
                         namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'})[0]
        begin = float(elem.get('midi.date'))
    if end != np.inf:
        elem = xml.xpath('//*[@xml:id=\'' + end + '\']',
                         namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'})[0]
        end = float(elem.get('midi.date')) + float(elem.get('midi.dur'))

    # iterate through all rests and notes
    for elem in xml.xpath('//*[local-name()="note"][@midi.dur]|//*[local-name()="rest"][@midi.dur]'):
        identifier = elem.get('{http://www.w3.org/XML/1998/namespace}id')

        pitch = (int(float(elem.get('pnum'))) if elem.tag == '{http://www.music-encoding.org/ns/mei}note' else None)
        date = float(elem.get('midi.date'))
        dur = float(elem.get('midi.dur'))

        if begin <= date <= end:
            notes_and_rests[identifier] = {}
            notes_and_rests[identifier]['pitch'] = pitch
            notes_and_rests[identifier]['date'] = date - begin
            notes_and_rests[identifier]['dur'] = dur

            shortest_duration = min(shortest_duration, dur)
            highest_date = max(highest_date, date - begin + dur)

    cqt_matrix = np.zeros((12 * 8, int(highest_date / shortest_duration)), dtype=np.float64)

    for elem in notes_and_rests:
        begin = math.floor(notes_and_rests[elem]['date'] / shortest_duration)
        id_to_index[elem] = begin
        if notes_and_rests[elem]['pitch'] is not None:
            end = math.ceil((notes_and_rests[elem]['date'] + notes_and_rests[elem]['dur']) / shortest_duration)
            for c in range(begin, end):
                try:
                    pitch = notes_and_rests[elem]['pitch']
                    cqt_matrix[pitch, c] += 1

                    # cqt_matrix[pitch, c + 1] += 0.5
                    # cqt_matrix[pitch, c + 2] += 0.3
                    # cqt_matrix[pitch, c + 3] += 0.1
                    # if pitch + 12 <= cqt_matrix.shape[0]:
                    #     cqt_matrix[pitch + 12, c] += 0.4
                    # if pitch + 19 <= cqt_matrix.shape[0]:
                    #     cqt_matrix[pitch + 19, c] += 0.2
                    # if pitch + 24 <= cqt_matrix.shape[0]:
                    #     cqt_matrix[pitch + 24, c] += 0.1
                except IndexError:
                    pass

    cqt_matrix = np.log(1 + cqt_matrix)

    return cqt_matrix, id_to_index


def calc_accu_cost(C, D, D_steps, step_sizes_sigma, weights_mul, weights_add, max_0, max_1):
    for cur_n in range(max_0, D.shape[0]):
        for cur_m in range(max_1, D.shape[1]):
            # accumulate costs
            for cur_step_idx, cur_w_add, cur_w_mul in zip(range(step_sizes_sigma.shape[0]),
                                                          weights_add, weights_mul):
                cur_D = D[cur_n - step_sizes_sigma[cur_step_idx, 0],
                          cur_m - step_sizes_sigma[cur_step_idx, 1]]
                cur_C = cur_w_mul * C[cur_n - max_0, cur_m - max_1]
                cur_C += cur_w_add
                cur_cost = cur_D + cur_C

                # check if cur_cost is smaller than the one stored in D
                if cur_cost < D[cur_n, cur_m]:
                    D[cur_n, cur_m] = cur_cost

                    # save step-index
                    D_steps[cur_n, cur_m] = cur_step_idx

    return D, D_steps


def backtracking(D_steps, step_sizes_sigma):
    wp = []
    # Set starting point D(N,M) and append it to the path
    cur_idx = (D_steps.shape[0] - 1, D_steps.shape[1] - 1)
    wp.append((cur_idx[0], cur_idx[1]))

    # Loop backwards.
    # Stop criteria:
    # Setting it to (0, 0) does not work for the subsequence dtw,
    # so we only ask to reach the first row of the matrix.
    while cur_idx[0] > 0:
        cur_step_idx = D_steps[(cur_idx[0], cur_idx[1])]

        # save tuple with minimal acc. cost in path
        cur_idx = (cur_idx[0] - step_sizes_sigma[cur_step_idx][0],
                   cur_idx[1] - step_sizes_sigma[cur_step_idx][1])

        # append to warping path
        wp.append((cur_idx[0], cur_idx[1]))

    return wp


def dtw(distance_matrix):
    # Default Parameters
    step_sizes_sigma = np.array([[1, 1], [0, 1], [1, 0]])
    weights_add = np.array([0, 0, 0])
    weights_mul = np.array([1, 1, 1])

    max_0 = step_sizes_sigma[:, 0].max()
    max_1 = step_sizes_sigma[:, 1].max()

    # calculate pair-wise distances
    C = distance_matrix

    # initialize whole matrix with infinity values
    D = np.ones(C.shape + np.array([max_0, max_1])) * np.inf

    # set starting point to C[0, 0]
    D[max_0, max_1] = C[0, 0]

    D_steps = np.empty(D.shape, dtype=np.int)

    # calculate accumulated cost matrix
    D, D_steps = calc_accu_cost(C, D, D_steps,
                                step_sizes_sigma,
                                weights_mul, weights_add,
                                max_0, max_1)

    # delete infinity rows and columns
    D = D[max_0:, max_1:]
    D_steps = D_steps[max_0:, max_1:]

    wp = backtracking(D_steps, step_sizes_sigma)
    return D, np.asarray(wp, dtype=int)


def to_chroma(y):
    chroma = y.reshape(-1, 12, y.shape[1]).sum(0)
    norms = np.linalg.norm(chroma, axis=0)
    norms[norms == 0] = 1
    chroma /= norms
    chroma[chroma < 1 / 12] = 0
    return chroma


# Configure meico
meico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meico.jar')
jpype.startJVM(
    jpype.getDefaultJVMPath(),
    '-ea',
    '-Djava.class.path=' + meico_path
)


def calc_alignment(audio_path, mei_path):
    wave_data, sr = librosa.load(audio_path)

    Mei = jpype.JPackage('meico').mei.Mei  # Get Mei class
    try:
        File = jpype.java.io.File  # the Java File class
        mei_file = File(mei_path)
        mei = Mei(mei_file, False)  # Read in MEI data
        mei.addIds()
        mei.exportMsm(720, True, False)  # Generate timestamps with ppq=720, no channel 10, no cleanup
        debug_mei_xml = mei.toXML()
    except jpype.JavaException:
        # TODO Proper exception handling
        sys.stderr.write('Error during processing of MEI file.')

    # Calculate MEI chroma features
    cqt_mei, id_to_index = from_meico(debug_mei_xml)
    chroma_mei = to_chroma(cqt_mei)
    chroma_mei_circular = chroma_mei[circular]

    # Calculate audio chroma features
    # chroma_size = round(len(wave_data) / chroma_mei.shape[1])
    hop_length = 2 ** math.ceil(math.log2(len(wave_data) / chroma_mei.shape[1]))

    # cqt = librosa.feature.chroma_stft(wave_data, sr=sr, hop_length=hop_length)
    # chroma_audio = to_chroma(cqt)
    cqt = librosa.cqt(wave_data, sr=sr, bins_per_octave=12 * 3, n_bins=12 * 8 * 3, tuning=0,
                      fmin=librosa.midi_to_hz(24), hop_length=hop_length)
    cqt_splitted = librosa.magphase(cqt)[0].reshape(-1, 3, cqt.shape[1])
    energy = cqt_splitted.sum(0)
    energy_argmax = np.argmax(energy, axis=0)

    new_cqt = np.empty((12 * 8, cqt_splitted.shape[2]))
    for frame, feature in enumerate(cqt_splitted.T):
        # https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html

        a = energy[(energy_argmax[frame] - 1) % 3, frame]
        b = energy[energy_argmax[frame], frame]
        c = energy[(energy_argmax[frame] + 1) % 3, frame]
        p = 0.5 * (a - c) / (a - 2 * b + c)  # [-0.5, +0.5]

        new_cqt[:, frame] = feature[energy_argmax[frame]] - (
            0.25 * (
            feature[(energy_argmax[frame] - 1) % 3] - feature[(energy_argmax[frame] + 1) % 3]) * p)

        # new_cqt[:, frame] = feature[energy_argmax[frame]]
    chroma_audio = to_chroma(new_cqt)

    # Calculate warping path
    # distances = 1 - np.max(np.matmul(chroma_mei_circular.T, chroma_audio), axis=1)
    distances = cdist(chroma_mei.T, chroma_audio.T)
    # librosa.display.specshow(distances)
    # plt.show()
    path = dtw(distances)[1]

    # path = librosa.dtw(chroma_mei, chroma_audio)[1]
    path_dict = {key: value for (key, value) in path}

    # Extract mappings
    id_to_time = {}
    chroma_length = len(wave_data) / sr / chroma_audio.shape[1]
    for identifier in id_to_index:
        id_to_time[identifier] = path_dict[id_to_index[identifier]] * chroma_length

    return id_to_time


def combine(mei_path, vertaktoid_path, output_path=None):
    mei_xml = etree.parse(mei_path).getroot()
    vertaktoid_xml = etree.parse(vertaktoid_path).getroot()

    facsimile = vertaktoid_xml.xpath('//mei:mei/mei:music/mei:facsimile', namespaces=ns)[0]
    mei_music = mei_xml.xpath('//mei:mei/mei:music', namespaces=ns)[0]
    mei_music.insert(0, facsimile)

    mei_measures = mei_music.xpath('.//*[local-name()="measure"]', namespaces=ns)
    vertaktoid_measures = vertaktoid_xml.xpath('//*[local-name()="measure"]', namespaces=ns)

    if len(mei_measures) == len(vertaktoid_measures):
        for i in range(len(mei_measures)):
            mei_measures[i].set('label', vertaktoid_measures[i].get('n'))
            mei_measures[i].set('facs', vertaktoid_measures[i].get('facs'))
    else:
        sys.stderr.write('Error: Numbers of measures do not match!')

    if output_path is not None:
        etree.ElementTree(mei_xml).write(output_path, encoding='utf-8', xml_declaration=True)


def calc_measure_alignment(alignment, mei_path, output_path=None):
    mei_xml = etree.parse(mei_path).getroot()
    mei_music = mei_xml.xpath('//mei:mei/mei:music', namespaces=ns)[0]

    mei_measures = mei_music.xpath('.//*[local-name()="measure"]', namespaces=ns)
    last = None

    measure_alignment = {}

    for m in mei_measures:
        min_time = np.inf
        for elem in m.xpath('.//*[local-name()="note"]|.//*[local-name()="rest"]'):
            identifier = elem.get('{http://www.w3.org/XML/1998/namespace}id')
            if identifier in alignment:
                min_time = min(alignment[identifier], min_time)
        if min_time == np.inf:
            min_time = last

        m.set('tstamp.ges', str(min_time))
        measure_alignment[m.get('{{{ns}}}id'.format(ns=ns['xml']))] = str(min_time)
        last = min_time

    if output_path is not None:
        etree.ElementTree(mei_xml).write(output_path, encoding='utf-8', xml_declaration=True)

    return measure_alignment


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
    combine(
        'data/source.mei',
        'data/measures_new.mei',
        output_path='data/combined.mei'
    )

    audio_path = os.path.realpath(os.path.join('data', 'Curzon_original.mp3'))
    mei_path = os.path.realpath(os.path.join('data', 'combined.mei'))

    note_alignment = calc_alignment(audio_path, mei_path)
    measure_alignment = calc_measure_alignment(note_alignment, mei_path, output_path='data/aligned.mei')

    image_overlays = calc_image_overlays('data/combined.mei')

    data = {'images': image_overlays, 'alignment': measure_alignment}

    with open('data/dataset.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
