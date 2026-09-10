"""Minimal local web UI for the evidence-governed reporting MVP."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .report_engine import ReportEngine


HTML_PATH = Path(__file__).with_name("index.html")


class Handler(BaseHTTPRequestHandler):
    engine = ReportEngine()

    def _send(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(
                200,
                "text/html; charset=utf-8",
                HTML_PATH.read_bytes(),
            )
        else:
            self._send(
                404,
                "text/plain; charset=utf-8",
                b"Not found",
            )

    def do_POST(self):
        if self.path != "/api/answer":
            return self._send(
                404,
                "application/json",
                b'{"error":"Not found"}',
            )

        try:
            payload = json.loads(
                self.rfile.read(
                    int(self.headers.get("Content-Length", "0"))
                )
            )

            question = payload.get("question", "").strip()

            if not question:
                raise ValueError("A question is required.")

            response = self.engine.answer(question)
            status = 200

        except (ValueError, json.JSONDecodeError) as error:
            response = {
                "status": "bad_request",
                "message": str(error),
            }
            status = 400

        self._send(
            status,
            "application/json; charset=utf-8",
            json.dumps(
                response,
                ensure_ascii=False,
            ).encode(),
        )

    def log_message(self, format, *args):
        return


def main():
    # Render provides PORT when deployed.
    # Locally, we use port 8000.
    port = int(os.environ.get("PORT", "8000"))

    # 0.0.0.0 allows both local and cloud access.
    server = ThreadingHTTPServer(
        ("0.0.0.0", port),
        Handler,
    )

    print(f"MVP running at http://0.0.0.0:{port}")

    server.serve_forever()


if __name__ == "__main__":
    main()