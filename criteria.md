# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Wrongly accusing my own writing

Of 10 pieces of writing that I wrote myself, **at most 1** comes back with a
guess of `ai`. This has to hold in each of the three trials separately, so
results of 2, 1, 2 across the trials count as a miss, not an average of 1.67.

**Why this target:**

On a writing site the two kinds of mistake do not cost the same. If some
generated text slips through, the site carries a post it did not want. If a
real writer gets told a machine wrote their work, that person is accused of
cheating by a system they cannot argue with, and the appeal is all they get. So
I am willing to let more AI text through in exchange for fewer wrong
accusations, and 1 in 10 is already higher than I would want to defend to the
person it happens to.

I picked 1 rather than 0 because I do not believe 0 is reachable. My Milestone 1
trace found that both of my signals fail the same kind of writer in the same
direction, so plain writing is going to get caught sometimes. A target of 0
would be a target I set knowing it was a wish.

---

## 2. Clearly AI and clearly human writing actually separate

Across 3 pieces I am confident are AI generated and 3 I am confident are human
written, the **average combined score of the AI group is at least 0.30 above
the average combined score of the human group**, in each of the three trials.

**Why this target:**

0.30 is not an arbitrary round number. My unsure band runs from 0.35 to 0.65,
which is 0.30 wide. If the two kinds of writing do not separate by at least the
width of that band, then clearly AI text and clearly human text can both land
inside it, and every label my service produces is a coin flip wearing a
confident sentence. The gap has to be at least as wide as the gap I claim to be
measuring, or my thresholds are decoration.

I am measuring group averages rather than demanding that every single AI piece
beat every single human piece, because one weird input should not sink the
whole criterion. If the averages fail, something real is wrong with a signal.

---

## 3. All three labels are reachable

Across my 6 calibration pieces, **each of the three labels appears at least
once**: at least one `human`, at least one `unsure`, and at least one `ai`, in
each of the three trials.

**Why this target:**

A label no score can produce is a gap in my ranges that I would never notice,
because nothing errors. It just silently never happens.

The one I care about most here is `unsure`. If that label never fires, I have
built a service that is always certain, and Milestone 1 already showed me it has
no right to be. A system that can only say "a person wrote this" or "a machine
wrote this" has removed the honest answer from its own vocabulary, and the
honest answer is the one that protects the writer in the middle.

---

## 4. An appeal always lands

Of 5 appeals sent against content ids that really exist, **all 5** return a 200,
write exactly one new line to `logs/audit.jsonl`, and that new line has a status
of `under_review`. Of 3 appeals sent against content ids that do not exist,
**all 3** return a 404 and write no decision line at all. This holds in each of
the three trials.

**Why this target:**

This is the only criterion where I will accept nothing less than every single
case passing, and that is deliberate. The appeal is the entire remedy. It is the
one thing standing between a writer who was wrongly accused and nothing at all.
A detector that is wrong sometimes is a system with a known flaw. An appeal path
that is wrong sometimes is a system that loses people's objections without
telling them, which is worse, because the writer thinks they have been heard.

The 404 half matters as much as the 200 half. If a typo'd content id quietly
returns a cheerful 200, the writer walks away believing their appeal was
recorded when nothing was written down anywhere.

Note on how this gets tested: `run_eval.py` only sends to `/submit`, so it
cannot test this one on its own. I have to submit first, take the content id
that comes back, and then appeal against it. I will say in my write up whether I
did that by hand or extended the tooling.

---

## 5. Bad input never crashes the service

Sent 4 malformed requests (`text` missing entirely, `text` empty, `text` set to
null, and `text` of 50,000 words), **all 4** come back with a 400 and a JSON
body containing an `error` field, **none** return a 500, and **none** take
longer than 10 seconds to answer. This holds in each of the three trials.

**Why this target:**

A crash on malformed input is one of the most ordinary real failures there is,
and it is the first thing anybody probing my service will find. A 500 is not
just an error, it is information: it tells whoever sent it that they found a
place where my handler broke, which is a map of where to push harder.

The 10 second bound is in there because of the 50,000 word case specifically. My
first signal loads text into a model, and a huge submission is a way to tie up
the service without ever triggering an error at all. Refusing it quickly costs
me nothing, since my detector only reads the first 400 tokens anyway, so
accepting an enormous body buys no extra accuracy and hands out a free way to
make everyone else wait.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
