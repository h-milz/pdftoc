# pdftoc

Es existieren eine ganze Reihe guter Fachbücher im PDF-Format aus der Zeit, als noch nicht mit modernen Layoutprogrammen gearbeitet wurde und die Bücher daher nicht gleich auch als PDF erzeugt wurden. Beispiele sind "Meinke/Gundlach: Handbuch der Hochfrequenztechnik", 4. Auflage von 1986 oder "Schiek: Grundlagen der HF-Messtechnik" von 1999. Diese Art PDFs erkennt man daran, dass sie kein klickbares Inhaltsverzeichnis haben, man aber Text mit copy & paste heraus kopieren kann. Technisch wurden diese PDFs erstellt, indem der Verlag die Bücher eingescannt hat und eine OCR-Texterkennung hat darüber laufen lassen. Der erkannte Text wurde dann unsichtbar und möglichst deckungsgleich über die Images gelegt als "PDF-Sandwich". 

Leider ist der Gebrauchswert dieser PDF-Versionen etwas eingeschränkt, weil man im Grunde nur eine Volltextsuche machen kann und Glück haben muss. 

pdftoc ist ein Skript, mit dem dieser Art PDFs ein "richtiges" Inhaltsverzeichnis mit Collapse-Funktion hinzugefügt werden kann. Dazu muss man einmalig den Inhalt als Textdatei erstellen und dem Aufruf von pdftoc mitgeben. Beispiel: 

    pdftoc -f 21 -p Mein-Buch.pdf -c Mein-Buch-Inhalt.txt -v 

Technisch liest pdftoc die PDF-Datei komplett ein und extrahiert den Text in eine Struktur. Diese wird dann nach den in der Inhaltsdatei gelisteten Kapitelüberschriften durchsucht, aus dem jeweils ersten Vorkommen ein Bookmark erzeugt und dem PDF hinzugefügt. 

Mit dem Schalter `-f` sollte man die erste Textseite angeben, in der nach den Kapitelüberschriften gesucht werden soll, sonst findet das Skript das gedruckte Inhaltsverzeichnis und sonst nichts mehr. 

Die Erstellung des Inhalts geht am einfachsten mit copy & paste aus dem PDF in einen Texteditor, aber man kann auch Textextraktion mit Tools wie `pdftotext` oder `pdf2text` (beide Linux) machen. Beispiele sind im Repo gelistet.   Um die Hierarchie der Überschriften richtig zu bauen, muss je Einrückungs-Level ein Space vorangestellt werden.

 
