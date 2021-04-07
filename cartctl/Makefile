test:
	python3 cartctl_test.py -b

verb:
	python3 cartctl_test.py -v

.SUFFIXES: .png .gv

.gv.png:
	dot -Tpng -o $@ $<

jarvis.gv: jarvisenv.py
	python3 -c 'import jarvisenv; jarvisenv.Jarvis.TRACKS.export("jarvis.gv")'
