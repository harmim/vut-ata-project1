# Author: Dominik Harmim <harmim6@gmail.com>

PACK := proj1.zip


.PHONY: pack
pack: $(PACK)

$(PACK): specifikace.md ceg.txt ceg.json ceg.png combine.json combine.png \
		testy.md cartctl/
	zip -r -9 $@ $^


.PHONY: clean
clean:
	rm -rf $(PACK) cartctl/__pycache__/
