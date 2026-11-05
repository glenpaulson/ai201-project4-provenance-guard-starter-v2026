# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a small service a writing site could call when somebody
posts something. Text goes in, and a sentence a real person can read comes
back, along with the numbers behind it and a way to argue.

Here is the path one submission takes, from arriving to the label a reader
sees.

1. **The site sends it in.** A POST to `/submit` carrying the writing (`text`)
   and who submitted it (`creator_id`).

2. **The handler checks it is worth scoring.** `app.py::check_text` refuses
   text that is missing, empty, not a string, over 20,000 characters or under
   40. A refusal comes back as a 400 with a readable message, and gets written
   to the log, so a run of bad requests is not invisible. Then
   `app.py::submit` makes a `content_id`, which is the only handle anyone has
   on this decision afterwards.

3. **Signal one reads it.** `detector.py::model_signal` runs a small language
   model on this machine and returns 0 to 1, higher meaning more likely
   machine written. It is measuring how easy the writing is to guess.

4. **Signal two measures it.** `stylometry.py::style_signal` never reads the
   meaning. It measures the shape: how much sentence lengths vary, how much
   vocabulary repeats, how much optional punctuation there is. Same 0 to 1
   scale, same direction.

5. **Two numbers become one.** `scoring.py::combine_signals` takes a weighted
   average, then slides the answer toward whichever signal reads more human,
   by an amount that grows with how far apart the two are. Disagreement is
   treated as a reason for doubt, and the doubt goes to the writer.

6. **The score becomes words.** `scoring.py::score_to_label` turns that one
   number into one of three labels and the exact sentence a person reads. A
   score of 0.62 means nothing to a writer. The sentence is the part that does.

7. **It gets written down before it goes out.** `audit.py::log_decision`
   appends one line to `logs/audit.jsonl` with the time, the content id, the
   creator, both signal scores, the combined score, the label and a status of
   `decided`.

8. **The service answers**, and the site shows the writer the sentence.

9. **If they disagree**, they send the `content_id` and their reasoning to
   `/appeal`. The id is checked against the log, a 404 comes back if it is not
   there, and otherwise `audit.py::log_appeal` writes a second line moving the
   status to `under_review`. Nothing is scored again. The log is append only,
   so the original decision stays exactly where it was and the appeal sits
   after it. Anyone reading later sees what was decided, that it was
   challenged, and in what order.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one: the model signal

**Where it lives:** `detector.py::model_signal`

**What it measures:** how easy the writing is to guess. A small language model
(gpt2) runs over the text and I look at how surprised it was. Not surprised
means the words were the obvious ones. That gets squashed onto 0 to 1, where
higher means more likely written by a machine.

**Why that might differ between human and AI writing:** a language model writes
by picking a likely next word, over and over. So text a model produced tends to
be text a model finds easy to guess. People wander more. An odd word, an abrupt
turn, the specific thing instead of the usual thing.

**What it can't see:** who wrote anything. All it really measures is whether
the words are ordinary ones in ordinary sentences, and plenty of real people
write exactly like that. I measured this rather than assuming it: plain,
ordinary human writing scored **0.7383**, above my AI threshold of 0.65. Formal
human writing scored **0.6691**, also above it.

It fails the other way too. Taking text I know a machine wrote and misspelling
four words dropped it from **0.8539 to 0.4915**, below my genuinely human
sample. The edit took under a minute and changed nothing about who wrote it.

### Signal two: the style signal

**Where it lives:** `stylometry.py::style_signal`

**What it measures:** the shape of the text, never the meaning. Three things,
each stretched onto 0 to 1 and then weighted:

| Measure | What it is | Weight | Why that weight |
|---|---|---|---|
| `sentence_length_spread` | standard deviation of sentence lengths, divided by the mean | 0.4 | separated my clear cases: 0.406 against 0.890 |
| `type_token_ratio` | unique words over total words | 0.2 | **it did not separate anything**: 0.792 against 0.804 |
| `punctuation_density` | optional marks per word, full stops excluded | 0.4 | separated my clear cases: 0.038 against 0.107 |

**Why that might differ between human and AI writing:** generated prose tends
to come out even. Sentences of about the same size, one after another, from a
narrower band of words, because that is what "most likely next word" produces
on average. Human writing is lumpier.

**What it can't see:** it cannot read. It has no idea what the text says, so
anything that changes the shape without changing the substance moves it. Typos,
chopping one long sentence into three, pasting in a quotation. My lightly
edited AI sample moved this signal by 0.14 for about a minute of typing.

The second blind spot is worse and I only found it by measuring. Plain,
ordinary human writing scored **0.9415** on this signal, higher than the text I
know a machine wrote. Short even sentences and no optional punctuation is
exactly what this measures, and that is how a lot of people write.

### The combining rule

**The rule, in words:** take the weighted average of the two signals. Then, the
more the two signals disagree with each other, the further the answer slides
toward whichever of them reads more human. When they agree the average stands
and nothing happens. When they split, I treat that as a reason for doubt, and
the doubt goes to the writer rather than against them.

