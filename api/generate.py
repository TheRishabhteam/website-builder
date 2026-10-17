import json
import os

try:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY',''))
except:
    client = None

def generate_html(prompt, max_tokens=4000):
    if not client:
        raise Exception("Anthropic client not available")
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[{"role":"user","content":prompt}]
    )
    txt = msg.content[0].text
    txt = txt.replace('```html','').replace('```','').strip()
    return txt

class handler:
    def __init__(self, request, client_address, server):
        pass

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length',0))
            body = json.loads(self.rfile.read(length))
            sec = body.get('section','hero')
            bn = body.get('bn','Business')
            bt = body.get('bt','business')
            loc = body.get('loc','India')
            svc = body.get('svc','Services')
            wa = body.get('wa','')
            ext = body.get('ext','')
            p = body.get('p','#0A66C2')
            s = body.get('s','#1A3A5C')
            gr = body.get('gr','linear-gradient(135deg,#0A66C2,#1A3A5C)')
            lt = body.get('lt','#EFF6FF')
            td = body.get('td','#1A1A2E')
            tm = body.get('tm','#6B7280')
            bg = body.get('bg','#0A1628')
            h_img = body.get('h_img','')
            a_img = body.get('a_img','')
            dv = body.get('dv','cinematic')
            wal = f"https://wa.me/{wa.replace('+','').replace(' ','')}" if wa else '#contact'

            sys = "Output ONLY raw HTML with inline CSS. No markdown. No backticks. Fully responsive using CSS grid auto-fit and clamp(). No fixed px layout widths."

            prompts = {
                'hero': f"""Write a STUNNING PREMIUM hero for "{bn}" ({bt} in {loc}).
Services:{svc} | USP:{ext} | WhatsApp:{wal} | Phone:{wa}
Hero image:{h_img}
Primary:{p} | Gradient:{gr} | Dark bg:{bg}
STYLE ({dv}):
- cinematic: fullscreen image, dark overlay 0.72, centered, big h1 clamp(42px,7vw,80px), italic tagline above, decorative hr, WhatsApp CTA, glassmorphism stats below
- split_doctor: 50/50 split, left dark bg text+CTAs+trust badges, right image only, min-height:100vh
- bold_typography: dark bg, giant ALL CAPS h1 clamp(52px,8vw,96px), one word underlined {p}, left-aligned stats
- minimal_centered: white/light bg, centered Playfair h1 one word gradient, minimal buttons, colorful stats row below
- luxury_elegant: image 0.6 overlay, thin uppercase badge, centered italic h1 font-weight:200 letter-spacing:4px, gold divider
Apply the '{dv}' style. data-aos on all elements. Add stats bar (4 stats, gradient text) after hero.
Return ONLY raw <section> HTML.""",

                'services': f"""Write PREMIUM services section for "{bn}" ({bt}).
Services:{svc} | Primary:{p} | Gradient:{gr} | Light bg:{lt}
STYLE ({dv}):
- icon_cards: grid auto-fit minmax(260px,1fr), white cards, gradient icon circle, border-top {p}, hover lift, prices in ₹
- dark_glassmorphism: dark bg {bg}, glassmorphism cards rgba(255,255,255,0.08) backdrop-filter:blur(16px)
- numbered_list: two-col, left numbered 01-06 outline numbers, right large image
- minimal_grid: borderless, icon+name+desc+price, hover underline animation {p}
- alternating_layout: 3 rows alternating text+image with large bg numbers
Apply '{dv}'. REAL {bt} services from: {svc}. Realistic ₹ prices.
section id="services", padding 80px 0, data-aos. Return ONLY <section> HTML.""",

                'about': f"""Write PREMIUM about for "{bn}" ({bt}).
USP:{ext} | Primary:{p} | Gradient:{gr}
About image:{a_img}
Split grid 1fr 1fr gap:60px. Left: badge+h2 Playfair+paragraph+4 checkmarks gradient icons+stats row+CTA button.
Right: img border-radius:20px height:440px object-fit:cover box-shadow + floating badge overlay.
@media max-width:768px grid 1 column, img height:280px.
section id="about", white bg, padding 80px 0. data-aos. Return ONLY <section>+<style> HTML.""",

                'testimonials': f"""Write PREMIUM testimonials for "{bn}" ({bt}).
Primary:{p} | bg:{lt} | Services:{svc}
grid auto-fit minmax(280px,1fr). White cards radius:20px shadow.
Each: 5 gold stars ★★★★★, italic quote in "", avatar circle initial gradient bg, bold name, role city.
3 REALISTIC testimonials mentioning actual {bt} services.
section id="testimonials" padding 80px 0 bg:{lt}. data-aos. Return ONLY <section> HTML.""",
            }

            prompt = prompts.get(sec, f"Write a {sec} section for {bn} in {bt}. Primary: {p}. Return only raw HTML.")
            html = generate_html(sys+"\n\n"+prompt, 4000)

            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({'html':html,'src':'Claude'}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({'error':str(e)}).encode())
