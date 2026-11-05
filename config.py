"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

You'll edit the thresholds in Milestone 5 and the rate limits in unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────
# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how *predictable* your text is to a language model. Text a
# model finds easy to predict tends to be text a model wrote.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words, which is enough for the signal to mean something.
DETECTOR_MAX_TOKENS = 400

# The longest submission /submit will accept, in characters. Anything bigger
# gets a 400 instead of being scored.
#
# My criterion 5 says a huge submission has to be refused in under 10 seconds.
# This is how. Since DETECTOR_MAX_TOKENS above means I only ever read the first
# 400 tokens anyway, accepting a giant body buys me no extra accuracy at all.
# It just hands anybody a free way to make my service slow for everyone else.
# 20,000 characters is roughly 3,000 words, far more than any blog post needs.
MAX_TEXT_CHARS = 20_000

# The shortest submission worth scoring. The model needs at least a few tokens
# before "how surprised was it" means anything, and detector.perplexity raises
# on anything under 3 tokens. Catching it here gives the writer a clear message
# instead of a crash.
MIN_TEXT_CHARS = 40


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────
# How much each signal counts toward the combined score.
#
# ⚠️ These are placeholders. Milestone 4 asks you to write your combining rule
# down BEFORE you code it, and to put the numbers in your README. Whatever you
# decide, it goes here.

WEIGHT_MODEL_SIGNAL = 0.5
WEIGHT_STYLE_SIGNAL = 0.5

# I left these equal, and that is a decision rather than me not getting round
# to it. On my five calibration texts the style signal actually separated
# clearly AI from clearly human better than the model signal did (a gap of
# 0.54 against 0.35). I did not promote it for that, because it is also the
# signal I can break in about a minute with a keyboard: adding typos and
# chopping sentences up moved it by 0.14 on its own. Neither signal earned the
# right to outvote the other, so the work gets done by the rule below instead.

# ─── How much disagreement bends the result (Milestone 4) ────────────────────
# My combining rule is a weighted average that then slides toward whichever
# signal reads more human, by an amount that grows with how far apart the two
# signals are.
#
# The reasoning is the one from Milestone 1: on a writing site the two kinds of
# mistake do not cost the same. When my two signals cannot agree with each
# other, I would rather be wrong in the direction that does not accuse anybody.

# The gap between the two signals at which the lean is at its strongest. Half
# the whole scale. Two signals further apart than this are not disagreeing,
# they are measuring different things.
FULL_DISAGREEMENT = 0.5

# How far the result can slide toward the kinder signal when the two are fully
# apart. 0.0 would mean the disagreement rule does nothing and this is just a
# weighted average. 1.0 would mean a disagreement throws away the harsher
# signal completely, which is too much: one signal shouting "machine" is still
# evidence. 0.6 leans hard without ignoring it.
MAX_LEAN = 0.6


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
# Where one label becomes another. Scores run 0.0 (confidently human) to 1.0
# (confidently AI).
#
#   score < HUMAN_THRESHOLD          -> high-confidence human
#   between the two                  -> unsure
#   score > AI_THRESHOLD             -> high-confidence AI
#
# ⚠️ This is where your false-positive decision from Milestone 1 actually gets
# made. Widening the unsure band means fewer wrong accusations and more AI text
# getting through. There is no setting that avoids the trade — only settings
# that decide who pays for it.

HUMAN_THRESHOLD = 0.35
AI_THRESHOLD = 0.65

# ⚠️ One thing that catches people out in Milestone 5. A weighted average can
# only land between its two inputs — so while `style_signal` is still the stub
# returning 0.5, the combined score can never leave 0.25–0.75 no matter what
# the model signal says, and the human label needs a model score below 0.20 to
# be reachable at all.
#
# If a label you can't reach is the problem, the fix is upstream of the
# thresholds: a style signal that actually varies. `scoring.label_ranges()`
# prints the bands; the reachable range is a different question.


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────
# Off in unit 7. You turn it on and choose the numbers in unit 8, Milestone 1.
#
# Think about two people: a real writer submitting their own work a few times
# an hour, and a script sending a thousand variations to map your thresholds.
# Your README has to say why your numbers and not others.

# On by default now. The env var still turns it off if I need a run without it,
# which I do when I want to tell a rate limit rejection apart from a real
# refusal in the attack set.
RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "1") == "1"

# My numbers, and the reasoning is in the README under Rate Limiting.
#
# The short version. A real writer submitting their own post needs two or three
# goes in a row at the very most: submit it, notice a typo, submit again. Five
# covers that with room for a double click and a retry.
#
# The daily number is the one that actually defends anything, and that is
# because of something specific to my service: /submit hands back model_score
# and style_score, not just the label. Every request tells the caller where my
# two signals sit, so a script mapping my thresholds learns a lot per request
# and does not need to hurry. One request every fifteen seconds never touches a
# per minute limit and still gets 240 readings in an hour. Sixty a day is far
# more than any real writer needs and it caps what a patient script can learn
# before someone notices it.
RATE_LIMIT_PER_MINUTE = 5
RATE_LIMIT_PER_DAY = 60

# Flask-Limiter warns loudly without this. In-memory is right for one laptop
# and wrong for anything real — a restart forgets every count, and two copies
# of the service wouldn't share limits.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
