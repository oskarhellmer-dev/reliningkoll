#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Serverar den byggda sajten MED _headers-headers, sa CSP kan verifieras riktigt."""
import http.server, socketserver, os, re

ROOT = "/home/clawd/reliningkoll"
HDR = {
 "X-Content-Type-Options": "nosniff",
 "X-Frame-Options": "DENY",
 "Referrer-Policy": "strict-origin-when-cross-origin",
 "Permissions-Policy": "geolocation=(), camera=(), microphone=(), payment=(), usb=()",
 "Content-Security-Policy": ("default-src 'self'; base-uri 'self'; object-src 'none'; "
   "frame-ancestors 'none'; form-action https://formsubmit.co; img-src 'self' data:; "
   "style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; upgrade-insecure-requests"),
 "Cross-Origin-Opener-Policy": "same-origin",
}

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        for k, v in HDR.items(): self.send_header(k, v)
        super().end_headers()
    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8099), H) as httpd:
    httpd.serve_forever()
