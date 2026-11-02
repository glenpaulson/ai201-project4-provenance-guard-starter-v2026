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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

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
