# Makefile for geting wiki names
GET_WIKI_NAMES_ZH_SRC = $(wildcard $(GET_WIKI_NAMES_ZH)/*.cpp)
GET_WIKI_NAMES_ZH_HDR = $(wildcard $(GET_WIKI_NAMES_ZH)/*.hpp)
GET_WIKI_NAMES_ZH_OBJ = $(GET_WIKI_NAMES_ZH_SRC:.cpp=.o)

get_wiki_names_zh_all: get_wiki_names_zh

get_wiki_names_zh: $(GET_WIKI_NAMES_ZH_BIN)/get_wiki_names_zh

$(GET_WIKI_NAMES_ZH_BIN)/get_wiki_names_zh: $(GET_WIKI_NAMES_ZH_OBJ) $(GET_WIKI_NAMES_ZH_BIN)
	$(NAME_CXX) $(NAME_CXXFLAGS) $(NAME_INCFLAGS) \
	$(GET_WIKI_NAMES_ZH_OBJ) $(NAME_LDFLAGS) -o $@

$(GET_WIKI_NAMES_ZH_OBJ): %.o: %.cpp $(GET_WIKI_NAMES_ZH_HDR)
	$(NAME_CXX) $(NAME_CXXFLAGS) -Wno-unused-result $(NAME_INCFLAGS) -c $< -o $@

get_wiki_names_zh_clean:
	rm -rf $(GET_WIKI_NAMES_ZH_OBJ)
	rm -rf $(get_wiki_names_zh)

.PHONY: get_wiki_names_zh_clean get_wiki_names_zh_all
