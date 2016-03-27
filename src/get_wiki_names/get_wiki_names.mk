# Makefile for geting wiki names
GET_WIKI_NAMES_SRC = $(wildcard $(GET_WIKI_NAMES)/*.cpp)
GET_WIKI_NAMES_HDR = $(wildcard $(GET_WIKI_NAMES)/*.hpp)
GET_WIKI_NAMES_OBJ = $(GET_WIKI_NAMES_SRC:.cpp=.o)

get_wiki_names_all: get_wiki_names

get_wiki_names: $(GET_WIKI_NAMES_BIN)/get_wiki_names

$(GET_WIKI_NAMES_BIN)/get_wiki_names: $(GET_WIKI_NAMES_OBJ) $(GET_WIKI_NAMES_BIN)
	$(NAME_CXX) $(NAME_CXXFLAGS) $(NAME_INCFLAGS) \
	$(GET_WIKI_NAMES_OBJ) $(NAME_LDFLAGS) -o $@

$(GET_WIKI_NAMES_OBJ): %.o: %.cpp $(GET_WIKI_NAMES_HDR)
	$(NAME_CXX) $(NAME_CXXFLAGS) -Wno-unused-result $(NAME_INCFLAGS) -c $< -o $@

get_wiki_names_clean:
	rm -rf $(GET_WIKI_NAMES_OBJ)
	rm -rf $(get_wiki_names)

.PHONY: get_wiki_names_clean get_wiki_names_all
