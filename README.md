# nyanshell.strat
A virtual electric guitar in [SFZ format](https://sfzformat.com/). Sound samples from a customized Stratocaster American Deluxe.

[Sound sample](https://soundcloud.com/gestalt-baklava-lur/fender-american-deluxesfizz-ievan-polkka?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)

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

## Recording Hardware

| - | - |
| --- | --- |
| neck | ROASTED MAPLE STRATOCASTER® NECK, 22 JUMBO FRETS, 12" |
| body | Fender® DELUXE SERIES STRATOCASTER® ALDER BODY - HSH ROUTING |
| pickup | Fender Tex-Mex Strat |
| string | Ernie Ball 3221 Regular Slinky Nickel Wound Electric Guitar Strings - .010-.046 |
| picks | Jim Dunlop Nylon Guitar Picks, 0.38 mm |
| audio interface | steinberg UR22C |
| DAW | Ableton Live Lite 11 |
