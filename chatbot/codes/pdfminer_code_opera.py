from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import pickle as pkl
import os

import sys
# sys.append('codes/')
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')



def file_Convert(filePathInput,filePathOutput,fileName):
    # Open a PDF file.
    # fp = open('word2007IT.pdf', 'rb')

    fp = open(os.path.join(filePathInput, fileName), 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    def parse_obj(x, page_num, lt_objs):

        # loop over the object list
        for obj in lt_objs:

            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                try:
                    x.append((page_num, obj.bbox[0], obj.bbox[1], obj.height, str(obj.get_text()).replace('\n', ' ').strip()))
                except:
                    x = x

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                parse_obj(x, page_num, obj._objs)

    # loop over all pages in the document
    pos_list = []
    # out_file = open('word2007IT_miner.txt', 'w')
    # raw = open('word2007IT_text.txt', 'w')
    #############################################################################
    fileRawName = '.'.join(fileName.split('.')[:-1])+'.txt'
    fileOutName = '.'.join(fileName.split('.')[:-1])+'_miner.txt'

    out_file = open(os.path.join(filePathOutput, fileOutName), 'w')
    raw = open(os.path.join(filePathOutput, fileRawName), 'w')
    #############################################################################
    for i, page in enumerate(PDFPage.create_pages(document)):

        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        x = []
        parse_obj(x, i, layout._objs)
        y = [ele[-1]+'\n' for ele in x[2:-2]]
        # print(x[2:-2])
        for ele in x[2:-2]:
            raw.write(str(ele[0])+','+str(ele[1])+','+str(ele[2])+','+str(ele[3])+','+str(ele[-1])+'\n')
        out_file.writelines(y)
        z = [(ele[0], ele[1], ele[2], ele[3]) for ele in x[2:-2]]
        pos_list += z

    out_file.close()
    raw.close()
    pkl.dump(pos_list, open(filePathOutput+'/pos_list_'+'.'.join(fileOutName.split('.')[:-1])+'.p', 'wb'))
    # pkl.dump(pos_list, open('pos_list_word2007IT.p', 'wb'))
    print(len(pos_list))
    return os.path.join(filePathOutput, fileOutName)

# x = file_Convert('../clientA/original_files', '../clientA/files/representation', 'sap.pdf')