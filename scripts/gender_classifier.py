#!/usr/bin/env python
# Gender classifier
###############################################################################
import sys, os, subprocess, time, codecs, re, shutil, glob
import utils
from nltk.util import ngrams
import nltk
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.externals import joblib
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from scipy.sparse import csr_matrix
import cPickle as pickle
import numpy as np
import random,math

def main(params_file):
    params = {}
    params_file = os.path.realpath(params_file)
    # Figure out the paths
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    app_dir = os.path.dirname(script_dir)
    params['app_dir'] = app_dir

    # Current timestamp
    curr_timestamp = time.strftime("%d_%b_%Y_%H_%M_%S_GMT", time.gmtime())

    # read configuration file and check
    utils.read_config(params_file, params)
    gen_class = GenderClassifier()
    #gen_class.loadData(params['process_country_gender_output_file_gender'], params['gender_classifier_model_file'])
    gen_class.loadModel(params['gender_classifier_model_file'])
    t1 = time.time()
    print gen_class.predict('Diyi Yang')
    t2 = time.time()
    print("Predict Time: %f ms"%((t2-t1)*1000))
    print gen_class.predict('Yuntian Deng')
    print gen_class.predict('Hanyue Liang')
    print gen_class.predict('Lidan Mu')
    print gen_class.predict('Lanxiao Xu')
    print gen_class.predict('Zhiruo Zhou')
    print gen_class.predict('Charlotte Riley')
    print gen_class.predict('Qi Guo')
    print gen_class.predict('Eric Xing')
    print gen_class.predict('Yiming Yang')
