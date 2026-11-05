#!/usr/bin/env python3
"""
The two criteria run_eval.py cannot reach.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_extra_checks.py --label before  # in another

`run_eval.py` sends text to /submit and records what came back. Two of my five
criteria are not shaped like that:

  **Criterion 4** is about the appeal path. An appeal needs a real content_id,
  so it needs a submission first and then an appeal against the id that came
  back. `scenarios.py` cannot express a two step request.

  **Criterion 5** has a timing bound in it: nothing takes longer than 10
  seconds. `run_eval.py` records the status code but not how long it took.

The brief says to test these by hand or extend the tooling, and to say which I
did. I extended the tooling, for two reasons. Three trials by hand is 24
appeals and 12 malformed requests typed out, which is where mistakes come from.
And a script leaves a results file, so the evidence is something I can point at
rather than something I claim.

Writes `results/extra_checks_<date>.md`.

⚠️ Rate limiting interferes with this. Each submission here gets its own
creator_id so it does not trip the per minute limit, but if you see a 429
where you expected a 200, that is the limiter and not the route. Run with
AI201_RATE_LIMITS=0 on a separate port to tell them apart.
"""

import argparse
import datetime as dt
import json
import sys
import time
import uuid

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

# Long enough to get past MIN_TEXT_CHARS, and dull enough that what it scores
# does not matter. This is testing the appeal path, not the detector.
APPEAL_TEXT = (
    "I wrote this paragraph myself so that there is something to appeal "
    "against. It needs to be long enough to get past my minimum length check "
    "and that is the only thing being asked of it."
)

# The four bad inputs criterion 5 names.
BAD_BODIES = [
    ("no text field at all", {"creator_id": "extra_bad_missing"}),
    ("text is empty", {"text": "", "creator_id": "extra_bad_empty"}),
    ("text is null", {"text": None, "creator_id": "extra_bad_null"}),
    ("text is 50,000 words", {"text": "word " * 50000,
                              "creator_id": "extra_bad_huge"}),
]


def post(url, path, body, timeout):
    """Send one request. Returns (status, payload, seconds, error)."""
    import requests

    started = time.perf_counter()
    try:
        response = requests.post(f"{url}{path}", json=body, timeout=timeout)
        elapsed = time.perf_counter() - started
        payload = response.json() if response.content else {}
        return response.status_code, payload, elapsed, None
    except Exception as exc:  # noqa: BLE001
        return None, {}, time.perf_counter() - started, f"{type(exc).__name__}: {exc}"


def log_length(url, timeout):
    """How many entries the audit log holds right now."""
    import requests

    try:
        return requests.get(f"{url}/log", timeout=timeout).json()["count"]
    except Exception:  # noqa: BLE001
        return None


def check_appeals(url, timeout, trial):
    """
    Criterion 4. Five appeals against ids that exist, three against ids that
    do not.

    For each valid one I check three things, because the criterion names three:
    a 200 comes back, exactly one new line appears in the log, and that line
    says `under_review`. Checking the log length either side is the only way to
    tell "wrote one line" from "wrote none" or "wrote two".
    """
    results = []

    for i in range(1, 6):
        creator = f"extra_appeal_{trial}_{i}_{uuid.uuid4().hex[:6]}"
        status, submitted, _, error = post(
            url, "/submit", {"text": APPEAL_TEXT, "creator_id": creator}, timeout)

        if status != 200 or not submitted.get("content_id"):
            results.append({
                "case": f"valid appeal {i}",
                "status": status,
                "ok": False,
                "why": error or f"the submission itself returned {status}",
            })
            continue

        content_id = submitted["content_id"]
        before = log_length(url, timeout)
        status, payload, _, error = post(
            url, "/appeal",
            {"content_id": content_id,
             "reasoning": "I wrote every word of this myself."}, timeout)
        after = log_length(url, timeout)

        wrote_one = (before is not None and after is not None
                     and after - before == 1)
        ok = (status == 200
              and payload.get("status") == "under_review"
              and wrote_one)
        results.append({
            "case": f"valid appeal {i}",
            "status": status,
            "appeal_status": payload.get("status"),
            "new_log_lines": None if before is None else after - before,
            "ok": ok,
            "why": error or "",
        })

    for i, bad_id in enumerate(
            ["not-an-id", "00000000-0000-0000-0000-000000000000",
             f"typo-{uuid.uuid4().hex[:8]}"], 1):
        before = log_length(url, timeout)
        status, payload, _, error = post(
            url, "/appeal",
            {"content_id": bad_id, "reasoning": "I wrote this"}, timeout)
        after = log_length(url, timeout)

        wrote_nothing = (before is not None and after is not None
                         and after == before)
        results.append({
            "case": f"unknown id {i}",
            "status": status,
            "error_field": payload.get("error"),
            "new_log_lines": None if before is None else after - before,
            "ok": status == 404 and wrote_nothing,
            "why": error or "",
        })

    return results


