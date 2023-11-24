# ranalyze
recursively compare every file with every other file and give the probability that they had a common ancestor

## Prerequisites

1. vscode
2. python
3. git

To use, open a fresh folder in vscode and open a new terminal

```bash
git clone https://github.com/rhildred/ranalyze.git .
```

Drag and drop a .zip of the files you want to check for common ancestry in to the explorer pane on the left of vscode.

```bash
python ranalyze.py > results.txt
```

`results.txt` will have the probabilities expressed as a percentage that a file had a common ancestor with any other file in the set. Edit this file to 


