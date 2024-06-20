# pdftoc

`pdftoc` ist ein Tool, mit dem man bestimmten eBooks wie Fachbüchern im PDF-Format nachträglich ein "richtiges" Inhaltsverzeichnis ("table of contents", toc) hinzufügen kann. 

## Motivation

Es existieren eine ganze Reihe guter Fachbücher im PDF-Format aus der Zeit, als noch nicht mit modernen Layoutprogrammen gearbeitet wurde und die Bücher daher nicht gleich auch als PDF erzeugt wurden. Diese wurden ursprünglich mit normalem Buchdruck erstellt und später von den Verlagen nachträglich digitalisiert, indem man die Bücher eingescannt und den Buchtext behelfsweise und teilweise ziemlich halbseiden per OCR-Texterkennung extrahiert hat.  Der erkannte Text wurde dann unsichtbar und möglichst deckungsgleich über die Bilder gelegt als "PDF-Sandwich". Diese Art PDFs erkennt man daran, dass sie kein klickbares Inhaltsverzeichnis haben, man aber Text mit copy & paste heraus kopieren kann. 

Beispiele sind "Meinke/Gundlach: Handbuch der Hochfrequenztechnik", 4. Auflage von 1986 oder "Schiek: Grundlagen der HF-Messtechnik" von 1999. 

Leider ist der Gebrauchswert dieser eBooks etwas eingeschränkt, weil man im Grunde nur eine Volltextsuche machen kann und Glück haben muss, dass der OCR'te Text einigermaßen passt.  

## Aufruf

Um `pdftoc` verwenden zu können, muss man einmalig den Inhalt des Buchs als Textdatei erstellen und dem Aufruf von pdftoc mitgeben. Beispiel: 

    pdftoc -f 21 -p Mein-Buch.pdf -c Mein-Buch-Inhalt.txt

Technisch liest pdftoc die PDF-Datei komplett ein und extrahiert den Text in eine Struktur. Diese wird dann nach den in der Inhaltsdatei gelisteten Kapitelüberschriften fehlertolerant durchsucht (Python fuzzy search), aus dem jeweils ersten Vorkommen ein Bookmark erzeugt und dem PDF hinzugefügt. 

Mit dem Schalter `-f` sollte man die erste Textseite angeben, in der nach den Kapitelüberschriften gesucht werden soll, sonst findet das Skript das gedruckte Inhaltsverzeichnis und sonst nichts mehr. 

Der Schalter `-v` erzeugt eine verbose Ausgabe, `-v -v` eine sehr verbose Ausgabe mit Debug-Informationen. 

Die Konvertierung geschieht in place, d.h. das Original-PDF wird überschrieben. Am besten vorher eine Kopie erstellen. 

Die Erstellung des Inhalts geht am einfachsten mit copy & paste aus dem PDF in einen Texteditor, aber man kann auch Textextraktion mit Tools wie `pdftotext` oder `pdf2text` (beide Linux) machen. Beispiele, wie das nachher aussehen sollte, finden sich im Repo. Um die Hierarchie der Überschriften richtig zu bauen, muss je Einrückungs-Level ein Space vorangestellt werden.

## Kompatibilität mit verschiedenen Betriebssystemen

Das Skript wurde in "Pure Python" unter Linux erstellt und sollte damit auch auf anderen Betriebssystemen lauffähig sein, wenn die Abhängigkeiten erfüllt sind (Python 3, `regex`, `getopt`, `sys` sowie `pymupdf` bzw. `fitz`). Das müsste mal jemand testen. Eine grafische Oberfläche gibt es aktuell nicht, aber das sollte mit `tkinter`, `PyQt` oder `wxWidgets` nicht schwierig sein.  Mehr als die obigen 3.14159 Parameter muss man ja nicht abfragen. Hilfe ist willkommen! 

TODO: Auch Bücher, die keinen Sandwich-Text enthalten, sondern nur die gescannten Bilder, lassen sich damit aufwerten, indem man das Inhaltsverzeichnis mit Seitenzahlen erstellt. In dem Fall der Buchtext nicht durchsucht, sondern das TOC einfach "as-is" eingebaut. 

Aus urheberrechtlichen Gründen kann ich keine fertigen aufgewerteten eBooks verteilen, daher müssen Anwender:innen die Konvertierung selbst durchführen. Was wir aber machen können: jede:r, die einen Inhalt erstellt, kann ihn hier mit genauen Angaben zu Buchtitel, Auflage und Erscheinungsjahr hier rein stellen. So entsteht vielleicht im Laufe der Zeit eine kleine Sammlung und alle haben was davon. 

## Copyright-Informationen

`pdftoc` ist Copyright 2024 Harald Milz <harald.milz@tum.de> und wird lizenziert unter der GNU General Public License Version 3 oder später. Der Lizenztext liegt dem Programm bei oder ist im Repo enthalten. 



 