def check_bad_input(url, timeout):
    """
    Criterion 5. Four malformed requests: a 400 with an error field, never a
    500, never slower than 10 seconds.
    """
    results = []
    for description, body in BAD_BODIES:
        status, payload, elapsed, error = post(url, "/submit", body, timeout)
        results.append({
            "case": description,
            "status": status,
            "error_field": payload.get("error"),
            "seconds": round(elapsed, 3),
            "ok": (status == 400
                   and bool(payload.get("error"))
                   and elapsed <= 10.0),
            "why": error or "",
        })
    return results


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="", help="e.g. before / after")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    trials = []
    for trial in range(1, args.trials + 1):
        print(f"\ntrial {trial}")
        appeals = check_appeals(args.url, args.timeout, trial)
        passed = sum(1 for r in appeals if r["ok"])
        valid = [r for r in appeals if r["case"].startswith("valid")]
        unknown = [r for r in appeals if r["case"].startswith("unknown")]
        print(f"  criterion 4  valid appeals {sum(1 for r in valid if r['ok'])}/5, "
              f"unknown ids {sum(1 for r in unknown if r['ok'])}/3")

        bad = check_bad_input(args.url, args.timeout)
        slowest = max(r["seconds"] for r in bad)
        print(f"  criterion 5  {sum(1 for r in bad if r['ok'])}/4 refused "
              f"cleanly, slowest {slowest:.3f}s")

        trials.append({"appeals": appeals, "bad_input": bad})

    write_report(trials, args)


def write_report(trials, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"extra_checks_{stamp}{label}.md"

    lines = [
        f"# Extra checks{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_extra_checks.py::main`",
        "- Criterion 4 by `check_appeals`, criterion 5 by `check_bad_input`",
        f"- {len(trials)} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Criterion 4 — the appeal path",
        "",
        "| Trial | Valid appeals 200 + one log line + under_review | Unknown ids 404 + nothing logged |",
        "|---|---|---|",
    ]
    for n, t in enumerate(trials, 1):
        valid = [r for r in t["appeals"] if r["case"].startswith("valid")]
        unknown = [r for r in t["appeals"] if r["case"].startswith("unknown")]
        lines.append(f"| {n} | {sum(1 for r in valid if r['ok'])} of 5 | "
                     f"{sum(1 for r in unknown if r['ok'])} of 3 |")

    lines += ["", "## Criterion 5 — bad input", "",
              "| Trial | Refused cleanly | Any 500 | Slowest |", "|---|---|---|---|"]
    for n, t in enumerate(trials, 1):
        bad = t["bad_input"]
        any500 = any((r["status"] or 0) >= 500 for r in bad)
        lines.append(f"| {n} | {sum(1 for r in bad if r['ok'])} of 4 | "
                     f"{'yes' if any500 else 'no'} | "
                     f"{max(r['seconds'] for r in bad):.3f}s |")

    lines += ["", "---", "", "## What actually came back", ""]
    for n, t in enumerate(trials, 1):
        lines += [f"**Trial {n}**", "", "```json",
                  json.dumps(t, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
