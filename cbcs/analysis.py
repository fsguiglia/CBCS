#!/usr/bin/env python

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import numpy as np
import librosa

import progressbar

import os
import easygui
import argparse
import sys
import json

def main():
	args = {
		"sample_rate": "22050",
		"window_size": "2048",
		"iterations": "1000",
		"learning_rate": "200",
		"perplexity": "30",
		"hop_length": "512",
	}
	analyze(args)

def analyze(args):
	sample_rate = int(args['sample_rate'])
	window_size = int(args['window_size'])
	hop_length = int(args['hop_length'])
	perplexity = int(args['perplexity'])
	learning_rate = int(args['learning_rate'])
	iterations = int(args['iterations'])	
	
	file_position = list()
	Y = np.array([])
	
	#save empty json and exit if no file is provided
	init_path = os.environ['USERPROFILE'] + '//Desktop//'
	audio_files = (easygui.diropenbox(msg='Audio file folder', title='MNT2', default = init_path))
	if audio_files is None:
		error = 'no file to analize'
		print(error)
		save_empty_file(error, new_path)
		sys.exit()

	files = getListOfFiles(audio_files, ['.wav'])
	X = np.array([]).reshape(0, int(sample_rate * 0.5)) #analize half a second, this needs to be tested
	
	#load audio files and get features
	print('loading ' + str(len(files)) + ' files')
	bar = progressbar.ProgressBar(maxval=len(files), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	for index, file in enumerate(files):
		cur_file_position, cur_X = getFilePosition(file, sample_rate)
		for file in cur_file_position:
			file_position.append(file)
		X = np.concatenate((X, cur_X))
		bar.update(index + 1)
	bar.finish()
	
	#save empty json and exit if less than 5 files are provided
	if len(file_position) < 2:
		error = 'not enough data to create map, exiting'
		print(error)
		#save_empty_file(error, new_path)
		sys.exit()
	
	D,F = getFeatures(X, window_size, hop_length)
	#PCA
	PCA = getPCA(D, 2)
	PCA = min_max_normalize(PCA)
	#TSNE
	pca_tsne = getPCA(D, 0.8)
	TSNE = getTSNE(pca_tsne, 2, perplexity, learning_rate, iterations) 
	TSNE = min_max_normalize(TSNE)
	#Features
	flatness = np.zeros((len(file_position),1))
	rms = np.zeros((len(file_position),1))
	centroid = np.zeros((len(file_position),1))
	rolloff = np.zeros((len(file_position),1))
	bandwidth = np.zeros((len(file_position),1))
	for i in range(len(F)):
		flatness[i] = float(F[i]['flatness'])
		rms[i] = float(F[i]['rms'])
		centroid[i] = float(F[i]['centroid'])
		rolloff[i] = float(F[i]['rolloff'])
		bandwidth[i] = float(F[i]['bandwidth'])
	flatness=min_max_normalize(flatness)
	rms=min_max_normalize(rms)
	centroid=min_max_normalize(centroid)
	rolloff=min_max_normalize(rolloff)
	bandwidth=min_max_normalize(bandwidth)
	
	dict_out = dict()
	out = list()
	for i in range(len(file_position)):
		curOut = dict()
		curOut['name'] = file_position[i][0]
		curOut['pos'] = file_position[i][1]
		curOut['tsne_x'] = float(TSNE[i][0])
		curOut['tsne_y'] = float(TSNE[i][1])
		curOut['pca_x'] = float(TSNE[i][0])
		curOut['pca_y'] = float(TSNE[i][1])
		curOut['flatness'] = float(flatness[i])
		curOut['rms'] = float(rms[i])
		curOut['centroid'] = float(centroid[i])
		curOut['rolloff'] = float(rolloff[i])
		curOut['bandwidth'] = float(bandwidth[i])
		curOut['length'] = window_size
		out.append(curOut)
	
	dict_out['samples'] = out
	filename = audio_files + "\cbcs_out.json"
	with open(filename, 'w+') as f:
		json.dump(dict_out, f, indent = 4)
	
	print("saved analysis file as " + filename)
	input("press any key to exit")
	

def getListOfFiles(dirName, extensions):
	listOfFile = os.listdir(dirName)
	allFiles = list()
	for entry in listOfFile:
		fullPath = os.path.join(dirName, entry)
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath, extensions)
		else:
			valid_extension = False
			for extension in extensions:
				if fullPath[-4:] == extension:
					valid_extension = True
					break
			if(valid_extension):
				allFiles.append(fullPath)
	return allFiles

