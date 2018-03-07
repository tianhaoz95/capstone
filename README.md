# Capstone Dataset Tools

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
