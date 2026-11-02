#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

def check_text(text) -> dict | None:
    """
    Decide whether this is something I am willing to score.

    Returns None when the text is fine, or the error body to send back when it
    is not. Keeping it in one place means /submit has one way of saying no,
    and every way of saying no looks the same to whoever is reading the answer.

    These four cases are exactly the ones my criterion 5 names.
    """
    if text is None:
        return {
            "error": "missing_text",
            "message": "Send a 'text' field with the writing you want checked.",
        }

    if not isinstance(text, str):
        return {
            "error": "text_not_a_string",
            "message": f"'text' has to be a string, not {type(text).__name__}.",
        }

    if not text.strip():
        return {
            "error": "empty_text",
            "message": "The 'text' field is empty. There is nothing to check.",
        }

    if len(text) > config.MAX_TEXT_CHARS:
        return {
            "error": "text_too_long",
            "message": (
                f"That is {len(text):,} characters and the limit is "
                f"{config.MAX_TEXT_CHARS:,}. Only the opening few hundred words "
                f"get read anyway, so send a shorter piece."
            ),
        }

    if len(text.strip()) < config.MIN_TEXT_CHARS:
        return {
            "error": "text_too_short",
            "message": (
                f"That is {len(text.strip())} characters and I need at least "
                f"{config.MIN_TEXT_CHARS}. A few sentences, so there is "
                f"something to measure."
            ),
        }

    return None


@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """
    import detector
    import scoring
    import stylometry

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}

    text = payload.get("text")
    creator_id = payload.get("creator_id") or "unknown"

    # Check the input before doing any work. My criterion 5 says a bad request
    # comes back as a 400 with an error field, never a 500, and never takes
    # more than 10 seconds. The only way to keep that promise is to say no
    # before the text ever reaches the model.
    problem = check_text(text)
    if problem:
        audit.log_rejection(creator_id=creator_id, reason=problem["error"])
        return jsonify(problem), 400

    # Make the id first. It is the only handle the writer has on this decision,
    # and /appeal needs it later.
    content_id = str(uuid.uuid4())

    # Signal one: how predictable the writing is to a language model.
    try:
        model_score = detector.model_signal(text)
    except detector.DetectorUnavailable as exc:
        audit.log_rejection(creator_id=creator_id, reason="detector_unavailable")
        return jsonify({
            "error": "detector_unavailable",
            "message": f"The detector could not run: {exc}",
        }), 503
    except ValueError as exc:
        # The model needs a few tokens before it can be surprised by anything.
        audit.log_rejection(creator_id=creator_id, reason="text_too_short_to_score")
        return jsonify({
            "error": "text_too_short_to_score",
            "message": str(exc),
        }), 400

    # Signal two: the shape of the writing, without reading a word of it.
    # No try/except around this one. It is plain arithmetic over the text, it
    # does not load anything, and the edge cases it used to have (one sentence,
    # no words at all) are handled inside stylometry.py itself.
    style_score = stylometry.style_signal(text)

    # Two numbers become one. The rule, and the reasoning behind it, live in
    # scoring.py::combine_signals.
    confidence = scoring.combine_signals(model_score, style_score)

    # One number becomes something a person can read. A score of 0.62 means
    # nothing to a writer. The sentence is the part that does.
    guess, label = scoring.score_to_label(confidence)

    # Write it down before answering. A decision that is not in the log is a
    # decision nobody can check later.
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=confidence,
        label=label,
        status="decided",
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
    })


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({
            "error": "missing_content_id",
            "message": "Send the content_id you got back when you submitted.",
        }), 400

    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({
            "error": "missing_reasoning",
            "message": "Tell us why you think this is wrong.",
        }), 400

    # Does this piece actually exist? My criterion 4 says an appeal against an
    # id I have never seen gets a 404, and this is why: if a mistyped id came
    # back with a cheerful 200, the writer would walk away believing their
    # appeal had been recorded when nothing had been written down anywhere.
    # That failure is silent on both ends, which makes it the worst kind.
    existing = audit.entries_for(content_id)
    if not existing:
        return jsonify({
            "error": "unknown_content_id",
            "message": (
                f"No submission with the id '{content_id}'. Check the "
                f"content_id from the response when you submitted."
            ),
        }), 404

    # Take the creator from the original decision rather than from the appeal.
    # Whoever is appealing does not get to tell me whose work this was.
    creator_id = existing[0].get("creator_id", "unknown")

    # Append the appeal next to the original decision. This does not overwrite
    # the decision and it does not score anything again. The log is append
    # only, so the original stays exactly where it was and the appeal sits
    # after it. Someone reading later sees what was decided, that it was
    # challenged, and in what order.
    entry = audit.log_appeal(
        content_id=content_id,
        creator_id=creator_id,
        reasoning=reasoning,
    )

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": (
            "Thank you. Your appeal has been recorded and this piece is now "
            "waiting for a person to look at it. Nothing further happens to "
            "your post in the meantime."
        ),
        "recorded_at": entry["timestamp"],
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
