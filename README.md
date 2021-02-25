# language Predictor Tool
DS 2000 Fundamentals of Data Science - Spring 2018

Completed individually (not pair programming)

A tool that predicts which language a document is written in given a sample set of documents whose languages you do know.

Method:
  1. Analyze the frequencies of trigrams (3-character subsequence) in the known documents
  2. Collect trigram frequencies in the unknown documents
  3. Cleans all data and normalize all trigram frequencies
  4. Calculate the cosine similarity of trigram collections to match unknown documents to known documents
  5. Generates output that orders the likelihood of which language the unknown documents may be written in from most to least likely. Output structured as such:
      UNKNOWN[#], where the # corresponds to the order of which the unknown files were detected in the input
      [most likely language] [cosine similarity between the unknown file trigrams and the known [most likely language] files' trigrams]
      [2nd most likely language] [cosine similarity between the unknown file trigrams and the known [2nd most likely language] files' trigrams]
      ...
      [least likely language] [cosine similarity between the unknown file trigrams and the known [least likely language] files' trigrams]


In hindsight:
The program takes quite long to run with only the small batch of input files given. The code can most certainly be optimized. 
