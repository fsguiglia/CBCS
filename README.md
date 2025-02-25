# HATO
Corpus based concatenative synth for Max for Live. Hato uses a python script to analyze audio files and to distribute them in a 2d grid
using audio descriptors and unsupervised learning. This project is now part of [MNT](https://github.com/fsguiglia/MNT2).

This version of Hato is for Windows only and requires Python and some libraries.
Compiled versions for Windows and MacOS can be found at [https://www.sguiglia.com.ar/hato.html](https://www.sguiglia.com.ar/hato.html).

### Installing
* Move files to your Ableton Live Library folder
* CBCS uses the MuBu external, you might need to install it
* Python + Librosa, scikit-learn, progressbar and numpy are needed to run the analysis script

### Usage
Analyze a folder using the "analyze" button. Turn on the synth and browse the display. You can change the features being used with the dropdown menus. Analysis parameters can be configured editing configure.ini. The rest of the controls are typical granular synth stuff.
