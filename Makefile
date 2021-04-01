# Author: Dominik Harmim <harmim6@gmail.com>

PACK := proj1.zip


.PHONY: pack
pack: $(PACK)

$(PACK): specifikace.md ceg.txt combine.json testy.md cartctl/
	zip -r $@ $^


.PHONY: clean
clean:
	rm -f $(PACK)