def getFilePosition(file, sample_rate, mode=1):
	y, sr = librosa.load(file, sample_rate)
	y = librosa.to_mono(y)
	shape = int(sample_rate * 0.5)
	#maybe more windows?
	windows = int(y.shape[0] / shape)
	if mode == 0: 
		windows = 0
	X = list()
	D = np.array([]).reshape(0, shape)
	
	for i in range(windows + 1):
		start = int(shape * i)
		end = int(shape * (i + 1))
		if end > y.shape[0]: 
			end = y.shape[0]
		X.append((file, i * 500))
		#pad with zeros if file is shorter than 0.5 seconds, this needs to be tested
		padded = np.zeros(shape)
		padded[:end-start] = y[start:end]
		padded = padded.reshape(1, shape)
		D = np.concatenate((D,padded))
	return X, D
	
def getFeatures(samples, window_size, hop_length):
	#size of stft result is  (window size / 2 + 1) * (samples / hop length + 1)
	shape = int((1 + window_size * 0.5))
	shape *= int(samples[0].shape[0] / hop_length) + 1
	D = np.array([]).reshape(0, shape)
	print('extracting features')
	bar = progressbar.ProgressBar(maxval=samples.shape[0], \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	F = list()
	for index,sample in enumerate(samples):
		sample = sample.T
		S = librosa.stft(sample, n_fft = window_size, hop_length = hop_length)
		m, p = librosa.magphase(S)
		features = {
			'flatness': librosa.feature.spectral_flatness(S=m)[0][0],
			'rms': librosa.feature.rms(S=m)[0][0],
			'centroid': librosa.feature.spectral_centroid(S=m)[0][0],
			'rolloff': librosa.feature.spectral_rolloff(S=m)[0][0],
			'bandwidth': librosa.feature.spectral_bandwidth(S=m)[0][0],
			'length': window_size,
		}
		F.append(features)
		S = np.abs(S)
		S = S.reshape(S.shape[0] * S.shape[1])
		S = S.reshape(1, shape)
		D = np.concatenate((D, S))
		bar.update(index + 1)
	bar.finish()
	return D, F

def getPCA(data, components):
	print('Principal component analysis (this can take a while)')
	pca = PCA(n_components=components)
	pca.fit(data)
	Y = pca.transform(data)
	print('done, ' + str(Y.shape[1]) + ' components')
	return Y

def getTSNE(data, components, perplexity, learning_rate, iterations):
	print('t-distributed stochastic neighbor embedding (this can take a while)')
	tsne = TSNE(n_components = components,
			 perplexity = perplexity,
			 learning_rate = learning_rate,
			 n_iter = iterations,
			 verbose = 1,
			 )
	Y = tsne.fit_transform(data)
	print('done!')
	return Y

def min_max_normalize(a):
	a = np.transpose(a)
	max_values = np.amax(a,1)
	min_values = np.amin(a,1)
	a = np.transpose(a)
	norm = (a - min_values) / (max_values - min_values)
	return norm

def save(data, files, output_file):
	out = dict()
	points = dict()
	for i in range(len(files)):
		curOut = dict()
		curOut['name'] = files[i][0]
		curOut['pos'] = files[i][1]
		curOut['x'] = float(data[i][0])
		curOut['y'] = float(data[i][1])
		points[i] = curOut
	
	out['points'] = points
	with open(output_file, 'w+') as f:
		json.dump(out, f, indent = 4)

def save_empty_file(error, output_file):
	out = dict()
	out["error"] = error
	with open(output_file, 'w+') as f:
		json.dump(out, f, indent = 4)
		
main()