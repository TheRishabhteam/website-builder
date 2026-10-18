from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps({"status": "AI Website Builder API is running!"}).encode())

    def do_POST(self):
        try:
            import anthropic
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))

            api_key = os.environ.get('ANTHROPIC_API_KEY', '')
            if not api_key:
                raise Exception("ANTHROPIC_API_KEY not set")

            client = anthropic.Anthropic(api_key=api_key)

            sec   = body.get('section', 'hero')
            bn    = body.get('bn', 'Business')
            bt    = body.get('bt', 'business')
            loc   = body.get('loc', 'India')
            svc   = body.get('svc', 'Professional services')
            wa    = body.get('wa', '')
            ext   = body.get('ext', '')
            p     = body.get('p',  '#0A66C2')
            s     = body.get('s',  '#1A3A5C')
            gr    = body.get('gr', 'linear-gradient(135deg,#0A66C2,#1A3A5C)')
            lt    = body.get('lt', '#EFF6FF')
            td    = body.get('td', '#1A1A2E')
            tm    = body.get('tm', '#6B7280')
            bg    = body.get('bg', '#0A1628')
            h_img = body.get('h_img', '')
            a_img = body.get('a_img', '')
            dv    = body.get('dv', 'cinematic')
            wal   = ('https://wa.me/' + wa.replace('+','').replace(' ','')) if wa else '#contact'

            sys_p = ("You are an expert HTML/CSS developer. Output ONLY raw HTML with inline CSS. "
                     "No markdown. No backticks. No explanation. "
                     "Use Google Fonts: Playfair Display + Inter. Use Font Awesome 6 icons. "
                     "Add data-aos attributes for animations. "
                     "Fully responsive: CSS grid auto-fit, clamp() for fonts, no fixed px widths. "
                     "Quality must match premium ThemeForest themes.")

            hero_map = {
                'cinematic':       f'Fullscreen img bg url({h_img}) center/cover, overlay rgba(0,0,0,0.70). Centered. Italic serif tagline above h1. h1 clamp(42px,7vw,80px) Playfair white. Thin hr divider. WhatsApp CTA. After hero: white stats bar 4 gradient-text numbers grid auto-fit.',
                'split_doctor':    f'50/50 split. LEFT dark {bg}: green-pulse badge, h1 clamp(36px,5vw,68px) white Playfair, subtext, 2 CTAs, trust tags, phone. RIGHT: bg-image url({h_img}) cover. min-height 100vh. Mobile: image hidden.',
                'bold_typography': f'Dark {bg}. Left-aligned. ALL CAPS h1 clamp(52px,8vw,96px) weight:900 letter-spacing:-3px. One word color {p}. Subtext. Solid CTA. Stats bottom-left.',
                'minimal_centered':f'White/light bg. Centered. Playfair h1 clamp(36px,5vw,64px) dark, one word gradient {gr}. 2 minimal buttons. Colorful stats row below.',
                'luxury_elegant':  f'Image bg url({h_img}) 0.60 overlay. Centered. Thin uppercase badge. Italic Playfair h1 weight:200 letter-spacing:4px white. Gold thin divider. Two outline buttons.',
            }

            svc_map = {
                'icon_cards':         f'Grid auto-fit minmax(260px,1fr) gap:24px. White cards radius:16px pad:28px. Gradient icon circle. border-top:4px {p}. Name, desc, price From ₹XXX. Hover lift. bg:{lt}.',
                'dark_glassmorphism': f'Dark {bg}. Cards rgba(255,255,255,0.08) backdrop-filter:blur(16px) border rgba(255,255,255,0.15) radius:16px. White text. Accent icon.',
                'numbered_list':      f'Two-col. Left: numbered 01-06 outline numbers {p}, service name, desc. Right: image {a_img} radius:16px. Dark bg.',
                'minimal_grid':       f'White bg. Borderless grid. Icon {p}, bold name, desc, price. hover border-left:3px {p} animation.',
                'alternating_layout': f'3 rows alternating text+image. Large decorative bg numbers. White bg. Image radius:16px.',
            }

            prompts = {
                'hero': f"""Write STUNNING PREMIUM hero for "{bn}" ({bt} in {loc}).
Services:{svc} | USP:{ext or 'quality & expertise'} | Phone:{wa} | WA:{wal}
Image:{h_img or 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=1920&q=80'}
Primary:{p} | Gradient:{gr} | Dark:{bg}
STYLE ({dv}): {hero_map.get(dv, hero_map['cinematic'])}
Rules: Playfair headings, Inter body, clamp() sizes, data-aos, fully responsive.
Also add stats bar after hero: white bg, 4 stats gradient text, grid auto-fit.
Return ONLY raw HTML starting with <section.""",

                'services': f"""Write PREMIUM services for "{bn}" ({bt}).
Services:{svc} | Primary:{p} | Gradient:{gr} | Light:{lt}
STYLE ({dv}): {svc_map.get(dv, svc_map['icon_cards'])}
Use REAL {bt} services from "{svc}" with descriptions and ₹ prices.
Font Awesome icons. data-aos staggered. section id="services" pad:80px 0.
Return ONLY raw <section> HTML.""",

                'about': f"""Write PREMIUM about for "{bn}" ({bt}).
USP:{ext or 'expert team'} | Primary:{p} | Gradient:{gr}
Image:{a_img or 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80'}
Split grid 1fr 1fr gap:60px.
LEFT: badge + h2 Playfair + paragraph + 4 checkmarks gradient circles + 3 stats + CTA.
RIGHT: img radius:20px height:440px cover shadow + floating stat badge overlay.
Add <style> for @media max-width:768px: 1 column, img height:280px.
section id="about" white bg pad:80px 0. data-aos.
Return ONLY <section> + <style>.""",

                'testimonials': f"""Write PREMIUM testimonials for "{bn}" ({bt}).
Primary:{p} | bg:{lt} | Services:{svc}
Grid auto-fit minmax(280px,1fr). White cards radius:20px pad:30px shadow.
Each: gold stars, italic quote, gradient avatar circle, bold name, role+city.
3 REALISTIC Indian testimonials mentioning {bt} services.
section id="testimonials" bg:{lt} pad:80px 0. data-aos.
Return ONLY raw <section> HTML.""",
            }

            prompt = prompts.get(sec, f"Write premium {sec} section for {bn} ({bt}). Primary:{p}. Return only raw HTML.")

            msg = client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=4000,
                system=sys_p,
                messages=[{"role": "user", "content": prompt}]
            )

            html = msg.content[0].text
            html = html.replace('```html','').replace('```','').strip()

            self.send_response(200)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({'html': html, 'src': 'Claude'}).encode())

        except Exception as e:
            self.send_response(500)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _cors(self):
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')

    def log_message(self, format, *args):
        pass
