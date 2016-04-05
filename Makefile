# Assuming this Makefile lives in project root directory
PROJECT := $(shell readlink $(dir $(lastword $(MAKEFILE_LIST))) -f)

NAME_ROOT = $(PROJECT)

include $(NAME_ROOT)/defns.mk

# defined in defns.mk
THIRD_PARTY = $(NAME_THIRD_PARTY)
THIRD_PARTY_SRC = $(NAME_THIRD_PARTY_SRC)
THIRD_PARTY_LIB = $(NAME_THIRD_PARTY_LIB)
THIRD_PARTY_INCLUDE = $(NAME_THIRD_PARTY_INCLUDE)
THIRD_PARTY_BIN = $(NAME_THIRD_PARTY_BIN)

BIN = $(PROJECT)/bin
LIB = $(PROJECT)/lib

NEED_MKDIR = $(BIN) \
             $(THIRD_PARTY_SRC) \
             $(THIRD_PARTY_LIB) \
             $(THIRD_PARTY_INCLUDE)

all: path \
	third_party_all \
	get_wiki_names_all \
	get_wiki_names_zh_all \
	get_people_ids_all \
	get_people_ids_zh_all

path: $(NEED_MKDIR)

$(NEED_MKDIR):
	mkdir -p $@

clean: get_wiki_names_clean \
	get_people_ids_clean \
	get_people_ids_zh_clean
	rm -rf $(BIN) 
	rm -rf $(LIB)

distclean: clean
	rm -rf $(filter-out $(THIRD_PARTY)/third_party.mk, \
		            $(wildcard $(THIRD_PARTY)/*))

.PHONY: all path clean distclean

include $(GET_WIKI_NAMES)/get_wiki_names.mk
include $(GET_WIKI_NAMES_ZH)/get_wiki_names_zh.mk
include $(GET_PEOPLE_IDS)/get_people_ids.mk
include $(GET_PEOPLE_IDS_ZH)/get_people_ids_zh.mk

include $(THIRD_PARTY)/third_party.mk
