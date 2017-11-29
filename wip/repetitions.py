"""Script to detect repetitions in an audio recording when the corresponding MEI file is given."""

import os
import sys

import jpype
import librosa
from lxml import etree

# Configure meico
meico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meico.jar')
jpype.startJVM(
    jpype.getDefaultJVMPath(),
    '-ea',
    '-Djava.class.path=' + meico_path
)


def get_repetitions_map(audio_path, mei_path, mdiv=0):
    # audio_data, sr = librosa.load(audio_path)
    mei_xml = etree.parse(mei_path).getroot()

    Mei = jpype.JPackage('meico').mei.Mei  # Get Mei class
    Msm = jpype.JPackage('meico').msm.Msm  # Get Mei class
    try:
        mei_xml = etree.tostring(mei_xml).decode('utf-8')  # Extract MEI data from body
        mei = Mei(mei_xml, False)  # Read in MEI data
        mei.addIds()
        msm = mei.exportMsm(360, True, True).get(mdiv)  # Generate timestamps with ppq=360, no channel 10, no cleanup
        msm_xml = etree.fromstring(msm.toXML())


        possibilities = []
        gotos = msm_xml.xpath('//*[local-name()="goto"]')
        for g in gotos:
            del g.attrib['target.id']
            print(etree.tostring(g).decode())

    except jpype.JavaException:
        sys.stderr.write('Error during processing of MEI file.')


get_repetitions_map('', 'data/source_fing_mdiv.mei', mdiv=0)

jpype.shutdownJVM()
