#!/usr/bin/env python3
"""A local stand-in for the event receiver, for rehearsing submit.py.

    python3 tests/mock_receiver.py            # listens on 127.0.0.1:8730
    python3 leaderboard/submit.py --url http://127.0.0.1:8730 \\
        --handle test_handle --file samples/eth1_es.txt --lang es-ES

It implements the public submission contract and nothing else: it scores
with this repository's own probe.py, prints the row it WOULD have sent, and
sends it nowhere. It has no ingestion settings and cannot reach the live
table. Standard library only.

The contract (one prompt per submission):
    POST /submit   JSON {"handle", "prompt", "lang"?, "variant"?}
    GET  /health
  - the receiver recomputes RiskScore and Patterns; any client-sent score,
    stamps or identity fields are ignored
  - handle: 2-24 chars of letters, digits, _ . -  -> UserPrincipal handle@lb
  - prompt: 1-4000 characters, prompt text only, never a model response
  - anything containing "flag{" is rejected
  - one submission per handle per 20 seconds
"""
import json, os, re, sys, time, unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import probe  # noqa: E402

MAX_PROMPT, RATE_SECONDS = 4000, 20
HANDLE_RE = re.compile(r"^[A-Za-z0-9_.-]{2,24}$")
LANG_RE = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$")
MIXED = "mul"
STAMP_MAP = {"L1": "script_diversity", "L2": "code_switch",      # identical to the
             "L3": "transliteration", "L4": "framing"}           # event receiver's
_last = {}


def arabic_present(text):
    return any("ARABIC" in unicodedata.name(c, "") for c in text if c.isalpha())


def classify(handle, prompt, lang, variant):
    if not HANDLE_RE.match(handle or ""):
        return None, "handle must be 2-24 chars: letters, digits, _ . -"
    if not isinstance(prompt, str) or not 1 <= len(prompt) <= MAX_PROMPT:
        return None, f"prompt must be 1-{MAX_PROMPT} characters"
    if "flag{" in prompt.lower():
        return None, "that is a CTF flag, not a prompt"
    lang = (lang or "").strip() or ("ar-MSA" if arabic_present(prompt) else "en-US")
    if not LANG_RE.match(lang):
        return None, f"{lang!r} is not a language code (use an ISO code, or mul)"
    variant = (variant or "V1").strip().upper()
    variant = variant if variant in ("V1", "V2") else "V1"
    score, hits = probe.analyze(prompt)
    stamps = [STAMP_MAP[h.split()[0]] for h in hits]
    has_ar = arabic_present(prompt)
    if lang != MIXED and ((lang.startswith("en") and has_ar) or
                          (lang.startswith("ar") and not has_ar and "transliteration" not in stamps)):
        stamps.append("label_mismatch")
    return {"TimeGenerated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "UserPrincipal": f"{handle}@lb", "Language": lang, "Variant": variant,
            "RiskScore": float(score), "Patterns": ",".join(stamps),
            "PromptPreview": prompt[:200]}, None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"ok": True, "mode": "mock"})
        self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        if self.path != "/submit":
            return self._send(404, {"ok": False, "error": "not found"})
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
        except Exception:
            return self._send(400, {"ok": False, "error": "body must be JSON"})
        handle = str(payload.get("handle", "")).strip()
        row, err = classify(handle, payload.get("prompt", ""), payload.get("lang"), payload.get("variant"))
        if err:
            return self._send(400, {"ok": False, "error": err})
        now = time.time()
        if now - _last.get(handle, 0) < RATE_SECONDS:
            return self._send(429, {"ok": False, "error": f"one submission per {RATE_SECONDS}s per handle"})
        _last[handle] = now
        if os.environ.get("MOCK_QUIET") != "1":
            print("[mock] would send:", json.dumps({k: v for k, v in row.items() if k != "PromptPreview"}))
        self._send(200, {"ok": True, "score": row["RiskScore"],
                         "patterns": row["Patterns"].split(","),
                         "badge": row["RiskScore"] >= 5,
                         "note": "mock receiver: scored locally, sent nowhere"})


def serve(host="127.0.0.1", port=8730):
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    srv = serve(port=int(os.environ.get("MOCK_PORT", "8730")))
    print("mock receiver on http://127.0.0.1:%d  (Ctrl+C to stop; sends nothing anywhere)" % srv.server_port)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
