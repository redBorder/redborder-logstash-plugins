PACKAGE_NAME?=	redborder-logstash-plugins

VERSION?=	$(shell git describe --abbrev=6 --tags HEAD --always | sed 's/-/_/g')

BUILD_NUMBER?= 1

MOCK_CONFIG?=default

RESULT_DIR?=pkgs

all: rpm


SOURCES:
	mkdir -p SOURCES

archive: SOURCES
	cd ../../ && \
	git archive --prefix=$(PACKAGE_NAME)-$(VERSION)/ \
		-o packaging/rpm/SOURCES/$(PACKAGE_NAME)-$(VERSION).tar.gz HEAD
	@echo Running git archive submodules...
	pwd
	cd ../../ &&  pwd && ls &&\
	p=`pwd` && (echo .; git submodule foreach) | while read entering path; do \
			temp="$${path%'}"; \
			temp="$${temp#'}"; \
#			path=$$temp; \
			path=$(echo $$temp | sed "s/'//g"); \
			[ "$$path" = "" ] && continue; \
			(cd $$path && git archive --prefix=$(PACKAGE_NAME)-$(VERSION)/$$path/ HEAD > $$p/tmp.tar && tar --concatenate --file=packaging/rpm/SOURCES/$(PACKAGE_NAME)-$(VERSION).tar.gz $$p/tmp.tar && rm $$p/tmp.tar); \
	done


build_prepare: archive
	mkdir -p $(RESULT_DIR)
	rm -f $(RESULT_DIR)/$(PACKAGE_NAME)*.rpm


srpm: build_prepare
	/usr/bin/mock \
		-r $(MOCK_CONFIG) \
		--define "__version $(VERSION)" \
		--define "__release $(BUILD_NUMBER)" \
		--resultdir=$(RESULT_DIR) \
		--buildsrpm \
		--spec=${PACKAGE_NAME}.spec \
		--sources=SOURCES
	@echo "======= Source RPM now available in $(RESULT_DIR) ======="

rpm: srpm
	/usr/bin/mock \
		-r $(MOCK_CONFIG) \
		--define "__version $(VERSION)"\
		--define "__release $(BUILD_NUMBER)"\
		--resultdir=$(RESULT_DIR) \
		--rebuild $(RESULT_DIR)/$(PACKAGE_NAME)*.src.rpm
	@echo "======= Binary RPMs now available in $(RESULT_DIR) ======="

clean:
	rm -rf SOURCES pkgs

distclean: clean
	rm -f build.log root.log state.log available_pkgs installed_pkgs \
		*.rpm *.tar.gz
