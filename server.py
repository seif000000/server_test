from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

bookmarks = []

class BookmarkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # نقرأ ملف الـ HTML
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # نجهز قائمة الروابط HTML
        items = ""
        for title, url in bookmarks:
            items += f'<li><a href="{url}" target="_blank">{title}</a></li>'
        
        # نستبدل الـ __BOOKMARKS__ بالروابط اللي اتخزنوا
        html = html.replace("__BOOKMARKS__", items)
        
        # نبعت الرد للعميل
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(length).decode()
        data = parse_qs(post_data)
        title = data.get("title", [""])[0]
        url = data.get("url", [""])[0]

        # نخزن الرابط الجديد
        bookmarks.append((title, url))

        # نعيد التوجيه للصفحة الرئيسية (GET)
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

# نشغل السيرفر
server_address = ("localhost", 8000)
httpd = HTTPServer(server_address, BookmarkHandler)
print("✅ done http://localhost:8000")
httpd.serve_forever()

