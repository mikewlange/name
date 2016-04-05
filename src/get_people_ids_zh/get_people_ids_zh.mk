# Makefile for geting wiki names
GET_PEOPLE_IDS_ZH_SRC = $(wildcard $(GET_PEOPLE_IDS_ZH)/*.cpp)
GET_PEOPLE_IDS_ZH_HDR = $(wildcard $(GET_PEOPLE_IDS_ZH)/*.hpp)
GET_PEOPLE_IDS_ZH_OBJ = $(GET_PEOPLE_IDS_ZH_SRC:.cpp=.o)

get_people_ids_zh_all: get_people_ids_zh

get_people_ids_zh: $(GET_PEOPLE_IDS_ZH_BIN)/get_people_ids_zh

$(GET_PEOPLE_IDS_ZH_BIN)/get_people_ids_zh: $(GET_PEOPLE_IDS_ZH_OBJ) $(GET_PEOPLE_IDS_ZH_BIN)
	$(NAME_CXX) $(NAME_CXXFLAGS) $(NAME_INCFLAGS) \
	$(GET_PEOPLE_IDS_ZH_OBJ) $(NAME_LDFLAGS) -o $@

$(GET_PEOPLE_IDS_ZH_OBJ): %.o: %.cpp $(GET_PEOPLE_IDS_ZH_HDR)
	$(NAME_CXX) $(NAME_CXXFLAGS) -Wno-unused-result $(NAME_INCFLAGS) -c $< -o $@

get_people_ids_zh_clean:
	rm -rf $(GET_PEOPLE_IDS_ZH_OBJ)
	rm -rf $(get_people_ids_zh)

.PHONY: get_people_ids_zh_clean get_people_ids_zh_all
