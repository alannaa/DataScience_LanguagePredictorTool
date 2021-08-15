# language Predictor Tool
DS 2000 Fundamentals of Data Science - Spring 2018

A language-prediction tool that predicts which langauge a given document is written in, effective on documents written in one of seven languages included in the sample set.

Method:
<ol>
<li>Create two dictionaries: one for files we do know the language of, and one for unknown files
<li>Read in the input files
<li>Delegate and Store each input file as such:<br>
key = [file name] or [unknown#] where the # corresponds to the order with which the tool encountered the unknown files<br>
value = one long string that is the contents of the file
<li>Clean all data (removing punctuation and spaces)
<li>Collect and analyze the frequency of trigrams (3-character subsequences) in the files
<li>Normalize the trigram frequencies
<li>Calculate the cosine similarity between trigram collections of unknown files and known files
<li>Match the unknown documents with the languages they have the greatest cosine similarity index with
<li>Organize output and store in output file indicated in sys args
</ol>

In hindsight:
The program takes quite long to run with only the small batch of input files given. The code can most certainly be optimized. 
