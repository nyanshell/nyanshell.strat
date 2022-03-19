'''
Generate SFZ file from samples
'''
import os.path
from collections import Counter, defaultdict


string_range = {
    'E2': 'F2	Gb2	G2	Ab2	A2	Bb2	B2	C3	Db3	D3	Eb3	E3	F3	Gb3	G3	Ab3	A3	Bb3	B3	C4	Db4	D4'.split('	'),
    'A': 'Bb2	B2	C3	Db3	D3	Eb3	E3	F3	Gb3	G3	Ab3	A3	Bb3	B3	C4	Db4	D4	Eb4	E4	F4	Gb4	G4'.split('	'),
    'D': 'Eb3	E3	F3	Gb3	G3	Ab3	A3	Bb3	B3	C4	Db4	D4	Eb4	E4	F4	Gb4	G4	Ab4	A4	Bb4	B4	C5'.split('	'),
    'G': 'Ab3	A3	Bb3	B3	C4	Db4	D4	Eb4	E4	F4	Gb4	G4	Ab4	A4	Bb4	B4	C5	Db5	D5	Eb5	E5	F5'.split('	'),
    'B': 'C4	Db4	D4	Eb4	E4	F4	Gb4	G4	Ab4	A4	Bb4	B4	C5	Db5	D5	Eb5	E5	F5	Gb5	G5	Ab5	A5'.split('	'),
    'E4': 'F4	Gb4	G4	Ab4	A4	Bb4	B4	C5	Db5	D5	Eb5	E5	F5	Gb5	G5	Ab5	A5	Bb5	B5	C6	Db6	D6'.split('	'),
}
OPEN_STRINGS = ['E2', 'A', 'D', 'G', 'B', 'E4']
MIDI_START = {
    'E4': 65,  # F4
    'B': 60,  # C4
    'G': 56,  # Ab3
    'D': 51,  # Eb3
    'A': 46,  # Bb2
    'E2': 41,  # F2
}


def gen():
    notes_sep = {}
    notes_cnt = Counter()
    notes_string = defaultdict(list)
    for s, notes in string_range.items():
        for n in notes:
            notes_string[n].append(s)

    for n in notes_string.keys():
        notes_sep[n] = len(notes_string[n])
    with open('strat_basic.sfz', 'w') as fout:
        for s in OPEN_STRINGS:
            midi_key = MIDI_START[s]
            dynamics = 'mp'
            for note in string_range[s]:
                group = f'''
// note {note}
<group>
key={midi_key}
'''
                lovel, hivel = int(127 - 127 / notes_sep[note] * (notes_cnt[note] + 1)) + 1, \
                    int(127 - 127 / notes_sep[note] * notes_cnt[note])
                notes_cnt[note] += 1
                print(note, 'cnt:', notes_cnt[note], 'sep:', notes_sep[note], lovel, hivel)
                vel = f'''
lovel={lovel}
hivel={hivel}
'''
                regions = f'''
<region>
sample=samples\{s.lower()}_{dynamics}\{s}_{note}_{dynamics}_1.wav
hirand=0.333

<region>
sample=samples\{s.lower()}_{dynamics}\{s}_{note}_{dynamics}_2.wav
lorand=0.333
hirand=0.666

<region>
sample=samples\{s.lower()}_{dynamics}\{s}_{note}_{dynamics}_3.wav
lorand=0.666
'''  # noqa
                fout.write(group + vel + regions)
                midi_key += 1


def validate(sample_folder):
    # files = glob('E2_*.wav')
    sample_cnt = 3
    absent_cnt = 0
    for s in ['E2', 'A', 'D', 'G', 'B', 'E4']:
        print(f'open string {s}:')
        for d in ['mp']:
            for note in string_range[s]:
                for i in range(1, sample_cnt + 1):
                    note_file = os.path.join(f'{s.lower()}_{d}/', f'{s}_{note}_{d}_{i}.wav')
                    if not os.path.isfile(os.path.join(sample_folder, note_file)):
                        print(f'missing {note_file}')
                        absent_cnt += 1
    return absent_cnt


if __name__ == '__main__':
    BASE_PATH = os.get('BASE_PATH')  # the sample folder
    assert validate(BASE_PATH) == 0
    gen()
