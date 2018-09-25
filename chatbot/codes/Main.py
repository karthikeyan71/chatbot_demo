import sys
# sys.append('codes/')
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import os
import subprocess

import pdfminer_code_opera as pdfcoder
import pdfminer_encoder_opera as encoder 
import translate as fileTranslate
import pickle as pkl




# './chatbot/files/files/converted'
# def files(client_name,filefolderPath = '../clientA/files/converted',originalfilePath = '../clientA/original_files'):
def files(client_name,filefolderPath = './chatbot/files/files/converted',originalfilePath = './chatbot/files/original_files'):
	filesOriginal = os.listdir(originalfilePath)
	filesTranslated = os.listdir(filefolderPath)

	def get_language(filename):
		from googletrans import Translator
		translator = Translator()
		f = open(txt_original, 'r')
		language = 'en'
		for i, line in enumerate(f):
			if i == 0:
				split = line.strip().split('.')
				split = [word for word in split if len(word) > 1]
				line = ' '.join(split)
				langs = translator.detect(line)
				language = langs.lang
				print(language)
				break
		return language

	# filePathInput = '../' + client_name + '/files/converted'
	# filePathOutput = '../' + client_name + '/files/translated'

	filePathInput = './chatbot/files' + '/files/converted'
	filePathOutput = './chatbot/files' + '/files/translated'

	for fileOriginal in filesOriginal:

		out_name = fileOriginal.split('.')[0]+'_miner.txt'
		print(out_name)
		if out_name not in filesTranslated:
			txt_original = pdfcoder.file_Convert(originalfilePath,filefolderPath,fileOriginal)
		else:
			print('already converted')

		txt_original = os.path.join(filefolderPath, out_name)
		if not out_name in os.listdir(filePathOutput):
			fileLanguage = get_language(txt_original)
			if fileLanguage != 'en':
				break_line = fileTranslate.file_trans(filePathInput, filePathOutput, out_name)
				if isinstance(break_line, str):
					if break_line == 'Error':
						continue
			else:
				subprocess.call(['cp',os.path.join(filePathInput, out_name), os.path.join(filePathOutput, out_name)])
				pos_name = 'pos_list_' + out_name.replace('.txt', '.p')
				subprocess.call(['cp', os.path.join(filePathInput, pos_name), os.path.join(filePathOutput, pos_name)])
		else:
			print('already translated.')


	return 'File preparation done.'


# def searchAnswer(client_name, filePathInput='', fileName='all.txt'):
def searchAnswer(question, client_name = 'clientA',filePathInput='', fileName='all.txt'):
	# filePathInput = '../'+client_name + '/files/representation'
	filePathInput = './chatbot/files' + '/files/representation'
	print question,'ques in main'
	answer = encoder.search(filePathInput,fileName, question)
	return answer


# def combineFiles(client_name, converted_path='../clientA/files/translated'):
def combineFiles(client_name, converted_path='./chatbot/files/files/translated'):
	print('combining files')
	# filePath = '../'+client_name + '/files/representation'
	filePath = './chatbot/files' + '/files/representation'
	files = os.listdir(converted_path)

	txt_files = [file for file in files if 'miner' in file and file.endswith('.txt')]
	pkl_files = [file for file in files if file.endswith('.p')]
	print(txt_files, pkl_files)
	assert len(txt_files) == len(pkl_files)

	with open(filePath+'/all.txt', 'w') as outfile:
		for file in txt_files:
			with open(converted_path+'/'+file, 'r') as infile:
				for line in infile:
					outfile.write(line)

	import pickle as pkl
	pos_list_all = []
	for file in txt_files:
		pkl_file = 'pos_list_'+file.replace('.txt', '.p')
		assert pkl_file in pkl_files
		pos_list_path = os.path.join(converted_path, pkl_file)
		pos_list = pkl.load(open(pos_list_path, 'rb'))
		print(len(pos_list))
		pos_list_all += pos_list
	print(len(pos_list_all))
	pkl.dump(pos_list_all, open(os.path.join(filePath, 'pos_list_all.p'), 'wb'))



if __name__ == '__main__':

	# if sys.version_info[0] < 3:
	# 	raise Exception("Must be using Python 3")
	print 'starting code'
	files('clientA')
	combineFiles('clientA')
	print 'file configured'
	A = True
	while A:
		question = input('Ask a question: ').strip()
		answer = searchAnswer(question,client_name='clientA')
		print(answer)
		ex = input('type E to exit: ').strip().lower()
		if ex == 'e':
			A = False
	
