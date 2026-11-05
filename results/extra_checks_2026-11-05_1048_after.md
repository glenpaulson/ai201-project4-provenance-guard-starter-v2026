# Extra checks — after

- Produced by: `run_extra_checks.py::main`
- Criterion 4 by `check_appeals`, criterion 5 by `check_bad_input`
- 3 trials · 2026-11-05 10:48

## Criterion 4 — the appeal path

| Trial | Valid appeals 200 + one log line + under_review | Unknown ids 404 + nothing logged |
|---|---|---|
| 1 | 5 of 5 | 3 of 3 |
| 2 | 5 of 5 | 3 of 3 |
| 3 | 5 of 5 | 3 of 3 |

## Criterion 5 — bad input

| Trial | Refused cleanly | Any 500 | Slowest |
|---|---|---|---|
| 1 | 4 of 4 | no | 0.027s |
| 2 | 4 of 4 | no | 0.024s |
| 3 | 4 of 4 | no | 0.010s |

---

## What actually came back

**Trial 1**

```json
{
  "appeals": [
    {
      "case": "valid appeal 1",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 2",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 3",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 4",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 5",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 1",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 2",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 3",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    }
  ],
  "bad_input": [
    {
      "case": "no text field at all",
      "status": 400,
      "error_field": "missing_text",
      "seconds": 0.009,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is empty",
      "status": 400,
      "error_field": "empty_text",
      "seconds": 0.007,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is null",
      "status": 400,
      "error_field": "missing_text",
      "seconds": 0.027,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is 50,000 words",
      "status": 400,
      "error_field": "text_too_long",
      "seconds": 0.008,
      "ok": true,
      "why": ""
    }
  ]
}
```

**Trial 2**

```json
{
  "appeals": [
    {
      "case": "valid appeal 1",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 2",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 3",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 4",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 5",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 1",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 2",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 3",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    }
  ],
  "bad_input": [
    {
      "case": "no text field at all",
      "status": 400,
      "error_field": "missing_text",
      "seconds": 0.024,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is empty",
      "status": 400,
      "error_field": "empty_text",
      "seconds": 0.008,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is null",
      "status": 400,
      "error_field": "missing_text",
      "seconds": 0.019,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is 50,000 words",
      "status": 400,
      "error_field": "text_too_long",
      "seconds": 0.011,
      "ok": true,
      "why": ""
    }
  ]
}
```

**Trial 3**

```json
{
  "appeals": [
    {
      "case": "valid appeal 1",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 2",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 3",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 4",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "valid appeal 5",
      "status": 200,
      "appeal_status": "under_review",
      "new_log_lines": 1,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 1",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 2",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    },
    {
      "case": "unknown id 3",
      "status": 404,
      "error_field": "unknown_content_id",
      "new_log_lines": 0,
      "ok": true,
      "why": ""
    }
  ],
  "bad_input": [
    {
      "case": "no text field at all",
      "status": 400,
      "error_field": "missing_text",
      "seconds": 0.008,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is empty",
      "status": 400,
      "error_field": "empty_text",
      "seconds": 0.008,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is null",
      "status": 400,
      "error_field": "missing_text",
      "seconds": 0.008,
      "ok": true,
      "why": ""
    },
    {
      "case": "text is 50,000 words",
      "status": 400,
      "error_field": "text_too_long",
      "seconds": 0.01,
      "ok": true,
      "why": ""
    }
  ]
}
```
