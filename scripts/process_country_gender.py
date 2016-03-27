#!/usr/bin/env python
# Get countries and genders
###############################################################################
import sys, os, subprocess, time, codecs, re, shutil, glob
import utils
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

def process_country_gender(params):
    with codecs.open(params['process_country_gender_input_file'], encoding='utf-8', mode='r') as fin:
        with open(params['process_country_gender_output_file_gender'], 'w') as fgender:
            with open(params['process_country_gender_output_file_country'], 'w') as fcountry:
                line_idx = 0
                male_total = 0
                female_total = 0
                for line in fin:
                    line_idx += 1
                    if line_idx % 10000 == 0:
                        print '%d lines processed' %line_idx
                    id, name, place_of_birth, nationality, male_cnt, female_cnt = line.strip().split('\t')
                    if utils.is_ascii(name):
                        confidence, country = get_place_of_birth(place_of_birth)
                        if (confidence > 0 and 'process_country_gender_confidence' not in params) or ('process_country_gender_confidence' in params and confidence > params['process_country_gender_confidence']):
                            fcountry.write('%s\t%d' %(name, country))
                        else:
                            confidence, country = get_nationality(nationality)
                            if (confidence > 0 and 'process_country_gender_confidence' not in params) or ('process_country_gender_confidence' in params and confidence > params['process_country_gender_confidence']):
                                fcountry.write('%s\t%d' %(name, country))
                        confidence, gender = get_gender(male_cnt, female_cnt)
                        if (confidence > 0 and 'process_country_gender_confidence' not in params) or ('process_country_gender_confidence' in params and confidence > params['process_country_gender_confidence']):
                            fgender.write('%s\t%d\n' %(name, gender))
                            if gender == 1:
                                male_total += 1
                            else:
                                female_total += 1
                print 'Male: %d, Female: %d\n' %(male_total, female_total)

def get_place_of_birth(place_of_birth):
    return [-1, 1]

def get_nationality(nationality):
    return [-1, 1]

def get_gender(male_cnt, female_cnt):
    male_cnt = int(male_cnt)
    female_cnt = int(female_cnt)
    if male_cnt == 0 and female_cnt == 0:
        return [-1, -1]
    if male_cnt > 0 and female_cnt == 0:
        return [1, 1]
    if female_cnt > 0 and male_cnt == 0:
        return [1, 0]
    if float(male_cnt) / female_cnt >= 2:
        return [0.5, 1]
    if float(female_cnt) / male_cnt >= 2:
        return [0.5, 0]
    if male_cnt > female_cnt:
        return [0, 1]
    if female_cnt > male_cnt:
        return [0, 0]
    return [-1, -1]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: python %s <params-file>' %sys.argv[0]
        sys.exit(1)
    params_file = sys.argv[1]
    assert os.path.isfile(params_file), 'params-file %s is not a valid file!' %params_file
    main(params_file)
