# Makefile for geting wiki names
GET_PEOPLE_IDS_SRC = $(wildcard $(GET_PEOPLE_IDS)/*.cpp)
GET_PEOPLE_IDS_HDR = $(wildcard $(GET_PEOPLE_IDS)/*.hpp)
GET_PEOPLE_IDS_OBJ = $(GET_PEOPLE_IDS_SRC:.cpp=.o)

get_people_ids_all: get_people_ids

get_people_ids: $(GET_PEOPLE_IDS_BIN)/get_people_ids

$(GET_PEOPLE_IDS_BIN)/get_people_ids: $(GET_PEOPLE_IDS_OBJ) $(GET_PEOPLE_IDS_BIN)
	$(NAME_CXX) $(NAME_CXXFLAGS) $(NAME_INCFLAGS) \
	$(GET_PEOPLE_IDS_OBJ) $(NAME_LDFLAGS) -o $@

$(GET_PEOPLE_IDS_OBJ): %.o: %.cpp $(GET_PEOPLE_IDS_HDR)
	$(NAME_CXX) $(NAME_CXXFLAGS) -Wno-unused-result $(NAME_INCFLAGS) -c $< -o $@

get_people_ids_clean:
	rm -rf $(GET_PEOPLE_IDS_OBJ)
	rm -rf $(get_people_ids)

.PHONY: get_people_ids_clean get_people_ids_all
