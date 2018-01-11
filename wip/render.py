import os

from verovio import verovio

factor = 1.1

vrv = verovio.toolkit(False)
vrv.setResourcePath(os.path.abspath(os.path.join('verovio', 'data')))
vrv.setScale(int(50 / factor))
# vrv.setPageHeight(int(2970 * factor))
vrv.setPageWidth(int(2100 * factor))
vrv.setAdjustPageHeight(True)
vrv.loadFile(os.path.abspath(os.path.join('data', 'breaks.mei')))

print(vrv.getPageCount())  # Output: 1

for p in range(1, vrv.getPageCount() + 1):
    vrv.renderToSvgFile('output_{}.svg'.format(p), p)
