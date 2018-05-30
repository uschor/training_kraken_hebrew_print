Train a printed-Hebrew Kraken model, according to the [instructions here](http://kraken.re/training.html).
The goal is to quickly test Kraken on Hebrew (i.e. not HTR of a manuscript). 
Since Kraken requires at least 800 lines transcribed text, and the process provided by Kraken is manual, an automation script was developed, to run all the preparations of the lines image-text pairs.
After the  training set is ready, the Kraken model training can be run.

# Source text
The training text used is Genesis book, taken from [Sefaria](https://www.sefaria.org.il/Genesis?lang=he). The text is in Creative Commons license, taken from (http://www.tanach.us/Tanach.xml)

# Requirements
On a Debian Linux (Ubuntu 16.04 works well), install Kraken along with the Python installation and Vagrant image required for the training. [Instruction here](http://kraken.re/).
The script requires:
## Beautiful Soup 4 Python module:
`pip install beautifulsoup4`
## ImageMagic to convert text into images:
`sudo apt-get install imagemagick`

# Training set preparation
Run the script `src/train_kraken_print.py`
The script does the following:
* Breaks the Genesis JSON file into chapters, and for each chapter:
    * Extracts the verses into text file, verse per line.
    * Generates an image, big enough for Kraken - 5000x8000px, using ImageMagic. Since ImageMagic doesn't seem to support LTR, the Hebrew words are reversed. It's simplistic, but works for pure-Hebrew text. For mixed text, bidirectional support is required.
    * Runs the Kraken *ketos* utility, to generate the HTML file, intended for manual transcription
    * Fills the HTML transcription file automatically, with the text from the matching text file.

Running the script generates HTML files of the transcribed images to *./work/ketos_filled_\*.html*, along with byproducts.

## Extract lines image-text pairs
Now that the transcription file are ready, run the Kraken command:
`ketos extract --reorder --output training --normalization NFD work/ketos_filled_*`
The files will be generated into *training/* directory.

# Kraken training
Get and run the Kraken Vagrant virtual machine. Make sure to run Vagrant in the same directory in which the *train_kraken_script.py* script was run:
`vagrant init openphilology/kraken`
`vagrant up`
`vagrant ssh`
In the Kraken VM, run the training command:
`./train.sh /vagrant/training heb_print`
It will take the training set, and train a model called *heb_print*.


