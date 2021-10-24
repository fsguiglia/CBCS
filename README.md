# CBCS
Corpus based concatenative synth for Max for Live. CBCS uses a python script to analyze audio files and to distribute them in a 2d grid
using audio descriptors and techniques like PCA and T-SNE. CBCS is now part of [MNT](https://github.com/fsguiglia/concatenate).

### Installing
* Move files to your Ableton Live Library folder
* CBCS uses the MuBu external, you might need to install it
* Python + Librosa, scikit-learn, progressbar and numpy are needed to run the analysis script

### Usage
Create an analysis file using the analyze button, load it, turn on the synth and browse the display. You can change the features being used with the dropdown menus.
The rest of the controls are typical granular synth stuff.
