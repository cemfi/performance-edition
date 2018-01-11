import os
import sys

import jpype
from lxml import etree

# Configure meico
meico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meico.jar')
jpype.startJVM(
    jpype.getDefaultJVMPath(),
    '-ea',
    '-Djava.class.path=' + meico_path
)


def expand_repetitions(mei_path, mdiv=0):
    mei_xml = etree.parse(mei_path).getroot()

    Mei = jpype.JPackage('meico').mei.Mei  # Get Mei class
    Msm = jpype.JPackage('meico').msm.Msm  # Get Mei class
    try:
        mei_xml = etree.tostring(mei_xml).decode('utf-8')  # Extract MEI data from body
        mei = Mei(mei_xml, False)  # Read in MEI data
        mei.addIds()
        msm = mei.exportMsm(360, True, True).get(mdiv)  # Generate timestamps with ppq=360, no channel 10, no cleanup
        # msm_xml = etree.fromstring(msm.toXML())
        return(msm)

    except jpype.JavaException:
        sys.stderr.write('Error during processing of MEI file.')


msm = expand_repetitions(os.path.join('data', 'breaks.mei'), mdiv=0)
print(etree.fromstring(msm.toXML()))


jpype.shutdownJVM()