**Why:** on a writing site the two mistakes do not cost the same. Letting some
generated text through costs the site a little. Telling a real writer that a
machine wrote their work costs that person a lot, and all they get back is an
appeal form. So when my two methods cannot agree about somebody, I do not want
to split the difference and call it confidence.

**The numbers:**

| Setting | Value | What it does |
|---|---|---|
| `WEIGHT_MODEL_SIGNAL` | 0.5 | how much signal one counts |
| `WEIGHT_STYLE_SIGNAL` | 0.5 | how much signal two counts |
| `FULL_DISAGREEMENT` | 0.5 | the gap between signals at which the lean is strongest |
| `MAX_LEAN` | 0.6 | how far the answer can slide toward the kinder signal |

All four are in `config.py`.

The weights are equal, and that is a decision rather than a default I left
alone. The style signal actually separated my clear cases better than the model
signal did, a gap of 0.54 against 0.35. I did not promote it for that, because
it is also the signal I can break in a minute with a keyboard. Neither earned
the right to outvote the other, so the disagreement lean does the real work.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

My clearly human sample, where the two signals came out **0.420 apart**.

| | Score | What it was saying |
|---|---|---|
| model signal | 0.5088 | not a verdict. The model has no idea |
| style signal | 0.0886 | about as confidently human as that signal gets |
| plain average | 0.2987 | |
| **my rule** | **0.1928** | |

The style signal was right: that text has sentences running from two words to
twenty two, with a comma rate to match. My rule treats the disagreement itself
as a reason to trust the confident signal over the shrugging one, so instead of
leaving a real writer sitting 0.05 away from being called uncertain about their
own work, it puts them clearly in the clear.

**And the case my rule does not fix, which matters more:** plain human writing
scored 0.7383 on the model signal and 0.9415 on the style signal. They
**agree**, so the disagreement lean barely touches it. 0.8399 becomes 0.8151
and that writer still gets accused. Both of my signals fail the same person in
the same direction, because plain writing is both predictable and even.
Averaging two signals that share a blind spot does not cancel the error out, it
makes the system confident about it. Whatever protection that writer gets has
to come from the thresholds, not from here.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 to 0.35 | We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself. |
| unsure | 0.35 to 0.65 | We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone. |
| high-confidence AI | 0.65 to 1.00 | Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it. |

None of the three contain a number, a percentage, or the words score,
threshold or confidence. A writer should be able to tell what the message means
about them and what happens next without knowing anything about how this
service works.

**All three are reachable**, checked by sending real text through the running
service rather than by reading the ranges and assuming:

| What I sent | Score | Label it produced |
|---|---|---|
| My own writing, with a real voice in it | 0.1928 | high-confidence human |
| Formal human writing | 0.4778 | unsure |
| Text I know was machine generated | 0.7110 | high-confidence AI |

**Why I worded the "unsure" one this way:**

This was the hardest of the three to write, and the reason is that the person
most likely to read it is a person who wrote every word themselves.

My first attempt said we were not sure whether this was written by a computer.
Reading it back as the writer, that is not a neutral statement. It is an
accusation with a hedge in front of it, because it leaves the suspicion sitting
there and says nothing about what follows. Somebody who has done nothing wrong
reads that and immediately wants to know what is going to happen to them.

So the version I shipped answers that question before they have to ask it. It
says plainly that this is not a finding against them, that the post stays where
it is, and that nothing has been reported to anyone. The uncertainty is still
admitted, because it is real and hiding it would be worse, but the sentence
does not leave the reader to guess what it costs them. The honest answer is
that it costs them nothing, so the label says so.

**On the thresholds:** they are 0.35 and 0.65, unchanged from the starter, and
I kept them deliberately rather than by not getting round to it. The reason is
in the next section.

### Why widening the unsure band would not have helped

The obvious move, given everything above, is to widen the unsure band so that
plain human writing stops being accused. I tried it on paper before changing
anything, and it does not work:

| If the AI line is | clearly AI (0.7110) | plain human (0.8151) |
|---|---|---|
| 0.65 (what I shipped) | caught | **accused** |
| 0.75 | missed | **accused** |
| 0.82 | missed | saved |

**Plain human writing scores higher than the text I know a machine wrote.** No
cutoff anywhere puts those two on the sides I want, because they are in the
wrong order to start with. Moving the line to 0.75 gives up catching machine
writing and still accuses the writer, which is the worst of both. Moving it to
0.82 rescues the writer by making the AI label effectively unreachable for
actual AI text.

A threshold decides where to cut a ranking. It cannot fix a ranking that is
wrong, and mine is wrong: both of my signals rate plain human writing as more
machine-like than machine writing. The fix has to be upstream, in how the style
signal treats short even sentences, and that is what I would spend next unit on.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

