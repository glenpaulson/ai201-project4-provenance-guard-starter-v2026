"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    Returns:
        A float, 0.0 upwards. **Higher means more human.**

    This is the standard deviation of the sentence lengths divided by the
    average sentence length. Dividing by the average is what makes a long piece
    and a short piece comparable: a text with sentences of 5 and 15 words is
    just as lumpy as one with sentences of 50 and 150, and I want both to come
    out the same.

    A text with one sentence gets 0.0. There is genuinely no spread in one
    sentence, and `statistics.stdev` raises on fewer than two values, so I have
    to pick something. 0.0 means "reads as even", which pushes a one sentence
    submission towards the machine end. I am choosing that on purpose: a one
    sentence submission is too short for me to defend any answer about, and my
    MIN_TEXT_CHARS check in app.py refuses most of them before they get here.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]

    if len(lengths) < 2:
        return 0.0

    average = statistics.mean(lengths)
    if average == 0:
        return 0.0

    return statistics.stdev(lengths) / average


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0 and 1. **Higher means more human**, because it means
        more varied vocabulary.

    The catch, which I have to remember when I read the numbers: this falls as
    text gets longer, because ordinary words like "the" keep coming back. A
    1,000 word piece will score lower than a 100 word piece even if the same
    person wrote both. So this number is not comparable between texts of very
    different lengths, and if my test pieces vary a lot in length that alone
    can look like a signal when it is really just arithmetic.
    """
    all_words = words(text)
    if not all_words:
        return 0.0

    return len(set(all_words)) / len(all_words)


# The marks I count. Full stops are left out on purpose: every sentence ends
# with one, so counting them mostly measures how many sentences there are,
# which the first measure already covers. These are the optional ones, the
# marks a writer chooses to use.
INTERESTING_MARKS = ",;:!?()[]-—–"


def punctuation_density(text: str) -> float:
    """
    How much optional punctuation there is, per word.

    Returns:
        A float, 0.0 upwards. **Higher means more human** is the direction I am
        assuming, and section 2 of my notes says how I checked it rather than
        assuming it.

    I count only the marks in INTERESTING_MARKS above. The reasoning is that a
    full stop is not a choice, it is the end of a sentence, but a semicolon or
    a dash or a pair of brackets is something a writer decided to reach for.
    Those vary much more between people than full stops do.
    """
    all_words = words(text)
    if not all_words:
        return 0.0

    marks = sum(1 for ch in text if ch in INTERESTING_MARKS)
    return marks / len(all_words)


# ── Combining them ───────────────────────────────────────────────────────────

# ── Turning raw measures into comparable scores ──────────────────────────────
#
# All three of my measures point the same way: higher means more human. But
# they are on completely different scales. Type token ratio sits between 0 and
# 1, punctuation density came out between 0.000 and 0.107, and spread ran from
# 0.140 to 0.890. If I just averaged the raw numbers, type token ratio would
# drown out punctuation density purely because its numbers are bigger, which
# has nothing to do with either of them being useful.
#
# So each one gets two anchor points: the value where I call it fully machine
# like, and the value where I call it fully human. Anything between gets
# stretched onto 0 to 1 and then flipped, so that higher means more likely AI,
# the same direction as detector.model_signal.
#
# These anchors are not guesses. They come from running the five calibration
# texts in Milestone 4 and reading the table, which is written up in notes.md.
# They sit a little wider than the values I actually measured, so that text
# slightly outside my sample does not immediately peg at 0 or 1.

SPREAD_MACHINE_END, SPREAD_HUMAN_END = 0.15, 0.85
TTR_MACHINE_END, TTR_HUMAN_END = 0.60, 0.85
PUNCT_MACHINE_END, PUNCT_HUMAN_END = 0.02, 0.12

# How much each measure counts. These are weighted by how well each one
# actually separated my clearly AI text from my clearly human text:
#
#   spread           0.406 vs 0.890   a real gap
#   type token       0.792 vs 0.804   almost nothing
#   punctuation      0.038 vs 0.107   a real gap
#
# Type token ratio did not discriminate. I kept it rather than deleting it,
# because it is the only one of the three that notices repeated vocabulary and
# it may matter on text that is not in my sample, but it is down at 0.2 so it
# cannot drag a decision on its own. That is a finding, not a tuning knob, and
# it is written up in notes.md.
WEIGHT_SPREAD = 0.4
WEIGHT_TTR = 0.2
WEIGHT_PUNCT = 0.4


def _to_ai_score(value: float, machine_end: float, human_end: float) -> float:
    """
    Put one raw measure on a 0 to 1 scale where **higher means more likely AI**.

    All three of my measures read higher for more human writing, so this flips
    them at the end. Values past either anchor get clamped rather than running
    off the scale.
    """
    humanness = (value - machine_end) / (human_end - machine_end)
    humanness = min(max(humanness, 0.0), 1.0)
    return 1.0 - humanness


def style_signal(text: str) -> float:
    """
    The style signal as a 0 to 1 score. **Higher means more likely AI.**

    Same direction as `detector.model_signal`, so `scoring.combine_signals` can
    treat the two the same way. Getting that direction wrong would be the kind
    of mistake that makes everything above it quietly wrong.

    What this does: take each of my three measures, stretch it onto 0 to 1
    using the anchors above, flip it so higher means machine like, then take a
    weighted average using the weights above.

    What it scored on my five calibration texts:

        clearly AI             0.628
        clearly human          0.089
        plain human writing    0.942
        formal human writing   0.386
        lightly edited AI      0.492

    Read row three before trusting this signal. Plain, ordinary human writing
    scores higher here than text I know a machine wrote. Short even sentences
    and no optional punctuation is exactly what this measures, and plenty of
    real people write that way. That is the blind spot from Milestone 1,
    measured.

    Row five is the other half of the problem. Adding typos and chopping
    sentences up moved AI text from 0.628 down to 0.492, and it took about a
    minute to do.
    """
    spread = _to_ai_score(
        sentence_length_spread(text), SPREAD_MACHINE_END, SPREAD_HUMAN_END
    )
    ttr = _to_ai_score(
        type_token_ratio(text), TTR_MACHINE_END, TTR_HUMAN_END
    )
    punct = _to_ai_score(
        punctuation_density(text), PUNCT_MACHINE_END, PUNCT_HUMAN_END
    )

    score = (
        WEIGHT_SPREAD * spread
        + WEIGHT_TTR * ttr
        + WEIGHT_PUNCT * punct
    )
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
