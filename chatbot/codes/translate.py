import goslate
from googletrans import Translator
import time
import sys
import os
# reload(sys)
# sys.setdefaultencoding("utf-8")
import pickle as pkl

def file_trans(filePathInput,filePathOutput,fileName):
	translator = Translator()
	with open(filePathInput+'/'+fileName,'r', encoding='utf8') as f:
		lines = f.readlines()

	lines_trans = []
	for i, line in enumerate(lines):
		line_split =  line.strip().split('.')
		trans = []
		k = 0
		for x in line_split:
			c = 5
			try:
				while c:
					if len(x) > 1:
						# text = str(translator.translate(x.encode('utf-8'), 'en'))
						print x,'xxxxxxxxxxx'
						print unicode(x, 'utf-8'),'hjhhhkhhhhhhh'
						text = str(translator.translate(unicode(x, 'utf-8'), 'en'))
						line_p = text[text.index('text=') + 5: text.index(', pronunciation')]
						trans.append(line_p)
					else:
						trans.append('')
					c = c - 1
			except:
				print('error occured while translating:', x)
				print(i)
				k = 1
				return 'Error'
				break
			final = '.'.join(trans)
			lines_trans.append(final)
	if k == 0:
		out_file = open(os.path.join(filePathOutput, fileName), 'w')
		out_file.writelines(lines_trans)
	return i