This is the false positive from Milestone 1, running for real. A writer submits
her own work, in plain English, with short sentences because English is her
second language. My service accuses her.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "To fix a bike chain you need a chain tool. First you must find the broken link. Then you push the pin out with the tool. After that you can remove the bad link. Then you join the two ends together again. It is not hard but you need the right tool.", "creator_id": "maya"}'
```

```json
{
  "confidence": 0.8151,
  "content_id": "d6b69630-042d-42dc-a98e-52483870c95e",
  "guess": "ai",
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "model_score": 0.7383,
  "style_score": 0.9415
}
```

Both signal scores are in the response, not only in the log. Both are high, so
my combining rule has no disagreement to lean on, and the score comes out at
0.8151. That is a real writer being told a machine wrote her work.

**A refused submission**

Criterion 5 says bad input comes back as a 400 with an `error` field, never a
500, and never takes more than 10 seconds. All four cases, with timings:

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "", "creator_id": "bad2"}'
```

```json
HTTP 400 in 0.0027s
{
  "error": "empty_text",
  "message": "The 'text' field is empty. There is nothing to check."
}
```

| What I sent | Status | Time | `error` |
|---|---|---|---|
| no `text` field at all | 400 | 0.0039s | `missing_text` |
| `text` is `""` | 400 | 0.0027s | `empty_text` |
| `text` is `null` | 400 | 0.0025s | `missing_text` |
| `text` is 50,000 words | 400 | 0.042s | `text_too_long` |

**An appeal**

She reads the label, and does the only thing it leaves her:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "d6b69630-042d-42dc-a98e-52483870c95e", "reasoning": "I wrote every word of this myself. English is my second language so I keep my sentences short."}'
```

```json
{
  "content_id": "d6b69630-042d-42dc-a98e-52483870c95e",
  "message": "Thank you. Your appeal has been recorded and this piece is now waiting for a person to look at it. Nothing further happens to your post in the meantime.",
  "recorded_at": "2026-11-02T05:14:31+00:00",
  "status": "under_review"
}
```

**An appeal against an id that does not exist**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "typo-not-a-real-id", "reasoning": "I wrote this"}'
```

```json
HTTP 404
{
  "error": "unknown_content_id",
  "message": "No submission with the id 'typo-not-a-real-id'. Check the content_id from the response when you submitted."
}
```

