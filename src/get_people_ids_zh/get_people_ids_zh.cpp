#include <cstdio>
#include <cstdlib>
#include <string>
#include <cstring>
#include <boost/regex.hpp>
#define MAXLENGTH 1000000000
int main(void) {
    FILE *fp, *fp2;
    char *line;
    char str[1000000], buff[1000000];
    line = new char[MAXLENGTH];
    size_t len = 0;
    ssize_t read;
    fp = fopen("data/zhwiki/zhwiki-20160305-categorylinks.sql", "r");
    fp2 = fopen("data/person-id-zh.txt", "w");

    boost::regex expr{".*人物"};
    int idx = 0;
    while ((read = getline(&line, &len, fp)) != -1) {
        if (idx % 100 == 0) {
            printf("%d\n", idx);
        }
        ++idx;
        sscanf(line, "%s", str);
        std::string str2(str);
        if (str2.compare("INSERT") == 0) {
            int len = strlen(line);
            char *ptr = line;
            char *ptr2 = NULL;
            while (ptr != (line+len)) {
                while (*ptr != '(')
                    ++ptr;
                ++ptr;
                int id = strtol(ptr, &ptr2, 10);
                ptr = ptr2;
                ++ptr;++ptr;
                ptr2 = ptr;
                bool flag = false; 
                while (*ptr2 != '\'') {
                    if (flag) {
                        flag = false;
                        ++ptr2;
                        continue;
                    }
                    if (*ptr2 == '\\')
                        flag = true;
                    ++ptr2;
                }
                *ptr2 = '\0';
                strcpy(buff, ptr);
                str2 = buff;
                if (boost::regex_match(str2, expr)) {
                    fprintf(fp2, "%d\n", id);
                }
                ptr = ptr2+1;
                if (ptr >= (line+len))
                    break;
                while ((*ptr != '(') && (ptr < (line+len))) {
                    if (*ptr == '\'') {
                        ptr2 = ptr;
                        bool flag = false; 
                        while (*ptr2 != '\'') {
                            if (flag) {
                                flag = false;
                                ++ptr2;
                                continue;
                            }
                            if (*ptr2 == '\\')
                                flag = true;
                            ++ptr2;
                        }
                        ptr = ptr2;
                    }
                    ++ptr;
                }

            }
        }

    }
    delete []line;

    fclose(fp);
    fclose(fp2);
}
