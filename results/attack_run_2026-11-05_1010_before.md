# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 10:10
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `60be3445-42c2-4f6a-a01b-5fd061f87c67` | human | 0.268 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3b7676d8-8485-4b0f-95b5-bb4fdd13aedb` | unsure | 0.416 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `6a2769be-d126-4822-9bf2-42d2db823ca6` | unsure | 0.562 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `e956f049-89d0-4530-a4be-09567dff1fdc` | unsure | 0.622 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `9da4fa7e-f523-4388-920d-7a844709d57d` | human | 0.312 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `5ee95382-8935-4579-b5d6-8de2c9436fd3` | unsure | 0.489 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `08c010d0-b361-4c5d-8a4f-e45b0d58254c` | unsure | 0.514 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `1cbf5dda-e730-46fc-9590-8a386b33bd01` | human | 0.347 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `39fcb041-230c-4c72-bfc8-35107bc62cb5` | unsure | 0.566 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `fdae36fb-59ec-4d47-a962-e26f5596e97e` | ai | 0.911 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `7f23bee6-6f8e-4d5b-b4af-45e85ca44c0a` | ai | 0.669 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `4a9c9fc7-2022-408c-a27b-299a6f172381` | ai | 0.790 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `7576f060-9ea7-4ab7-9739-d8e30c98506c` | ai | 0.802 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `769563eb-c710-4210-93f9-54d72e340404` | ai | 0.762 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `fc6871ae-3f0f-45e7-b8fa-dca0190743ab` | ai | 0.842 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `267bad8d-250e-4ede-b700-4994b48bd4da` | ai | 0.757 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `5ea45e2f-56c2-4613-902e-be9872f046af` | ai | 0.704 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `828a3ac9-9294-404f-a279-98eb854b1a51` | unsure | 0.484 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `686f77e2-00ad-4e10-a89c-0cc8ad1ed53d` | human | 0.283 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a042e30e-8ad7-460d-99cb-74494ce80ffc` | unsure | 0.572 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `71517309-1532-4c9a-a97c-893ec876b935` | unsure | 0.459 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `77f61083-4631-4433-8cfc-8dff6532c148` | human | 0.320 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `1f25abcc-52a9-4a5a-aa21-8a00017185f5` | unsure | 0.631 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 200 | `0c3a60d5-d26d-48e2-9d90-eeffd1e32d75` | ai | 0.875 |  |
| MF06 | malformed | text is emoji only | 200 | `5d4ea71c-f66b-4578-adf7-6e026492d625` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `cb06c847-2904-4cdf-b9d8-d8304f555879` | ai | 0.948 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `ebf3c426-051b-478a-84e8-3064d1ab0ad4` | unsure | 0.352 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c96184f0-3fe1-4287-80b0-8c8fbbd31a98` | human | 0.183 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `722772b3-9f73-4511-a68d-49bf47af3470` | human | 0.183 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `63b29abc-379e-47bf-b755-cf723a7e0283` | human | 0.183 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2e9519e7-16c9-445e-a2fa-3f01d2540cdb` | human | 0.183 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `13bc1f3d-c4da-4a18-899a-7daedde06f5f` | human | 0.183 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "60be3445-42c2-4f6a-a01b-5fd061f87c67",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2679,
  "model_score": 0.1635,
  "style_score": 0.6856,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "3b7676d8-8485-4b0f-95b5-bb4fdd13aedb",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4164,
  "model_score": 0.5943,
  "style_score": 0.3253,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "6a2769be-d126-4822-9bf2-42d2db823ca6",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5624,
  "model_score": 0.6662,
  "style_score": 0.4942,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "e956f049-89d0-4530-a4be-09567dff1fdc",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6223,
  "model_score": 0.6114,
  "style_score": 0.6337,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "9da4fa7e-f523-4388-920d-7a844709d57d",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3123,
  "model_score": 0.3212,
  "style_score": 0.3038,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "5ee95382-8935-4579-b5d6-8de2c9436fd3",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4889,
  "model_score": 0.5727,
  "style_score": 0.4296,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "08c010d0-b361-4c5d-8a4f-e45b0d58254c",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5145,
  "model_score": 0.5862,
  "style_score": 0.4614,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "1cbf5dda-e730-46fc-9590-8a386b33bd01",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.347,
  "model_score": 0.2452,
  "style_score": 0.7241,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "39fcb041-230c-4c72-bfc8-35107bc62cb5",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5657,
  "model_score": 0.7042,
  "style_score": 0.4849,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "fdae36fb-59ec-4d47-a962-e26f5596e97e",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9115,
  "model_score": 0.9792,
  "style_score": 0.8606,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "7f23bee6-6f8e-4d5b-b4af-45e85ca44c0a",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.6688,
  "model_score": 0.6175,
  "style_score": 0.7373,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "4a9c9fc7-2022-408c-a27b-299a6f172381",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7905,
  "model_score": 0.7387,
  "style_score": 0.86,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "7576f060-9ea7-4ab7-9739-d8e30c98506c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8025,
  "model_score": 0.8051,
  "style_score": 0.7999,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "769563eb-c710-4210-93f9-54d72e340404",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7618,
  "model_score": 0.8329,
  "style_score": 0.7091,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "fc6871ae-3f0f-45e7-b8fa-dca0190743ab",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8417,
  "model_score": 0.8005,
  "style_score": 0.8932,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "267bad8d-250e-4ede-b700-4994b48bd4da",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7575,
  "model_score": 0.8814,
  "style_score": 0.6815,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "5ea45e2f-56c2-4613-902e-be9872f046af",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7036,
  "model_score": 0.8816,
  "style_score": 0.6125,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "828a3ac9-9294-404f-a279-98eb854b1a51",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4836,
  "model_score": 0.4625,
  "style_score": 0.5071,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "686f77e2-00ad-4e10-a89c-0cc8ad1ed53d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2832,
  "model_score": 0.2044,
  "style_score": 0.4155,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a042e30e-8ad7-460d-99cb-74494ce80ffc",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5718,
  "model_score": 0.5943,
  "style_score": 0.5515,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "71517309-1532-4c9a-a97c-893ec876b935",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4592,
  "model_score": 0.4998,
  "style_score": 0.4253,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "77f61083-4631-4433-8cfc-8dff6532c148",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.3204,
  "model_score": 0.6401,
  "style_score": 0.2163,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "1f25abcc-52a9-4a5a-aa21-8a00017185f5",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6307,
  "model_score": 0.5583,
  "style_score": 0.7448,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "0c3a60d5-d26d-48e2-9d90-eeffd1e32d75",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8754,
  "model_score": 0.9976,
  "style_score": 0.8,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "5d4ea71c-f66b-4578-adf7-6e026492d625",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9984,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "cb06c847-2904-4cdf-b9d8-d8304f555879",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9479,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "Our checks suggest this was written by a computer rather than by you. We can be wrong about this, and these checks cannot prove who wrote anything. If you wrote this yourself, tell us and a person will read it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "ebf3c426-051b-478a-84e8-3064d1ab0ad4",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3516,
  "model_score": 0.2395,
  "style_score": 0.8,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c96184f0-3fe1-4287-80b0-8c8fbbd31a98",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.183,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "722772b3-9f73-4511-a68d-49bf47af3470",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.183,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "63b29abc-379e-47bf-b755-cf723a7e0283",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.183,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "2e9519e7-16c9-445e-a2fa-3f01d2540cdb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.183,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "13bc1f3d-c4da-4a18-899a-7daedde06f5f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.183,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We checked this piece and found nothing that looks like computer writing. As far as we can tell, you wrote it yourself.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
