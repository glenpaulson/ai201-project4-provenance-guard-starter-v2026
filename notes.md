# Milestone 1 notes: thinking it through before building

Written before any code. This is the plan I am going to build against.

---

## 1. The path a submission takes

A writer finishes a post on the site and hits publish. Here is everything that
happens between that and the sentence they end up reading.

1. **The site sends it to me.** It makes a POST to `/submit` on my service with
   a JSON body holding the writing (`text`) and who submitted it
   (`creator_id`).

2. **My handler unpacks it.** `app.py::submit` pulls those two fields out of
   the JSON and makes up a brand new id for this piece, the `content_id`. That
   id is the only handle anyone has on this decision later, so it gets made
   first and it goes in the answer.

3. **Signal one reads it.** The text goes to `detector.py::model_signal`. That
   runs a small language model on my own laptop and hands back one number
   between 0 and 1. Higher means "more likely written by a machine".

4. **Signal two measures it.** The same text goes to
   `stylometry.py::style_signal`. That one never reads the meaning. It only
   measures the shape. It hands back a number on the same 0 to 1 scale,
   pointing the same direction.

5. **The two numbers become one.** Both go into
   `scoring.py::combine_signals`, which mixes them into a single score. This is
   the step where I actually decide how willing I am to accuse someone.

6. **The score becomes words.** That one number goes into
   `scoring.py::score_to_label`, which picks one of three labels and gives back
   the exact sentence a person will read. A score of 0.62 means nothing to a
   writer. The sentence is the part that does.

7. **It gets written down.** Before anything goes back out,
   `audit.py::log_decision` appends one line to `logs/audit.jsonl` with the
   time, the content id, the creator, both signal numbers, the combined number,
   the label, and a status of `decided`.

8. **The service answers.** `/submit` returns JSON with the content id, the
   guess, the confidence, the label sentence, and both signal scores. The site
   shows the writer the sentence.

And if they disagree:

9. **The appeal.** The writer sends the `content_id` and their reasoning to
   `/appeal`. I check the id actually exists in the log, then
   `audit.py::log_appeal` writes a second line that moves the status to
   `under_review`. Nothing gets scored again automatically. The original decision
   stays in the log exactly where it was, and the appeal sits after it, so
   anyone reading later sees what was decided, that it was challenged, and in
   what order.

---

## 2. My two signals

### Signal one: the model signal (`detector.py`)

**What it measures:** how easy the writing is to guess. A small language model
(gpt2) goes through the text word by word and I look at how surprised it was.
Not surprised means the words were the obvious ones. That gets turned into a
number from 0 to 1, where higher means more like a machine wrote it.

**Why that might tell human and machine writing apart:** a language model
writes by picking a likely next word, over and over. So text a model produced
tends to be text a model finds easy to guess. People wander more. An odd word,
an abrupt turn, the specific thing instead of the usual thing.

**What it can't see:** it cannot see who wrote anything. All it really measures
is whether the words are ordinary ones in ordinary sentences, and plenty of
real people write exactly like that. Someone writing in a second language and
sticking to vocabulary they are sure of. A younger writer. Anyone writing
plainly on purpose. All three look like a machine to this signal.

It goes wrong the other way too. A dense paragraph stuffed with rare words
scores as *human* here, because rare words are exactly what the model fails to
guess. So being fancy gets you off and being plain gets you accused. The people
this signal is most likely to accuse are the ones with the least room to argue
back, and that is not a bug I can patch out of it.

### Signal two: the style signal (`stylometry.py`)

**What it measures:** the shape of the text, not the meaning. Three things:
whether sentence lengths vary or all march along at the same size, how much of
the vocabulary is repeated words, and how much punctuation there is.

**Why that might tell human and machine writing apart:** generated prose tends
to come out even. Sentences of about the same size, one after another, drawing
from a narrower band of words, because that is what "most likely next word"
produces on average. Human writing is lumpier. A three word sentence can sit
next to a forty word one.

**What it can't see:** it cannot read. It has no idea what the text says. That
means anything which changes the shape without changing the substance moves it:
adding typos, chopping a long sentence into three short ones, pasting in a
quotation. All of that is very cheap to do on purpose, and none of it changes
who actually wrote the piece.

---

## 3. Following a false positive through

