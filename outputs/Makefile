all: ARR PREV EXAMPLE
	rm -f *.aux *.lof *.log *.lot *.fls *.out *.toc *.fdb_latexmk *.synctex.gz *.pdfsync
	echo "example.pdf was generated successfully"	

ARR: ARR_PDF 
	rm -f *.aux *.lof *.log *.lot *.fls *.out *.toc *.fdb_latexmk *.synctex.gz *.pdfsync
	echo "arrival matching was generated successfully"

PREV: PREV_PDF
	rm -f *.aux *.lof *.log *.lot *.fls *.out *.toc *.fdb_latexmk *.synctex.gz *.pdfsync
	echo "previous matching was generated successfully"

EXAMPLE: 
	cp -f ../example.tex example.tex 
	latexmk -cd -f -pdf -interaction=nonstopmode -synctex=1 example.tex >/dev/null 1>/dev/null 2>/dev/null

ARR_PDF: ARR_TEX
	latexmk -cd -f -pdf -interaction=nonstopmode -synctex=1 arrival_matching.tex >/dev/null 1>/dev/null 2>/dev/null

PREV_PDF: PREV_TEX
	latexmk -cd -f -pdf -interaction=nonstopmode -synctex=1 previous_matching.tex >/dev/null 1>/dev/null 2>/dev/null

ARR_TEX: 
	python ../generator.py -w 10 -W 50 -o arrival_matching.tex

PREV_TEX: 
	python ../generator.py -w 10 -W 50 -o previous_matching.tex -c arrival_matching.tex 

clean:
	rm -f *.aux *.lof *.log *.lot *.fls *.out *.toc *.fdb_latexmk *.synctex.gz *.pdfsync

distclean: clean
	rm -f *.pdf *.tex 