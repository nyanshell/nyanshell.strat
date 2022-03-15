import math
import os.path
from collections import Counter

import click
import numpy as np
from scipy.io import wavfile
from aubio import source, onset, pitch


A4 = 440
C0 = A4 * pow(2, -4.75)
note_name = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
notes_sharp = ['A', 'Bb', 'B', 'C', 'Dd', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']


def get_note_frequency(note):
    octave = int(note[-1])

    key_number = notes_sharp.index(note[0:-1])

    if key_number < 3:
        key_number += 12

    key_number = key_number + ((octave - 1) * 12) + 1

    return A4 * 2**((key_number - 49) / 12)


def get_note_name(freq):
    h = round(12 * math.log2(freq / C0))
    octave = h // 12
    n = h % 12
    return note_name[n] + str(octave)


def get_freq(sample, samplerate, min_confidence=0.95):
    win_s = 4096  # fft size
    hop_s = 512  # hop size

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("freq")
    pitch_o.set_tolerance(0.8)

    pitches = []
    confidences = []

    for i in range(0, sample.shape[0] - hop_s + 1, hop_s):
        p = pitch_o(sample[i:i + hop_s])[0]
        confidence = pitch_o.get_confidence()
        if confidence >= min_confidence:
            pitches.append(p)
            confidences.append(confidence)

    return np.mean(pitches), np.mean(confidences)


def detect_onsets(wav_fname, samplerate):
    """
    return onsets frames position
    """
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size

    s = source(wav_fname, samplerate, hop_s)
    samplerate = s.samplerate
    o = onset("default", win_s, hop_s, samplerate)
    # list of onsets, in samples
    onsets = []
    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            onsets.append(o.get_last())
            # keep some data to plot it later
        total_frames += read
        if read < hop_s:
            break

    return onsets


def save_samples(samples,
                 onsets,
                 save_path,
                 samplerate,
                 open_string='E2',
                 dynamics='mp',
                 backtrack_length=512,  # -512 to avoid boundary glitch
                 max_sample_seconds=4,
                 dry_run=False,
                 freq_confidence=0.95,
                 save_all=False
                 ):

    sample_cnt = Counter()
    for i in range(0, len(onsets) - 1):
        start_pos = onsets[i] - backtrack_length
        max_end = min(onsets[i + 1], onsets[i] + int(samplerate * max_sample_seconds))
        sample = samples[start_pos:max_end]
        freq, confidence = get_freq(sample[:, 0].astype(np.float32), samplerate, min_confidence=freq_confidence)
        note_name = get_note_name(freq)
        sample_cnt[note_name] += 1
        # draw_graph(data[onsets[i]:max_end])
        click.echo(f'#{i} freq: {freq} note: {note_name} length: {sample.shape[0] / samplerate} confidence: {confidence} total sample {sample_cnt[note_name]}')
        if dry_run:
            continue
        if save_all or click.confirm('save to sample?'):
            wavfile.write(
                os.path.join(
                    save_path,
                    f'{open_string}_{note_name}_{dynamics}_{sample_cnt[note_name]}.wav'),
                samplerate,
                sample)
        else:
            sample_cnt[note_name] -= 1  # exclude sample
    click.echo(f'total notes: {sum(sample_cnt.values())}')


def draw_graph(sample, samplerate):
    import matplotlib.pyplot as plt

    time = np.linspace(0., sample.shape[0] / samplerate, sample.shape[0])
    plt.plot(time, sample[:, 0], label="Left channel")
    plt.plot(time, sample[:, 1], label="Right channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


@click.command()
@click.argument("input_sample", type=str)
@click.argument("save_path", type=str)
@click.option("--open-string", type=str, default='E2')
@click.option("--dynamics", type=str, default='mp')
@click.option("--freq-confidence", type=float, default=0.95)
@click.option("--dry-run", type=bool, is_flag=True)
@click.option("--yes", type=bool, is_flag=True)
def cli(input_sample, save_path, open_string, dynamics, freq_confidence, dry_run, yes):
    samplerate, data = wavfile.read(input_sample)
    onsets = detect_onsets(input_sample, samplerate)
    onsets.append(int(data.shape[0]))
    save_samples(
        data,
        onsets,
        save_path,
        samplerate,
        open_string=open_string,
        dynamics=dynamics,
        dry_run=dry_run,
        freq_confidence=freq_confidence,
        save_all=yes
    )


if __name__ == '__main__':
    cli()
