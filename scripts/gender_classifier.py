#!/usr/bin/env python
# Gender classifier
###############################################################################
import sys, os, subprocess, time, codecs, re, shutil, glob
import utils
from nltk.util import ngrams
import nltk
from sklearn.ensemble import RandomForestClassifier
from scipy.sparse import csr_matrix
import numpy as np

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
    gen_class.loadData(params['process_country_gender_output_file_gender'])
    print gen_class.predict('Diyi Yang')
    print gen_class.predict('Yang Diyi')
    print gen_class.predict('Yuntian Deng')
    print gen_class.predict('Deng Yuntian')
    print gen_class.predict('Charlotte Riley')
    print gen_class.predict('Qi Guo')
    print gen_class.predict('Guo Qi')
    print gen_class.predict('Eric Xing')
    print gen_class.predict('Yiming Yang')
class GenderClassifier:
    def __init__(self):
        self.non_letters = r'[^a-zA-Z ]'
        self.feature_global = set()
        self.feature_id = {}

    def predict(self, name):
        features = self._nameFeatures(name)
        row = []
        col = []
        data = []
        idx = 0
        for feature in features:
            if feature in self.feature_global:
                row.append(idx)
                col.append(self.feature_id[feature])
                data.append(features[feature])
        row = np.array(row)
        col = np.array(col)
        data = np.array(data)
        X = csr_matrix((data, (row, col)), shape=(1, self.num_fea))
        return self.clf.predict(X)[0]


    def loadData(self, filename):
        features_all = []
        with open(filename, 'r') as fin:
            idx = 0
            for line in fin:
                idx += 1
                if idx % 10000 == 0:
                    print '%d lines read' %idx
                name, gender = line.strip().split('\t')
                features = self._nameFeatures(name, True)
                features_all.append((features, gender))
        idx = 0
        self.num_fea = 0
        for feature in self.feature_global:
            self.feature_id[feature] = idx
            idx += 1
            self.num_fea += 1
        idx = 0
        row = []
        col = []
        data = []
        genders = []
        for features, gender in features_all:
            for feature in features:
                row.append(idx)
                col.append(self.feature_id[feature])
                data.append(features[feature])
            genders.append(int(gender))
            idx += 1
        row = np.array(row)
        col = np.array(col)
        data = np.array(data)
        print row
        print col
        print data
        self.X = csr_matrix((data, (row, col)), shape=(len(features_all), self.num_fea))
        self.Y = np.array(genders)

        self.clf = RandomForestClassifier(n_estimators=10)
        self.clf = self.clf.fit(self.X, self.Y)

    
    def _nameFeatures(self, name, flag=False):
        name=name.upper()
        features = {}
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
