# Requires NAME_ROOT to be defined

# Get People Ids
GET_PEOPLE_IDS = $(NAME_ROOT)/src/get_people_ids
GET_PEOPLE_IDS_BIN = $(NAME_ROOT)/bin
# Get People Ids Chinese
GET_PEOPLE_IDS_ZH = $(NAME_ROOT)/src/get_people_ids_zh
GET_PEOPLE_IDS_ZH_BIN = $(NAME_ROOT)/bin
# Get Wiki Names
GET_WIKI_NAMES = $(NAME_ROOT)/src/get_wiki_names
GET_WIKI_NAMES_BIN = $(NAME_ROOT)/bin
# Get Wiki Names Chinese
GET_WIKI_NAMES_ZH = $(NAME_ROOT)/src/get_wiki_names_zh
GET_WIKI_NAMES_ZH_BIN = $(NAME_ROOT)/bin

# third party
NAME_THIRD_PARTY = $(NAME_ROOT)/third_party
NAME_THIRD_PARTY_SRC = $(NAME_THIRD_PARTY)/src
NAME_THIRD_PARTY_INCLUDE = $(NAME_THIRD_PARTY)/include
NAME_THIRD_PARTY_LIB = $(NAME_THIRD_PARTY)/lib
NAME_THIRD_PARTY_BIN = $(NAME_THIRD_PARTY)/bin

NAME_CXX = g++
NAME_CXXFLAGS = -O3 \
           -std=c++11 \
		   -static-libstdc++ \
           -Wall \
		   -Wno-sign-compare \
           -fno-builtin-malloc \
           -fno-builtin-calloc \
           -fno-builtin-realloc \
           -fno-builtin-free \
           -fno-omit-frame-pointer

NAME_INCFLAGS = -I$(NAME_ROOT) -I$(NAME_THIRD_PARTY_INCLUDE)

NAME_LDFLAGS = -Wl,-rpath,$(NAME_THIRD_PARTY_LIB) \
          -L$(NAME_THIRD_PARTY_LIB) \
          -pthread \
          -lglog \
          -lgflags \
          -lboost_thread \
          -lboost_system \
          -lboost_regex \
		  -lboost_filesystem \
		  -lzmq 