class GenderClassifier:
    def __init__(self):
        self.non_letters = r'[^a-zA-Z ]'
        self.feature_global = set()
        self.feature_id = {}
        self.cv = 5
        random.seed(910820)

    def loadModel(self, modelfile_prefix):
        self.clf = joblib.load(modelfile_prefix+'.pkl')
        self.feature_id = pickle.load(file(modelfile_prefix, 'r'))
        self.num_fea = len(self.feature_id)

    def predict(self, name):
        features = self._nameFeatures(name)
        print name
        row = []
        col = []
        data = []
        idx = 0
        for feature in features:
            if feature in self.feature_id:
                row.append(idx)
                col.append(self.feature_id[feature])
                data.append(features[feature])
        row = np.array(row)
        col = np.array(col)
        data = np.array(data)
        X = csr_matrix((data, (row, col)), shape=(1, self.num_fea))
        return self.clf.predict(X)[0]


    def loadData(self, filename, modelfile_prefix):
        row = []
        col = []
        data = []
        genders = []
        feature_idx = 0
        with open(filename, 'r') as fin:
            line_idx = 0
            idx = 0
            for line in fin:
                line_idx += 1
                if line_idx % 1000 == 0:
                    print '%d lines read' %line_idx
                if line_idx > 100000:
                    break
                name, gender = line.strip().split('\t')
                features = self._nameFeatures(name, False)
        	for feature in features:
        	    row.append(idx)
                    if not feature in self.feature_id:
                        self.feature_id[feature] = feature_idx
                        feature_idx += 1
        	    col.append(self.feature_id[feature])
        	    data.append(features[feature])
        	genders.append(int(gender))
        	idx += 1
        idx = 0
        self.num_fea = feature_idx
        print '%d features' %self.num_fea
        
        self.Y = np.array(genders)
        male_cnt = np.count_nonzero(self.Y)
        female_cnt = len(genders) - male_cnt
        ratio = float(female_cnt) / male_cnt
        print np.where(self.Y==1)[0]
        male_inds = np.where(self.Y==1)[0]
        random.shuffle(male_inds)
        female_inds = np.where(self.Y==0)[0]
        random.shuffle(female_inds)
        if ratio < 1:
            male_inds = male_inds[:math.floor(ratio*male_cnt)]
        else:
            female_inds = female_inds[:math.floor(1.0/ratio*female_cnt)]
        inds = np.concatenate([male_inds,female_inds])
        random.shuffle(inds)
        row = np.array(row)
        col = np.array(col)
        data = np.array(data)
        self.Y = self.Y
        print row
        print col
        print data
        self.X = csr_matrix((data, (row, col)), shape=(len(genders), self.num_fea))
        self.X = self.X[inds,:]
        self.Y = self.Y[inds]
        print self.Y
        print len(self.Y)
        print np.sum(self.Y)

        self.clf = tree.DecisionTreeClassifier()
        #self.clf = RandomForestClassifier(n_estimators=1, min_samples_leaf=1)
        #self.clf = svm.SVC()
	t1 = time.time()
        self.clf = self.clf.fit(self.X, self.Y)
	t2 = time.time()
	print("Training Time: %f ms"%((t2-t1)*1000))
        joblib.dump(self.clf, modelfile_prefix+'.pkl') 
	pickle.dump(self.feature_id, file(modelfile_prefix, 'w'))
        print 'Model saved to %s' %modelfile_prefix
        predicted = self.clf.predict(self.X)
        print 'Training Accuracy: %0.2f' %(accuracy_score(self.Y, predicted))

	t1 = time.time()
        scores = cross_validation.cross_val_score(self.clf, self.X, self.Y, cv=self.cv)
	t2 = time.time()
	print("CV Time: %f ms"%((t2-t1)*1000))
        print("CV Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


    
    def _nameFeatures(self, name, flag=False):
        features = {}
        name = re.sub(r' +', ' ', name)
        self._addNgramFeatures(name, features, '7', flag)
        self._addVowelFeatures(name, features, '8', flag)
        self._addTrailingFeatures(name, features, '9', flag)
        name=name.upper()
        self._addNgramFeatures(name, features, '1', flag)
        self._addVowelFeatures(name, features, '2', flag)
        self._addTrailingFeatures(name, features, '3', flag)

        name_pure = re.sub(self.non_letters, " ", name)
        self._addNgramFeatures(name_pure, features, '4', flag)
        self._addVowelFeatures(name_pure, features, '5', flag)
        self._addTrailingFeatures(name_pure, features, '6', flag)
        return features

    def _addNgramFeatures(self, name, features, prefix, flag):
        for n in range(1,5):
            ngrams_dict = nltk.FreqDist(ngrams([ch for ch in name], n))
            for item in ngrams_dict:
                feature_name = '%s-%d-%s' %(prefix, n, item)
                if flag:
                    self.feature_global.add(feature_name)
                features[feature_name] = ngrams_dict[item]
    def _addVowelFeatures(self, name, features, prefix, flag):
        cnt = 0
        for n in range(len(name)):
            if name[n] in 'AEIOUY':
                cnt += 1
        feature_name = prefix
        if flag:
            self.feature_global.add(feature_name)
        features[feature_name] = cnt
    def _addTrailingFeatures(self, name, features, prefix, flag):
        self._addWholeTrailingFeatures(name, features, prefix+'-1', flag)
        self._addFirstTrailingFeatures(name, features, prefix+'-2', flag)
        self._addLastTrailingFeatures(name, features, prefix+'-3', flag)
    def _addWholeTrailingFeatures(self, name, features, prefix, flag):
        for n in range(min([3, len(name)])):
            letters = name[-1-n:]
            feature_name = '%s-%d-%s' %(prefix, n, letters)
            if flag:
                self.feature_global.add(feature_name)
            features[feature_name] = 1
        for n in range(min([3, len(name)])):
            letter = name[-1-n]
            feature_name = '%s-%d-%s' %(prefix, n+3, letter)
            if flag:
                self.feature_global.add(feature_name)
            features[feature_name] = 1
        if name[-1] in 'AEIOUY':
            feature_name = '%s-6-vowel' %prefix
            if flag:
                self.feature_global.add(feature_name)
            features[feature_name] = 1
    def _addFirstTrailingFeatures(self, name, features, prefix, flag):
        names = name.split()
        if len(names) >= 2:
            first_name = names[0]
            self._addNgramFeatures(first_name, features, prefix, flag)
            self._addVowelFeatures(first_name, features, prefix, flag)
            self._addTrailingFeatures(first_name, features, prefix, flag)
            self._addWholeTrailingFeatures(first_name, features, prefix, flag)
    def _addLastTrailingFeatures(self, name, features, prefix, flag):
        names = name.split()
        if len(names) >= 2:
            first_name = names[1]
            self._addNgramFeatures(first_name, features, prefix, flag)
            self._addVowelFeatures(first_name, features, prefix, flag)
            self._addTrailingFeatures(first_name, features, prefix, flag)
            self._addWholeTrailingFeatures(first_name, features, prefix, flag)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: python %s <params-file>' %sys.argv[0]
        sys.exit(1)
    params_file = sys.argv[1]
    assert os.path.isfile(params_file), 'params-file %s is not a valid file!' %params_file
    main(params_file)
