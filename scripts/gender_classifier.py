#!/usr/bin/env python
# Gender classifier
###############################################################################
import sys, os, subprocess, time, codecs, re, shutil, glob
import utils
from nltk.util import ngrams
import nltk

class GenderClassifier:
    def __init__(self):
        self.non_letters = r'^[a-zA-Z ]'
        self.feature_global = set()
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
        process_country_gender(params)
    
    def _nameFeatures(self, name):
        name=name.upper()
        features = {}
        self._addNgramFeatures(name, features, '1')
        self._addVowelFeatures(name, features, '2')
        self._addTrailingFeatures(name, features, '3')

        name_pure = re.sub(self.non_letters, " ", name)
        print name_pure
        self._addNgramFeatures(name_pure, features, '4')
        self._addVowelFeatures(name_pure, features, '5')
        self._addTrailingFeatures(name_pure, features, '6')
        return {
        'last_letter': name[-1],
        'last_two' : name[-2:],
        'last_three': name[-3:],
        'last_is_vowel' : (name[-1] in 'AEIOUY')
        }

    def _addNgramFeatures(self, name, features, prefix):
        for n in range(1,5):
            ngrams = nltk.FreqDist(ngrams(sentence.split(), n))
            for item in ngrams:
                feature_name = '%s-%d-%s' %(prefix, n, item)
                self.feature_global.add('%s-%d-%s' %(prefix, n, item) )
                features[item] = ngrams[item]
    def _addVowelFeatures(self, name, features)
    def _addTrailingFeatures(self, name, features)

                                                                                        }
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: python %s <params-file>' %sys.argv[0]
        sys.exit(1)
    params_file = sys.argv[1]
    assert os.path.isfile(params_file), 'params-file %s is not a valid file!' %params_file
    main(params_file)