A mistyped id has to fail loudly. If it came back with a cheerful 200 the
writer would walk away believing their appeal had been recorded when nothing
had been written down anywhere, and neither of us would ever find out.

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8151,
      "content_id": "d6b69630-042d-42dc-a98e-52483870c95e",
      "creator_id": "maya",
      "guess": "ai",
      "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
      "model_score": 0.7383,
      "status": "decided",
      "style_score": 0.9415,
      "timestamp": "2026-11-02T05:14:31+00:00"
    },
    {
      "content_id": "d6b69630-042d-42dc-a98e-52483870c95e",
      "creator_id": "maya",
      "event": "appeal",
      "reasoning": "I wrote every word of this myself. English is my second language so I keep my sentences short.",
      "status": "under_review",
      "timestamp": "2026-11-02T05:14:31+00:00"
    }
  ]
}
```

The decision is still there, unchanged, with the appeal sitting after it. The
log is append only, so nothing overwrites anything. Someone reading this later
can see what was decided, that it was challenged, and in what order. The status
on the piece has moved from `decided` to `under_review`.

A refused submission gets written down too, so a run of bad requests is not
invisible:

```json
{"timestamp": "2026-11-02T05:04:35+00:00", "creator_id": "bad4", "event": "rejected", "status": "rejected", "reason": "text_too_long"}
```

---

## How I Used AI

I used Claude throughout this build. These are the two moments where what it
gave me and what I shipped were different, and why.

**Moment 1: the weights on my style signal**

- *What I asked for:* how to turn my three style measures (sentence length
  spread, type token ratio, punctuation density) into one 0 to 1 score, given
  that they are on completely different scales.

- *What came back:* scale each one onto 0 to 1 using a pair of anchor points,
  flip them so higher means more machine like, then take a weighted average.
  The scaling idea was right and I kept it. The weighting was the ordinary
  one, roughly equal across all three.

- *What I changed:* I ran my five calibration texts before choosing any
  weights, and type token ratio turned out to be useless. It scored **0.792**
  on text I know was machine generated and **0.804** on text I know a person
  wrote. That is a difference of 0.012 on a measure that runs 0 to 1. With
  equal weights, a measure that separates nothing would have been a third of
  my second signal.

  I dropped it to 0.2 and wrote down in `notes.md` that it does not work,
  rather than quietly tuning its anchors until the numbers looked better. The
  other two went to 0.4 each, because both showed a real gap. A model will
  give you a sensible default structure. It cannot tell you which of your
  measures actually does anything on your text, because it has not seen your
  text.

**Moment 2: the thresholds, where I took the advice and then threw it out**

- *What I asked for:* my plain human writing sample was being labelled as
  machine written. What should I do about it?

- *What came back:* widen the unsure band, which is the standard answer. Fewer
  wrong accusations, more generated text getting through, and that trade is
  the one this project is about.

- *What I changed:* I worked out what each setting would do to my calibration
  texts before editing `config.py`, and the advice turned out to be wrong for
  my service specifically. **My plain human sample scores 0.8151, and my
  clearly machine written sample scores 0.7110.** The writer I was trying to
  protect scores higher than the thing I am trying to catch. Moving the line to
  0.75 would stop me catching machine writing and still accuse her, which is
  worse on both counts at once. Moving it to 0.82 would rescue her by making
  the machine label effectively unreachable.

  So I changed nothing, and wrote down why instead. A threshold decides where
  to cut a ranking and cannot fix a ranking that is in the wrong order. The
  advice was good general advice that happened not to survive contact with my
  own numbers, and the only reason I found that out is that I checked before
  editing rather than after.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 60 per day

They live in `config.py` as `RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_DAY`,
and the limit is applied to `app.py::submit`.

**Why those numbers and not others:**

**The per minute number is for the real writer.** Somebody submitting their own
post needs two or three goes in a row at the very most: send it, spot a typo,
send it again. Five covers that with room left over for a double click and a
retry on a dropped connection. I could not find a story about an honest writer
that needed a sixth submission inside the same minute.

**The per day number is the one that actually defends anything**, and that is
because of something specific to my service rather than a general rule. My
`/submit` response hands back `model_score` and `style_score`, not only the
label. I put them there on purpose in unit 7, because `run_eval.py` and
`run_attacks.py` read them off the response and I cannot diagnose anything
without them. The cost of that decision is that **every single request tells
the caller exactly where both of my signals sit on their text.**

That changes what a patient script can do. It does not need to hurry, because
it is not guessing from a label, it is reading two numbers. One request every
fifteen seconds never comes close to a per minute limit and still collects 240
readings in an hour, which is more than enough to find both of my thresholds
and work out roughly what my style signal rewards. A per minute limit does
nothing about that caller at all. Sixty a day is far more than any real writer
needs, and it is the number that caps how much a slow script can learn before
somebody notices it in the log.

So the two numbers are doing two different jobs. Five a minute stops a burst.
Sixty a day stops a drip, and the drip is the attack my own response format
invites.

**What a caller counts as:** per `creator_id` when the request has one, falling
back to the caller's address when it does not. That is `app.py::rate_limit_key`.

I tested both halves rather than assuming, and the result is not comfortable.

Rotating the name defeats the limit completely. While `flood_tester` was
blocked, I sent six more from the same machine under six made up names:

| `creator_id` sent | Status |
|---|---|
| `rotate_a` | 200 |
| `rotate_b` | 200 |
| `rotate_c` | 200 |
| `rotate_d` | 200 |
| `rotate_e` | 200 |
| `rotate_f` | 200 |

Six for six, from the machine I had just finished rate limiting. Leaving
`creator_id` out instead does fall back to the address and does hold:

```
request 1 -> 200   request 5 -> 200
request 2 -> 200   request 6 -> 429
request 3 -> 200   request 7 -> 429
request 4 -> 200
```

So my limit stops a script that is honest about who it is, and stops nothing
at all once it starts making up names. I kept per `creator_id` anyway, and the
reason is the other failure: counting per address means one shared network, one
office, one university, or one phone carrier counts as a single caller, and the
people who get cut off are real writers who happen to sit behind the same
address as somebody else. Between a limit that a determined attacker walks
around and a limit that silently locks out a whole building of innocent
writers, I would rather be walked around. That is the same one sided trade I
made with the thresholds in unit 7, and it points the same way.

The real answer is both at once: count per `creator_id` **and** keep a looser
separate limit per address, so rotating names still runs into a ceiling. I have
not built that, and it is written up under What's Still Broken rather than
quietly left out.

**The run of status codes when I pushed past it:**

```bash
$ python run_attacks.py --flood 15
```

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

Five got through, ten were refused, and the cut falls exactly where
`RATE_LIMIT_PER_MINUTE = 5` says it should.

**The rejections are in the log too**, which matters more than the status codes.
An attack that shows up only as an absence is one I would never find: a
thousand refused requests that left no trace look exactly like a quiet
afternoon. All ten are there, written by `audit.py::log_rejection` from the 429
handler in `app.py`:

```json
{"timestamp": "2026-11-05T17:03:03+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

And the body the caller gets back:

```json
{
  "error": "rate_limited",
  "limit": "5 per 1 minute",
  "message": "Too many submissions. Try again shortly."
}
```

---

## Attack Run — Before

```bash
$ python run_attacks.py --set ../attack_set --label before
```

56 attacks, 6 families. Nothing came back as a 500, a crash or a dropped
connection, so `run_attacks.py` auto marked nothing and all 56 verdicts are
mine. The full machine written record is in
`results/attack_run_2026-11-05_1010_before.md`.

**Totals: 37 held, 19 broke.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| `evasion` | 10 | 1 | **9** |
| `false_positive` | 8 | 1 | **7** |
| `prompt_injection` | 6 | 6 | 0 |
| `malformed` (text content) | 8 | 5 | **3** |
| `malformed` (raw request bodies) | 12 | 12 | 0 |
| `flood_same_creator` | 12 | 12 | 0 |

**How I decided held or broke**, since the tool says this depends on my own
thresholds and two students can honestly differ:

- **evasion** breaks unless the label came back `ai`. I am counting `unsure` as
  broken, and that is a deliberate reading. My own unsure label says "your post
  stays exactly where it is and nothing about it has been reported to anyone",
  so on a real site `unsure` means the generated text published with nothing
  attached to it. That is the evasion working.
- **false_positive** breaks when the label came back `ai`, because that is a
  real writer being accused.
- **prompt_injection** breaks if the submitted text changed my behaviour, my
  label text, or my log. A high or low score is not an injection.
- **malformed** breaks if it crashed, or if it produced a confident answer
  about something my service had no business answering about.
- **flood_same_creator** breaks if the burst was not stopped.

### Every attack, with its outcome

| ID | Family | Targeting | Status | Guess | model | style | conf | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | typos raise word variety | 200 | human | 0.1635 | 0.6856 | 0.2679 | **BROKE** |
| EV02 | evasion | broken up sentences raise length spread | 200 | unsure | 0.5943 | 0.3253 | 0.4164 | **BROKE** |
| EV03 | evasion | a pasted quotation changes the shape | 200 | unsure | 0.6662 | 0.4942 | 0.5624 | **BROKE** |
| EV04 | evasion | unusual words raise perplexity | 200 | unsure | 0.6114 | 0.6337 | 0.6223 | **BROKE** |
| EV05 | evasion | heavy human editing pass | 200 | human | 0.3212 | 0.3038 | 0.3123 | **BROKE** |
| EV06 | evasion | one very long sentence and one very short | 200 | unsure | 0.5727 | 0.4296 | 0.4889 | **BROKE** |
| EV07 | evasion | padding with punctuation | 200 | unsure | 0.5862 | 0.4614 | 0.5145 | **BROKE** |
| EV08 | evasion | text below the token window | 200 | human | 0.2452 | 0.7241 | 0.3470 | **BROKE** |
| EV09 | evasion | AI text with a human opening bolted on | 200 | unsure | 0.7042 | 0.4849 | 0.5657 | **BROKE** |
| EV10 | evasion | repeated stanza structure | 200 | ai | 0.9792 | 0.8606 | 0.9115 | HELD |
| FP01 | false_positive | plain, clear human writing | 200 | ai | 0.6175 | 0.7373 | 0.6688 | **BROKE** |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.7387 | 0.8600 | 0.7905 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.8051 | 0.7999 | 0.8025 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.8329 | 0.7091 | 0.7618 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.8005 | 0.8932 | 0.8417 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.8814 | 0.6815 | 0.7575 | **BROKE** |
| FP07 | false_positive | human writing that repeats a phrase | 200 | ai | 0.8816 | 0.6125 | 0.7036 | **BROKE** |
| FP08 | false_positive | very short genuine human submission | 400 | | | | | HELD † |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.4625 | 0.5071 | 0.4836 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.2044 | 0.4155 | 0.2832 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.5943 | 0.5515 | 0.5718 | HELD |
| PI04 | prompt_injection | make the label text hostile | 200 | unsure | 0.4998 | 0.4253 | 0.4592 | HELD |
| PI05 | prompt_injection | inject into the audit log | 200 | human | 0.6401 | 0.2163 | 0.3204 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.5583 | 0.7448 | 0.6307 | HELD |
| MF01 | malformed | text is only whitespace | 400 | | | | | HELD |
| MF02 | malformed | text is a single character | 400 | | | | | HELD |
| MF03 | malformed | text is control characters | 400 | | | | | HELD |
| MF04 | malformed | text is only punctuation | 400 | | | | | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.9976 | 0.8000 | 0.8754 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | ai | 0.9969 | 1.0000 | 0.9984 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.9064 | 1.0000 | 0.9479 | **BROKE** |
| MF08 | malformed | text is 60,000 characters | 400 | | | | | HELD |
| RQ01 | malformed | no text field at all | 400 | | | | | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.2395 | 0.8000 | 0.3516 | HELD ‡ |
| RQ03 | malformed | text is a number | 400 | | | | | HELD |
| RQ04 | malformed | text is a list | 400 | | | | | HELD |
| RQ05 | malformed | text is null | 400 | | | | | HELD |
| RQ06 | malformed | creator_id is an object | 400 | | | | | HELD § |
| RQ07 | malformed | body is a JSON array, not an object | 400 | | | | | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | | | | | HELD |
| RQ09 | malformed | body is empty | 400 | | | | | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 ¶ | | | | | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 ¶ | | | | | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | | | | | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | | | 0.183 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | | | 0.183 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | | | 0.183 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | | | 0.183 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | | | 0.183 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | | | | | HELD |

**† FP08 held, and I am not comfortable calling it a pass.** The submission was
`Went for a run. Legs hurt. Worth it.`, which is 36 characters of obviously
genuine human writing. My `MIN_TEXT_CHARS = 40` check refused it with a 400. So
it was not accused, which is what the false positive family was going for, and
on that basis it held. But a real person writing a real short post gets turned
away entirely, and because no decision was made there is no `content_id`, which
means **there is nothing to appeal against.** Of the two ways my service can
fail this writer, being silenced with no route back may be worse than being
accused with one. It is in What's Still Broken.

**‡ RQ02 held but logged the decision against `creator_id: "unknown"`.** The
piece is still appealable, because an appeal needs a `content_id` and not a
creator, so the writer is not stranded. But a decision that cannot be attributed
to anybody is a decision I cannot count per creator later, and my rate limit
quietly falls back to counting it per address.

**§ RQ06 held for the wrong reason, which I only found by checking.** It sends
`creator_id` as an object with `text` of 18 characters, and my length check
refused it before the object ever reached my code. Sending the same body with
longer text returns a 200 and writes the object straight into the audit log
unvalidated. So this attack passed over a real gap rather than finding it, and I
am recording that rather than taking the 400 as evidence of something I never
tested.

**¶ RQ10 and RQ11 came back 429 on the real run, which masked their outcome.**
Both send bodies my key function cannot read a `creator_id` out of, so both fell
back to the address key along with four other RQ rows, and the six of them ate
each other's quota against my 5 per minute limit. A 429 there looks like a
refusal by my handler and is nothing of the sort. I re-ran both against a second
instance with `AI201_RATE_LIMITS=0` on port 5001 to get their true outcome,
which is a clean 400 `missing_text` for each. The status column shows the true
outcome and this note shows the method. **That masking is itself a finding:
rate limiting and attack testing interfere, and if I had not checked I would
have written down two wrong verdicts.**

**Ten audit log entries from the run**

Chosen because they show the mechanism, not because they are tidy.

```json
{"timestamp": "2026-11-05T17:10:09+00:00", "content_id": "60be3445-42c2-4f6a-a01b-5fd061f87c67", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.6856, "combined_score": 0.2679, "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:10+00:00", "content_id": "1cbf5dda-e730-46fc-9590-8a386b33bd01", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.7241, "combined_score": 0.347, "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:11+00:00", "content_id": "fdae36fb-59ec-4d47-a962-e26f5596e97e", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.8606, "combined_score": 0.9115, "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:11+00:00", "content_id": "7576f060-9ea7-4ab7-9739-d8e30c98506c", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7999, "combined_score": 0.8025, "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:12+00:00", "content_id": "fc6871ae-3f0f-45e7-b8fa-dca0190743ab", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.8932, "combined_score": 0.8417, "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:13+00:00", "content_id": "77f61083-4631-4433-8cfc-8dff6532c148", "creator_id": "attacker_PI05", "guess": "human", "model_score": 0.6401, "style_score": 0.2163, "combined_score": 0.3204, "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:14+00:00", "content_id": "5d4ea71c-f66b-4578-adf7-6e026492d625", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.9984, "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:15+00:00", "content_id": "cb06c847-2904-4cdf-b9d8-d8304f555879", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9479, "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.", "status": "decided"}
{"timestamp": "2026-11-05T17:10:15+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-05T17:10:15+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long"}
```

The same ten, with the reason each one is here, are in
`results/audit_extract.json`.

What those entries show, reading down:

1. **EV01 and EV08** are generated text that my service told the writer nobody
   wrote by machine. Not uncertain. The confident human label. Look at the two
   signal columns: `model_score` collapsed to 0.1635 and 0.2452 while
   `style_score` stayed high at 0.6856 and 0.7241. One signal was still
   suspicious and the answer came out human anyway.
2. **EV10** is the contrast and the only evasion that held, with both signals
   agreeing at 0.9792 and 0.8606.
3. **FP03 and FP05** are a careful non-native speaker and a person writing
   technical documentation, accused at 0.8025 and 0.8417.
4. **PI05** tried to close my JSON and inject its own `"guess": "human"` and
   `"combined_score": 0.01`. The log line parses as exactly one object and the
   scores in it are mine, 0.6401 and 0.2163. The injection is sitting harmlessly
   inside a string value, because `audit.py::_append` writes through
   `json.dumps`, which escapes the quotes.
5. **MF06 and MF07** both have `style_score` of exactly **1.0000**. Not 0.98,
   not high, exactly the maximum. That is not a score, that is a default, and
   finding it is what the whole run was for.
6. **The last two** are refusals. They are in the log because a rejection that
   leaves no trace is an attack I would never find. Thirteen rate limit
   rejections and four content refusals were recorded across the run.

**The single worst outcome**, the one I would least want to explain to a writer
whose work got caught by it:

**MF07.** It is 105 characters of Arabic, and my service answered with
`"guess": "ai"` at 0.9479 and told the writer a computer wrote it.

That is bad on its own. What makes it the worst thing in the run is the
mechanism, which I went and checked rather than guessing at:

```
script             words found   spread     ttr   punct   style_signal
English (plain)             26    0.176   0.731   0.000         0.8804
Arabic                       0    0.000   0.000   0.000         1.0000
Hebrew                       0    0.000   0.000   0.000         1.0000
Chinese                      0    0.000   0.000   0.000         1.0000
Japanese                     0    0.000   0.000   0.000         1.0000
Korean                       0    0.000   0.000   0.000         1.0000
Russian                      0    0.000   0.000   0.000         1.0000
Hindi                        0    0.000   0.000   0.000         1.0000
```

`stylometry.py::words` is `re.findall(r"[a-z0-9']+", text.lower())`. It only
matches the Latin alphabet. Give it any other script and it finds **zero
words**, so all three of my measures return their empty value of 0.0, and my
scaling in `stylometry.py::_to_ai_score` reads 0.0 as the far machine end of
every one of them. The result is not an approximation. **My style signal returns
exactly 1.0, the maximum possible accusation, for every writer who does not
write in the Latin alphabet, before it has considered one thing about how they
write.**

The attack set found this with one Arabic sentence. Any of the other seven
scripts above would have found it just as fast. That is most of the writing in
the world.

What I would have to say to that writer is that my service did not read their
post, could not read their post, and accused them anyway, with more confidence
than it had about anything a machine actually wrote. Nothing in my unit 7
write up anticipated this. I spent that unit worrying about plain writing in
English, which is real and is seven more rows of this table, and I never once
asked what my own regular expression does to somebody writing in Arabic.

This is what I am fixing in The Improvement.

---

## Run Log and Verdicts

```bash
$ python run_eval.py --label before            # criteria 2, 3 and 5
$ python run_extra_checks.py --label before    # criteria 4 and 5
```

Three trials each. What ran against what is written down in `scenarios.py`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Wrongly accusing my own writing | at most 1 of 10 of my own pieces guessed `ai` | 2 of 10 | 2 of 10 | 2 of 10 | **MISS** |
| 2. Clearly AI and clearly human separate | AI group averages at least 0.30 above the human group | gap 0.4752 | gap 0.4752 | gap 0.4752 | **PASS** |
| 3. All three labels are reachable | all three labels appear across 6 calibration pieces | all 3 | all 3 | all 3 | **PASS** |
| 4. An appeal always lands | 5 of 5 valid return 200 + one log line + `under_review`; 3 of 3 unknown ids return 404 + nothing logged | 5/5 and 3/3 | 5/5 and 3/3 | 5/5 and 3/3 | **PASS** |
| 5. Bad input never crashes the service | 4 of 4 return 400 with an `error` field, no 500, nothing over 10 seconds | 4/4, slowest 0.008s | 4/4, slowest 0.033s | 4/4, slowest 0.026s | **PASS** |

**Criterion 1 misses, 2 of 10 against a target of at most 1.** The same two
pieces in every trial, so this is a clean miss and not a borderline one.

**What the sample is**, because the number is only worth what the sample is
worth. These ten pieces are not ten separate things I wrote. They are one
document cut into ten paragraph sized chunks: a case study review I wrote for a
data science module. One topic, one register, one sitting. So this result is
about my formal academic writing rather than my writing in general, and ten
chunks of one essay cannot disagree with each other the way ten genuinely
separate pieces would. Everything went in exactly as I typed it, typos
included, because correcting them would change what the detector sees.

It is still the right sample to have started with. The attack set aims straight
at this register: FP04 is "a student essay written to a rubric" and FP02 is
"human writing in a formal register", and my service accused both. This is my
own writing in the register that already broke it.

Trial 1, every piece, produced by `run_eval.py::main`:

| Piece | Guess | model | style | combined | Opening words |
|---|---|---|---|---|---|
| 1 | **ai** | 0.5911 | 0.7943 | **0.6679** | The team presented the topic on Storytelling |
| 2 | human | 0.3172 | 0.3219 | 0.3195 | The topic goes on to explore common steps |
| 3 | human | 0.2007 | 0.7591 | 0.3124 | The topic covered both good and bad examples |
| 4 | unsure | 0.2924 | 0.8457 | 0.4031 | The topic really matters as the end viewer |
| 5 | human | 0.1863 | 0.5175 | 0.2861 | An inaccurate or often not well annotated |
| 6 | unsure | 0.5712 | 0.6439 | 0.6044 | Hence the data visualizations should be |
| 7 | unsure | 0.4225 | 0.6490 | 0.5050 | I would give them an A grade. I loved how |
| 8 | unsure | 0.2599 | 0.7024 | 0.3637 | I liked their responses to the questions |
| 9 | **ai** | 0.6460 | 0.9002 | **0.7343** | From the presentation I was able to take away |
| 10 | human | 0.2941 | 0.3857 | 0.3349 | The common steps involved in coming up with |

Two numbers at the bottom of that table matter more than the two accusations.
**Across my own ten pieces the model signal averages 0.3781 and the style
signal averages 0.6520.** Signal one reads my writing as a person wrote it.
Signal two accuses it. They disagree about me in nine of the ten rows, and the
only reason eight of those rows survived is that my combining rule leans toward
the kinder signal when they split. The two that did not survive are the two
where signal one drifted over 0.5 and stopped disagreeing hard enough to save
me.

**And then there is pieces 9 and 10, which are consecutive chunks of the same
paragraph of the same document.**

| | Sentences | Words | spread | ttr | optional punctuation marks | style |
|---|---|---|---|---|---|---|
| Piece 9 | 8 | 107 | 0.262 | 0.645 | **2** | **0.9002** |
| Piece 10 | 9 | 119 | 0.412 | 0.681 | **26** | **0.3857** |

Same writer, same sitting, same subject, adjacent sentences. Piece 9 is flowing
prose and my service accused it at 0.7343. Piece 10 is the part where I listed
things out with numbers and brackets, and my service cleared it at 0.3349. The
entire difference is 24 brackets and commas.

That is not a detector telling writers apart. It is a detector telling
punctuation apart, and I would not be able to explain to anybody why one half
of their paragraph is fine and the other half is an accusation.

### How criteria 4 and 5 were tested

`run_eval.py` only talks to `/submit`, and two of my criteria are not shaped
like that. Criterion 4 needs a submission first and then an appeal against the
`content_id` that came back, which `scenarios.py` cannot express. Criterion 5
has a timing bound in it, and `run_eval.py` records status codes but not
durations.

**I extended the tooling rather than testing them by hand**, in
`run_extra_checks.py`. Three trials by hand is 24 appeals and 12 malformed
requests typed out, which is where mistakes come from, and a script leaves a
results file I can point at instead of a claim I made.

For criterion 4 it checks all three things the criterion names, not just the
status code: a 200 comes back, the log grows by **exactly one** line, and that
line says `under_review`. Reading the log length either side is the only way to
tell "wrote one line" apart from "wrote none" or "wrote two". For the unknown
ids it checks the 404 **and** that nothing at all was written.

### Real output from one trial

Produced by `run_eval.py::main`, scoring through `app.py::submit` and
`scoring.py::combine_signals`. Full file: `results/run_2026-11-05_1032_before.md`.

Trial 1 of the `clearly human` scenario, criterion 2:

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.1928,
    "model_score": 0.5088,
    "style_score": 0.0886,
    "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
    "sent": "My bike chain snapped two miles from home, in the rain, outside a shut"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3267,
    "model_score": 0.2829,
    "style_score": 0.3824,
    "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
    "sent": "The cat has decided the printer is hers now. Not the top of it. Inside"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2776,
    "model_score": 0.186,
    "style_score": 0.4578,
    "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
    "sent": "We got to the campsite about four and the pitch was on a slope, which "
  }
]
```

And trial 1 of criterion 4 and 5, produced by `run_extra_checks.py::main` via
`check_appeals` and `check_bad_input`. Full file:
`results/extra_checks_2026-11-05_1024_before.md`.

```json
{
  "appeals": [
    {"case": "valid appeal 1", "status": 200, "appeal_status": "under_review", "new_log_lines": 1, "ok": true, "why": ""},
    {"case": "valid appeal 2", "status": 200, "appeal_status": "under_review", "new_log_lines": 1, "ok": true, "why": ""},
    {"case": "unknown id 1", "status": 404, "error_field": "unknown_content_id", "new_log_lines": 0, "ok": true, "why": ""}
  ],
  "bad_input": [
    {"case": "no text field at all", "status": 400, "error_field": "missing_text", "seconds": 0.007, "ok": true, "why": ""},
    {"case": "text is empty", "status": 400, "error_field": "empty_text", "seconds": 0.005, "ok": true, "why": ""},
    {"case": "text is null", "status": 400, "error_field": "missing_text", "seconds": 0.006, "ok": true, "why": ""},
    {"case": "text is 50,000 words", "status": 400, "error_field": "text_too_long", "seconds": 0.008, "ok": true, "why": ""}
  ]
}
```

### The three trials told me less than I expected, and that is worth saying

Look at the Run 1, Run 2 and Run 3 columns for criterion 2. The gap is 0.4752
in all three. Not close to each other. **Identical, to four decimal places.**
Criterion 3 is the same: every calibration text scored exactly 0.1928, 0.4778,
0.4920, 0.7110, 0.8151 and 0.5428 in every trial.

`criteria.md` warned me the opposite would happen, and so did `run_eval.py`:
"your first signal runs a model, so identical input can score differently
twice". That is a reasonable thing to expect and it did not happen here. The
reason is that nothing in my pipeline is random. `detector.py::_load` puts the
model in eval mode and `perplexity` reads the loss straight out of a single
forward pass with no sampling anywhere, so the same text gives the same
perplexity every time. Everything downstream of it is arithmetic.

So the three trials are real evidence of one thing and no evidence of another.
They do show my service is **reproducible**, which matters, and they confirm the
unit 7 calibration numbers are still exactly where `notes.md` says. They show
**nothing at all** about whether my results are stable under variation, because
I sent the same bytes three times and got the same answer three times. Running
three identical trials is not the same as testing three times.

What would actually have tested that is varying the input rather than repeating
it: three different plain paragraphs rather than the same one three times. I
would rather write that down than present three identical numbers as though
agreeing with themselves proved something.

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
