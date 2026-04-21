#!/usr/bin/env python3
"""
Proxy simples para Anthropic API
"""
import http.server
import socketserver
import json
import urllib.request
import os
import sys

PORT = 8001
API_KEY = "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"

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        print("[8001] POST recebido")
        
        try:
            data = json.loads(body)
            
            # Chamar Anthropic API
            req = urllib.request.Request(
                'https://api.anthropic.com/v1/messages',
                data=body.encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': API_KEY,
                    'anthropic-version': '2023-06-01'
                }
            )
            
            resp = urllib.request.urlopen(req, timeout=60)
            result = resp.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result)
            print("[8001] Resposta enviada")
            
        except Exception as e:
            print(f"[8001] Erro: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("=" * 60)
    print(f"[PROXY] Rodando em http://127.0.0.1:{PORT}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[PROXY] Parado")
        sys.exit(0)