**Maya** writes a short how to post about fixing a bike chain. English is her
second language, so she keeps sentences short and sticks to words she is sure
of. Every word is hers.

- **Signal one** sees plain, ordinary words in short, ordinary sentences and
  scores her around **0.78**, which reads as machine writing.
- **Signal two** sees sentences that are all about the same length and a small
  set of repeated words, and scores her around **0.70**, which reads the same
  way.
- **The combining rule**, if it is a straight average, gives **0.74**.
- **The label mapping** sees 0.74, which is over my AI threshold, and returns
  the high confidence AI label.

**What she reads:** a sentence telling her the site thinks a machine wrote her
post.

**What she can do about it:** send an appeal. That is the whole list. The appeal
records her reasoning, moves her item to `under_review`, and waits for a human.
It does not score the text again, so nothing she can type will change the number.

**What this tells me, and it is the important bit:** both of my signals got Maya
wrong *in the same direction, for the same reason*. Plain writing looks ordinary
to signal one and looks even to signal two. They are supposed to be two
different opinions, but on this exact person they agree. And because they agree,
averaging them does not cancel the mistake out, it makes the system *confident*
about the mistake. Two signals is not the same thing as two independent signals.

So my unsure band needs to be wide, and my combining rule needs to care about
which direction it would rather be wrong in. That is the decision I am going to
write criteria for in Milestone 2 and code in Milestone 4.

---

## 4. The shape of my two endpoints

This is the contract. Someone else should be able to build the website side
against this without asking me a single question.

### `POST /submit`

**Goes in:**

| Field | Type | Required | What it is |
|---|---|---|---|
| `text` | string | yes | the writing being checked |
| `creator_id` | string | yes | who submitted it |

**Comes back (200):**

| Field | Type | What it is |
|---|---|---|
| `content_id` | string | new id for this decision. Needed to appeal |
| `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| `confidence` | number | the combined score, 0.0 to 1.0 |
| `label` | string | the full sentence a person reads |
| `model_score` | number | signal one, 0.0 to 1.0 |
| `style_score` | number | signal two, 0.0 to 1.0 |

Both signal scores go in the response and not only in the log, because next
unit's tools read them straight off this answer.

**When it goes wrong (400):** `text` missing, empty, or only whitespace. Comes
back with `error` and `message`, and no `content_id`, because no decision was
made. The refusal still gets written to the log, so a pile of bad requests is
not invisible.

### `POST /appeal`

**Goes in:**

| Field | Type | Required | What it is |
|---|---|---|---|
| `content_id` | string | yes | the id from the `/submit` answer |
| `reasoning` | string | yes | the writer saying why this is wrong |

**Comes back (200):**

| Field | Type | What it is |
|---|---|---|
| `content_id` | string | echoed back |
| `status` | string | always `"under_review"` |
| `message` | string | confirmation the writer can read |
| `recorded_at` | string | when the appeal was written down |

**When it goes wrong (404):** the `content_id` is not in the log. Comes back
with `error` and `message`. A typo here would otherwise fail silently and look
like a broken endpoint.

---

# Milestone 3 notes: signal one on its own

Before wiring anything into the route I ran `detector.py` on three pieces of
text by hand, so I would know what the signal does before I could blame the
route for it.

| What I sent | perplexity | model_signal |
|---|---|---|
| Something I am sure is AI generated | 14.9 | **0.8539** |
| Something I am sure is human, written with a real voice | 44.0 | **0.5088** |
| Plain, ordinary human writing (the Maya case from Milestone 1) | 23.5 | **0.7383** |

**What this tells me, and I did not expect it to be this clean.**

In Milestone 1 I guessed plain human writing would score about 0.78 on this
signal. It scored 0.7383. My AI threshold is 0.65, so signal one on its own
already calls that writer a machine. The blind spot I wrote down on paper is
not a theory. It is sitting in my own test output on the first day.

The second row is the one that worries me more. Writing with an actual voice in
it, which is as human as anything I have, only reaches 0.5088. That is not
"this is a person". That is "I have no idea". So on this signal the gap between
obviously human writing and obviously machine writing is only about 0.35, and
plain human writing sits on the wrong side of it.

Signal one cannot carry this on its own, which is the whole reason there is a
Milestone 4.
