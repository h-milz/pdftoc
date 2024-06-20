#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program is Copyright (C) Harald Milz <harald.milz@tum.de>, and licensed under the 
GNU General Public License V3 (https://www.gnu.org/licenses/gpl-3.0). You should have received 
a copy if the license together with this program, if not, check the web page. 

As for warranty and liability information, see sections 15 and 16 of the license. 
"""

"""
First step: 
- extract content file from the PDF text, one line per entry, e.g. with 
  pdftotext -f 8 -p Meinke-Gundlach\ Taschenbuch\ der\ Hochfrequenztechnik.pdf  -c inhalt.txt
- review and adjust if necessary. The final content file should look e.g. like this:     
    
A Einleitung
 1 Hinweise zur Benutzung des Taschenbuchs
 2 Physikalische Größen, ihre Einheiten und Formelzeichen
 3 Schreibweise physikalischer Gleichungen
 4 Frequenzzuordnungen
B Elektromagnetische Felder und Wellen
 1 Grundlagen
  1.1 Koordinatensysteme
  1.2 Differentialoperatoren
  1.3 Maxwellsche Gleichungen    
    
"""    

import regex as re
import getopt, sys
import fitz              # a.k.a. pymupdf

def usage():
    print (f'usage {sys.argv[0]} -p "pdf file" -c "content file" [-f first] [-v]')

try:
    opts, args = getopt.getopt(sys.argv[1:], "hp:c:f:l:v", ["help", "pdffile=", "content=", "first=", "verbose"])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(1)

# Vorsicht Baustelle! Eltern haften für ihre Kinder! 
# das fliegt noch raus. 
pdffile = "/home/hm/aTUM/Hochfrequenztechnik/Meinke-Gundlach Taschenbuch der Hochfrequenztechnik.pdf"
pdffile = "/home/hm/aTUM/Hochfrequenztechnik/Gronau-Höchstfrequenztechnik-new.pdf"
content = "/home/hm/aTUM/Hochfrequenztechnik/Meinke-Gundlach-inhalt.txt"
content = "/home/hm/aTUM/Hochfrequenztechnik/Gronau-inhalt.txt"

# Konfiguration
fuzzy0 = "e<=1"  # for the chapter number - this may be too much for very short chapter number, but ... 
fuzzy1 = "e<=2"  # for the first 15 characters of the heading
first = 16
verbose = 2
dist = 2
maxchars = 15           # should be an option

for opt, arg in opts:
    if opt in ("-p", "--pdffile"):
        pdffile = arg
    elif opt in ("-c", "--content"):
        content = arg
    elif opt in ("-f", "--first"):
        first = arg
    elif opt in ("-v", "--verbose"):
        verbose = verbose + 1
    elif opt in ("-h", "--help"):
        usage
        sys.exit(1)
    else:
        assert False, "unhandled option"

if (pdffile == "" or content == ""):
    usage
    sys.exit(1)

# first, read content file 
with open(content, "r", encoding="utf-8") as file:
    search_terms = [line.rstrip() for line in file]

# create empty toc
toc = []

# open PDF file
doc = fitz.open(pdffile)

# create list for the textpages
textpage = []                   # this is zero based, but pymupdf's page counting is 1-based, so .. 
textpage.append("dummytext")    # .. we'll create a dummy entry for page 0

# read complete document into a list of text / html pages
# as opposed to pdf2txt, will not interpret \n between chapter and heading,
# hence the regex will need to allow for \n's between the parts
for page in doc:
    text = page.get_text('text')
    textpage.append(text)    

# skip over the scanned content or whatever there is. 
cur_page = first
# process the search terms one by one
for termnum in range(len(search_terms)):
    term = search_terms[termnum]
    sterm = term.lstrip()           # we'll need this multiple times
    # TODO: extract the page number if we have a full TOC. 
    if (verbose > 0):
        print ("looking for term {}, '{}'".format(termnum, sterm))
    # split term in 2 parts at the first space: chapter number, heading
    (chapter, heading) = sterm.split(' ', 1)
    # search pattern: 
    # - chapter with max fuzzy0 errors
    # - 1..dist arbitrary characters (will normally be \n or \s)
    # - maxchars characters of heading with max fuzzy1 errors
    # this being said, why do we need to split at all? Answer: because we do not want
    # the chapter number to have more than 1 error, while we allow more errors for the heading itself. 
    pattern = re.compile(rf"({re.escape(chapter)}){{{fuzzy0}}}(.{{1,{dist}}})({re.escape(heading[:maxchars])}){{{fuzzy1}}}")
    if (verbose > 1):
        print ("pattern = '{}'".format(pattern.pattern))
        print ("searching from page number {}".format(cur_page))
    # search the text pages from the current page to the end. 
    # If a match was found, add bookmark and look for the next search term 
    # beginning at the current page
    # if none is found until the end of the document, start over with next term, beginning at current page. 
    for pagenum in range (cur_page, len(textpage)):
        match = re.search(pattern, textpage[pagenum])        
        if (match): #  and match.start() > 20):
            if (verbose > 1):
                print (match)
                print ("page = {}, group = {}".format(pagenum, match.group().lstrip()))
 
            # by convention, the number of spaces gives the indentation / layer
            # must be >= 1
            layer = len(term) - len(sterm) + 1
            toc.append([layer, sterm, pagenum])
 
            if (verbose > 0):
                print ("adding bookmark {}, '{}', {}".format(layer, sterm, pagenum))
                print ("")
            # now we need to look for the next search term beginning at the current page
            cur_page = pagenum
            break

# this does all the heavy lifting
doc.setToC(toc)
doc.save(doc.name, incremental=True, encryption=0)
doc.close()

