# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 10:46
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `ac489066-0c06-4f0f-ac02-d6d70f1c43a5` | human | 0.268 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e120fb85-3621-4183-ad90-611fd34db1d0` | unsure | 0.416 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `92fd54cb-5feb-459d-bb9c-e2df887bb17f` | unsure | 0.562 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `5a72688a-21f8-4e86-84b3-e6e997d7499f` | unsure | 0.622 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c143436f-24a0-4bb2-bd96-ada33a5b91f2` | human | 0.312 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `8fbfcaf5-eb95-4b66-990e-46721b83c084` | unsure | 0.489 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c02d29c7-a100-4a42-8462-c8083a8c4ae9` | unsure | 0.514 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `5a03cb6d-0f39-4677-a2bb-688ad1f6ef93` | human | 0.347 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `20fee20f-6fa5-457e-b144-b898b3bfcef6` | unsure | 0.566 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `fb7c44d6-2043-4234-bef4-83ae92003734` | ai | 0.911 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `154b2c94-ff01-4d93-af85-0435df1f575a` | ai | 0.669 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `ba12867d-b9ba-47c7-90f4-5e33a5b5e5d0` | ai | 0.790 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `86325918-94be-4b94-9d57-e748c5f53fad` | ai | 0.802 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `1222c52c-1d38-4446-b63a-f054ea45f393` | ai | 0.762 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `5df639cc-ed5d-4233-aa07-ad9cab9dff2a` | ai | 0.842 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `944bf352-2924-43ec-995c-f965083522f5` | ai | 0.757 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3613bf12-284f-47c0-bca2-d2db0256b68c` | ai | 0.704 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `be6d97df-629e-4427-871b-e0f95f592a55` | unsure | 0.484 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `4f09916c-57b8-4449-9287-a4632c787db5` | human | 0.283 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `49568269-c347-4d86-8ef4-eabf173b5c10` | unsure | 0.572 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `78ed565b-8c55-4273-b311-9d3750a863b2` | unsure | 0.459 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `3a1bf0b8-0f5f-4c4b-b9cd-d695b0d0b796` | human | 0.320 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `503c10f7-20f3-49b9-9f50-c6ad2ce5c42f` | unsure | 0.631 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 200 | `7f8e4f96-8586-478c-898b-5ed9726213fa` | unsure | 0.600 |  |
| MF06 | malformed | text is emoji only | 200 | `fd7b3efe-4a64-45be-bd7b-168b5a5cfe89` | unsure | 0.600 |  |
| MF07 | malformed | text is right-to-left script | 200 | `14423467-496b-4fe8-9bbc-fe27f56a4857` | ai | 0.846 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c7a91234-0a43-4404-9baf-585e9342564b` | unsure | 0.352 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a95a62fb-f2fc-4179-9301-34a15e02ff8e` | human | 0.183 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fcaa400b-4d2f-461f-b91a-c5bb6e4272ab` | human | 0.183 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `caf6a1c3-7abd-4071-b759-320d67e55c3b` | human | 0.183 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3f8f69bf-0291-4ed2-aa53-c50e3b7e699f` | human | 0.183 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `834c417c-08a3-463c-b87f-619087017f36` | human | 0.183 |  |
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
  "content_id": "ac489066-0c06-4f0f-ac02-d6d70f1c43a5",
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
  "content_id": "e120fb85-3621-4183-ad90-611fd34db1d0",
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
  "content_id": "92fd54cb-5feb-459d-bb9c-e2df887bb17f",
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
  "content_id": "5a72688a-21f8-4e86-84b3-e6e997d7499f",
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
  "content_id": "c143436f-24a0-4bb2-bd96-ada33a5b91f2",
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
  "content_id": "8fbfcaf5-eb95-4b66-990e-46721b83c084",
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
  "content_id": "c02d29c7-a100-4a42-8462-c8083a8c4ae9",
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
  "content_id": "5a03cb6d-0f39-4677-a2bb-688ad1f6ef93",
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
  "content_id": "20fee20f-6fa5-457e-b144-b898b3bfcef6",
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
  "content_id": "fb7c44d6-2043-4234-bef4-83ae92003734",
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
  "content_id": "154b2c94-ff01-4d93-af85-0435df1f575a",
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
  "content_id": "ba12867d-b9ba-47c7-90f4-5e33a5b5e5d0",
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
  "content_id": "86325918-94be-4b94-9d57-e748c5f53fad",
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
  "content_id": "1222c52c-1d38-4446-b63a-f054ea45f393",
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
  "content_id": "5df639cc-ed5d-4233-aa07-ad9cab9dff2a",
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
  "content_id": "944bf352-2924-43ec-995c-f965083522f5",
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
  "content_id": "3613bf12-284f-47c0-bca2-d2db0256b68c",
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
  "content_id": "be6d97df-629e-4427-871b-e0f95f592a55",
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
  "content_id": "4f09916c-57b8-4449-9287-a4632c787db5",
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
  "content_id": "49568269-c347-4d86-8ef4-eabf173b5c10",
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
  "content_id": "78ed565b-8c55-4273-b311-9d3750a863b2",
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
  "content_id": "3a1bf0b8-0f5f-4c4b-b9cd-d695b0d0b796",
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
  "content_id": "503c10f7-20f3-49b9-9f50-c6ad2ce5c42f",
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
  "content_id": "7f8e4f96-8586-478c-898b-5ed9726213fa",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6002,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
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
  "content_id": "fd7b3efe-4a64-45be-bd7b-168b5a5cfe89",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6003,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We could not tell whether a person or a computer wrote this, so we are not going to say either way. This is not a finding against you. Your post stays exactly where it is and nothing about it has been reported to anyone.",
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
  "content_id": "14423467-496b-4fe8-9bbc-fe27f56a4857",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8464,
  "model_score": 0.9064,
  "style_score": 0.8,
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
  "content_id": "c7a91234-0a43-4404-9baf-585e9342564b",
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
  "content_id": "a95a62fb-f2fc-4179-9301-34a15e02ff8e",
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
  "content_id": "fcaa400b-4d2f-461f-b91a-c5bb6e4272ab",
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
  "content_id": "caf6a1c3-7abd-4071-b759-320d67e55c3b",
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
  "content_id": "3f8f69bf-0291-4ed2-aa53-c50e3b7e699f",
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
  "content_id": "834c417c-08a3-463c-b87f-619087017f36",
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
