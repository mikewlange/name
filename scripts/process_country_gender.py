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
    assert 'process_country_gender_countries' in params
    assert 'process_country_gender_cities' in params
    country_dict = {}
    city_dict = {}
    country_id = {}
    with codecs.open(params['process_country_gender_countries'], encoding='utf-8', mode='r') as fin:
        lines = fin.readlines()
        for i in range(1,len(lines)):
            line = lines[i]
            fips,iso,tsd,country = line.strip().split('\t')
            country = country.lower()
            country_dict[country] = i-1
            country_id[fips] = country
    with codecs.open(params['process_country_gender_cities'], encoding='utf-8', mode='r') as fin:
        city_dict_tmp = {}
        lines = fin.readlines()
        for i in range(1,len(lines)):
            line = lines[i]
            if len(line.strip().split('\t')) != 2:
                continue
            fips,city = line.strip().split('\t')
            city = city.lower()
            if city in city_dict_tmp:
                city_dict_tmp[city] = 'NOTACOUNTRY'
            else:
                city_dict_tmp[city] = country_id[fips]

    with codecs.open(params['process_country_gender_output_country_id'], encoding='utf-8', mode='w') as fout:
        countries = country_dict.keys()
        countries = sorted(countries)
        for country in countries:
            fout.write('%s\t%d\n'%(country, country_dict[country]))
    city_dict = {key:city_dict_tmp[key] for key in city_dict_tmp if not city_dict_tmp[key] == 'NOTACOUNTRY'}
    city_dict_opt = {}
    for city in city_dict:
        city_tmp = city_dict_opt
        for i in range(len(city)):
            c = city[i]
            if c not in city_tmp:
                city_tmp[c] = ['N',{}]
            if i == len(city)-1:
                city_tmp[c][0] = country_dict[city_dict[city]]
            city_tmp = city_tmp[c][1]
    city_dict = city_dict_opt

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
                        confidence, country = get_place_of_birth(place_of_birth, city_dict, country_dict)
                        if (confidence > 0 and 'process_country_gender_confidence' not in params) or ('process_country_gender_confidence' in params and confidence > params['process_country_gender_confidence']):
                            fcountry.write('%s\t%d\n' %(name, country))
                        else:
                            confidence, country = get_nationality(nationality, city_dict, country_dict)
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

non_letters = r'[^a-zA-Z ]'
def get_place_of_birth(place_of_birth, city_dict, country_dict):
    place_of_birth = re.sub(non_letters, " ", place_of_birth)
    place_of_birth = re.sub(r'\s+', " ", place_of_birth)
    place_of_birth = place_of_birth.strip()
    if len(place_of_birth) == 0:
        return [-1,-1]
    place_of_birth = place_of_birth.lower()
    for country in country_dict:
        if place_of_birth.find(country) > 0:
            return [1, country_dict[country]]
    i = 0
    last_space = 0
    city_tmp = city_dict
    flag = True
    while i < len(place_of_birth):
        c = place_of_birth[i]
        if c in city_tmp:
            if city_tmp[c][0] != 'N':
                return [1, city_tmp[c][0]]
            city_tmp = city_tmp[c][1]
            i = i + 1
            if c == ' ' and flag:
                last_space = i
                flag = False
        else:
            if flag:
                while i < len(place_of_birth) and place_of_birth[i] != ' ':
                    i = i + 1
                i = i + 1
            else:
                i = last_space
            flag = True
            city_tmp = city_dict

    #for city in city_dict:
    #    if place_of_birth.find(city) > 0:
    #        return [1, city_dict[city]]
    return [-1, -1]

def get_nationality(nationality, city_dict, country_dict):
    return get_place_of_birth(nationality, city_dict, country_dict)

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
