# nyanshell.strat
A virtual electric guitar in [SFZ format](https://sfzformat.com/). Sound samples from a customized Stratocaster American Deluxe.

## Use

- Open your DAW, e.g., Ableton Live, Studio One, etc.
- Add an SFZ player, e.g., [sfizz](https://github.com/sfztools/sfizz)
- load `strat_basic.sfz`

## Generate new samples

* Record sound samples from F2 to D6 in `.wav` format, save each open string\'s sample into a single file.
* Make folders to save sound samples (same structure as the project).
* Run parser. e.g, to genrate samples from D string's wave file: ``` > python parser/parse.py <wav-file-of-d-string> samples/d_mp/ --open-string D --freq-confidence 0.95```
* Run sfz generator: ```> BASE_PATH=<sample-folder> python parser/gen.py```

## TODO

- Add samples in dynamics _mf_ and _f_ .
- Add some common chords.
