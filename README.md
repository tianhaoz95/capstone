# Capstone Dataset Tools

## Status

Building:

[![CircleCI](https://circleci.com/gh/tianhaoz95/capstone.svg?style=svg)](https://circleci.com/gh/tianhaoz95/capstone)

Coverage:

[![codebeat badge](https://codebeat.co/badges/30652e8d-9540-40ad-b49f-981310baed78)](https://codebeat.co/projects/github-com-tianhaoz95-capstone-master)

## What does it do?

* convert tex to either html
* parse html to sentences
* GUI used to visualize and label sentences

## Prerequisites

Install Latexml, instructions can be found [here](https://dlmf.nist.gov/LaTeXML/get.html)

Install python dependency `pip3 install -r requirements.txt`

## How to convert tex files

Create a file `meta.json` inside the tex folder which indicates the entry point which has the following format:

```
{
  "tex_filename": "main.tex"
}
```

Put the unzipped tex file folder under `data/tex_files`

Then go to the root dir of the project and run `python3 convert.py`

Once completed, the output html files will be placed in `data/html_files`

## How to label data

Go to the root dir of the project, run `./run_tools.sh`

Then the labeling tool will automatically open in default browser (chrome recommended).

<img width="75%" src="https://raw.githubusercontent.com/tianhaoz95/pics/master/Screen%20Shot%202018-03-07%20at%202.01.21%20PM.png" />

where search will search all the sentences containing the symbol of choice within the document of choice.

<img width="75%" src="https://github.com/tianhaoz95/pics/blob/master/Screen%20Shot%202018-03-07%20at%202.01.51%20PM.png" />

Here is an example of search results, you can edit the labels as strings. To save the changes in json file. "Save to overall" will save it to the overall json file with many documents in it. "Save to separate" will save it to a separate file named as `data/outputs/[document_name]_[symbol_expression].json`. "Save to both" will literally do both as the same time.
