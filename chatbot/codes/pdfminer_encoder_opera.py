import nltk
from nltk.tokenize import sent_tokenize
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import subprocess
import pickle as pkl
from scipy.spatial.distance import cosine
import scipy.spatial.distance as sd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import sys
# sys.append('codes/')
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def search(filePathInput,fileName, question):
	stop_words = set(stopwords.words('english'))
	txt_file = open(os.path.join(filePathInput, fileName),'r')
	orig_sentences = txt_file.readlines()
	txt_file.close()

	pos_list_path = os.path.join(filePathInput, 'pos_list_all.p')
	pos_list = pkl.load(open(pos_list_path, 'rb'))  #################
	assert len(pos_list) == len(orig_sentences)

	for i, ele in enumerate(pos_list):
		orig_sentences[i] = orig_sentences[i].strip()
		if ele[-1] > 12.0:
			if not orig_sentences[i].endswith('.'):
				orig_sentences[i] = orig_sentences[i]+'.'
			if i-1 >= 0:
				if not orig_sentences[i-1].endswith('.'):
					orig_sentences[i-1] = orig_sentences[i-1] + '.'

	data = ' '.join(orig_sentences)

	sentences = sent_tokenize(unicode(data, 'utf-8'))


	module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
	#@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/2"]
	embed = hub.Module(module_url)

	# Reduce logging output.
	tf.logging.set_verbosity(tf.logging.ERROR)

	similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
	similarity_message_encodings = embed(similarity_input_placeholder)

	# if not os.path.isfile(os.path.join(os.curdir, 'sentence_embeddings_word2007IT.pkl')):
	fileName_embed = 'sentence_embeddings_' + '.'.join(fileName.split('.')[:-1]) + '.pkl'
	if not os.path.isfile(os.path.join(os.curdir, filePathInput + '/' + fileName_embed)):
		print('Embedding sentences...')
		with tf.Session() as session:
			session.run(tf.global_variables_initializer())
			session.run(tf.tables_initializer())
			sentence_emneddings = session.run(embed(sentences))
		pkl.dump(sentence_emneddings, open(filePathInput + '/' + fileName_embed, 'wb'))
		print('Embeddings dumped.')
	else:
		sentence_emneddings = pkl.load(open(filePathInput + '/' + fileName_embed, 'rb'))

	def get_nn(que_enconding, question, language, num=3):
		question = question.lower()
		question = ''.join(e for e in question if e.isalnum() or e.isspace())
		word_tokens = word_tokenize(question)
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		x = np.array(que_enconding)
		scores = sd.cdist(x, sentence_emneddings, "cosine")[0]
		sorted_ids = np.argsort(scores)
		ind_list = sorted_ids[0:num]
		Answers = []
		for i, ind in enumerate(ind_list):
			if ind-1 >= 0 and ind + 3 <= len(sentences):
				answer = '\n'.join(sentences[ind:ind + 3])
			elif ind-1 >= 0 and ind+2 <= len(sentences):
				answer = '\n'.join(sentences[ind-1:ind + 2])
			else:
				answer = '\n'.join(sentences[ind])
			Answers.append(answer)

		order = []
		for answer in Answers:
			sentence = answer.split('\n')[0].lower()
			k = 0
			for word in filtered_sentence:
				if word in sentence:
					k += 1
			order.append(k)

		sort_ind = []
		for i in range(3):
			ind = np.argmax(np.array(order))
			sort_ind.append(ind)
			order[ind] = -1

		for ind in sort_ind:
			x = Answers[ind]
			text = str(translator.translate(x, language))
			x = text[text.index('text=') + 5: text.index(', pronunciation')]
			return x

	from googletrans import Translator
	translator = Translator()
	print question,'dhgsjkag'
	# langs = translator.detect(unicode(str(question), 'utf-8'))
	# language = langs.lang
	# text = str(translator.translate(question, 'en'))
	# x = text[text.index('text=') + 5: text.index(', pronunciation')]
	x = 'hsukadgabjklghklDZ'
	language = 'en'
	with tf.Session() as session:
		session.run(tf.global_variables_initializer())
		session.run(tf.tables_initializer())
		quetion_embedding = session.run(embed([x]))

	answer = get_nn(quetion_embedding, question, language, 1)
	return answer
