// Date: 2014.09.14

#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <stdint.h>
#include <chrono>
#include <algorithm>
#include <set>
#include <map>
#include <tuple>

#include <boost/filesystem/operations.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/progress.hpp>
#include <boost/tokenizer.hpp>
#include <boost/regex.hpp>
#include <glog/logging.h>
#include <gflags/gflags.h>

DEFINE_string(input_dir, "", "");
DEFINE_string(output_file, "", "");

// trim from start
static inline std::string &ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), std::not1(std::ptr_fun<int, int>(std::isspace))));
    return s;
}

// trim from end
static inline std::string &rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
    return s;
}

// trim from both ends
static inline std::string &trim(std::string &s) {
    return ltrim(rtrim(s));
}

double get_time()
{
	auto start = std::chrono::high_resolution_clock::now();
	auto since_epoch = start.time_since_epoch();
	return std::chrono::duration_cast<std::chrono::duration<double, std::ratio<1, 1>>>(since_epoch).count();
}

void get_filenames(std::string input_dir, std::vector<std::string> &filenames) {

    boost::filesystem::directory_iterator end_itr;
    LOG(INFO) << input_dir;
    for( boost::filesystem::directory_iterator itr(input_dir); itr != end_itr; ++itr)
    {
        if(!boost::filesystem::is_regular_file(itr->status())) continue;
        std::string filename = itr->path().string(); 
        filenames.push_back(filename);
    }
    std::random_shuffle(filenames.begin(), filenames.end());
    std::cout<<filenames.size()<<std::endl;
}

int main(int argc, char* argv[]) {
	google::ParseCommandLineFlags(&argc, &argv, true);
	google::InitGoogleLogging(argv[0]);


    std::srand(unsigned(std::time(0)));

    std::vector<std::string> filenames;

    LOG(INFO)<<"stat";
    get_filenames(FLAGS_input_dir, filenames);
    LOG(INFO)<<"fini";
    boost::regex pId("<id>(.*?)</id>");
    boost::regex pName("<title>(.*?)(\\s*\\(.*?\\)\\s*|)</title>");
    boost::regex pBirth("birth_place\\s*=\\s*(.*?)\\s*\\|");
    boost::regex pNationality("nationality\\s*=\\s*(.*?)\\s*\\|");
    //std::map<int32_t, std::string> name;
    //std::map<int32_t, std::string> country;
    //std::map<int32_t, bool> gender;
    std::set<std::string> male;
    male.insert("He");
    male.insert("he");
    male.insert("His");
    male.insert("his");
    male.insert("him");
    std::set<std::string> female;
    female.insert("She");
    female.insert("she");
    female.insert("Her");
    female.insert("her");
    std::ofstream fout(FLAGS_output_file);
	CHECK(fout.good()) << "Can not open file: " << FLAGS_output_file;
    for (std::string filename: filenames) {
        std::ifstream fin(filename);
	    CHECK(fin.good()) << "Can not open file: " << filename;
        std::stringstream sstream;
        sstream << fin.rdbuf();//read the file
        std::string str = sstream.str();//str holds the content of the file

        boost::smatch result;
        if (boost::regex_search(str, result, pId)) {
            std::string id(result[1].first, result[1].second);
            std::replace(id.begin(), id.end(), '\n', ' ');
            std::replace(id.begin(), id.end(), '\t', ' ');
            id = trim(id);
            fout<<id<<"\t";
            if (boost::regex_search(str, result, pName)) {
                std::string name(result[1].first, result[1].second);
                std::replace(name.begin(), name.end(), '\n', ' ');
                std::replace(name.begin(), name.end(), '\t', ' ');
                name = trim(name);
                fout<<name;
            }
            fout<<"\t";
            if (boost::regex_search(str, result, pBirth)) {
                std::string birth(result[1].first, result[1].second);
                std::replace(birth.begin(), birth.end(), '\n', ' ');
                std::replace(birth.begin(), birth.end(), '\t', ' ');
                birth = trim(birth);
                fout<<birth;
            }
            fout<<"\t";
            if (boost::regex_search(str, result, pNationality)) {
                std::string nationality(result[1].first, result[1].second);
                std::replace(nationality.begin(), nationality.end(), '\n', ' ');
                std::replace(nationality.begin(), nationality.end(), '\t', ' ');
                nationality = trim(nationality);
                fout<<nationality;
            }
            fout<<"\t";
        }

        std::string word;
        int male_cnt = 0, female_cnt = 0;
        while (sstream >> word) {
            if (male.find(word) != male.end()) {
                ++male_cnt;
            } else if (female.find(word) != female.end()) {
                ++female_cnt;
            }
        }
        fout<<male_cnt<<"\t"<<female_cnt;
        fout<<"\n";

    }

	std::cout << "Success!" << std::endl;
    fout.close();
	return 0;
}
