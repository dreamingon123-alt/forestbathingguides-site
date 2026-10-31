# Builds the static forestbathingguides.ch into site/ (generated, not committed).
# Edit src/ (text, quotes, redirects) or static/ (images), then: python3 build.py
import json, re, html, datetime, os
DOMAIN='https://forestbathingguides.ch'
NRC='https://catherinepeloquin.com/nature-reset-club/'
MAIL='forestbathingswitzerland@gmail.com'
CAL='https://calendly.com/cat-quin-ch/15'
LINKEDIN='https://www.linkedin.com/company/forestbathingswitzerland/'
GA='G-YPDB066MPB'; CLARITY='yktsoicgjc'
TODAY=datetime.date.today().isoformat()
HERO='/wp-content/uploads/2026/09/forest-group-circle-hero-hd.webp'

PAGES={
 'en':dict(path='/',out='site/index.html',lang='en-US',og='en_US',
   title='Forest Bathing (Shinrin Yoku) & Team Events in Switzerland',
   desc='Guided forest bathing (Shinrin Yoku), outdoor team events and coaching in Zug, Zurich and across Switzerland. Certified guides for teams, groups and individuals.',
   entity='Forest Bathing Switzerland is a network of certified forest therapy guides leading guided forest bathing (Shinrin Yoku) and nature experiences for teams, groups and individuals across Switzerland.',
   nav=[('#teams','Teams'),('#groups','Individuals & groups'),('#public','Public events'),('#faq','FAQ'),('/waldbaden/','Deutsch')],
   h_explore='Explore',h_contact='Contact',email_label='Email us',join='Join an upcoming event',call='Book a 15-minute call',country='Zug, Switzerland',
   imp='Impressum: Forest Bathing Switzerland, Catherine Peloquin, Zug, Switzerland.',
   privacy_h='Privacy',privacy='This page uses Google Analytics and Microsoft Clarity to understand how visitors use it. There are no forms on this site. If you email us, we use your message only to answer it.'),
 'de':dict(path='/waldbaden/',out='site/waldbaden/index.html',lang='de-CH',og='de_CH',
   title='Waldbaden in Zürich & Zug | Outdoor-Teamevents Schweiz',
   desc='Geführtes Waldbaden in Zug und Zürich für Einzelpersonen und Gruppen. Outdoor-Teamevents für Firmen in der ganzen Schweiz. Zertifizierte Guides.',
   entity='Forest Bathing Switzerland ist ein Netzwerk zertifizierter Waldtherapie-Guides für Waldbaden (Shinrin Yoku) und Naturerlebnisse für Teams, Gruppen und Einzelpersonen in der ganzen Schweiz.',
   nav=[('#teams','Teams'),('#groups','Einzelpersonen & Gruppen'),('#public','Öffentliche Anlässe'),('#faq','FAQ'),('/','English')],
   h_explore='Übersicht',h_contact='Kontakt',email_label='E-Mail schreiben',join='Nächste Anlässe',call='15-Minuten-Gespräch buchen',country='Zug, Schweiz',
   imp='Impressum: Forest Bathing Switzerland, Catherine Peloquin, Zug, Schweiz.',
   privacy_h='Datenschutz',privacy='Diese Seite nutzt Google Analytics und Microsoft Clarity, um zu verstehen, wie Besuchende sie nutzen. Es gibt keine Formulare auf dieser Seite. Wenn Sie uns eine E-Mail schreiben, verwenden wir Ihre Nachricht nur für die Antwort.'),
}
AREA=['Zug','Cham','Baar','Steinhausen','Oberwil','Walchwil','Oberägeri','Zurich','Lucerne','Switzerland']
SAMEAS=['https://www.myswitzerland.com/en-ch/planning/offers/forest-bathing-shinrin-yoku-from-zug/','https://www.zug-tourismus.ch/en/poi/poi-and-infrastructure/forest-bathing/','https://www.swissactivities.com/en-ch/hiking/forest-bathing-team-event-zug/','https://anft.earth/',LINKEDIN]

css=open('src/site.css').read().replace(DOMAIN+'/wp-content/','/wp-content/')
css+='''
/* static build additions */
#fbs-root .hero p.stat{font-size:clamp(20px,2.4vw,27px)!important;font-weight:700!important;color:#2d2d2d!important;max-width:500px;margin:14px 0 0!important;line-height:1.3;text-align:left!important}
.nav-in{gap:22px}
#fbs-root .nav-in .brand{margin-right:auto!important}
#fbs-root .nav-in .brand + a.nl{margin-left:28px}
#fbs-root .hero p.stat{padding:0!important;text-indent:0!important}
.nav-in a.nl,.nav-in .btn,.nav-in .brand{white-space:nowrap}
@media(max-width:1100px){.nav-in{gap:16px}.nav-in a.nl{font-size:14px}}
@media(max-width:860px){#fbs-root .nav-in a.nl.contact{display:inline!important;font-size:14px}.nav-in{gap:12px;padding:10px 16px}.nav-in .brand{font-size:0!important;gap:0}.nav-in .btn{padding:8px 12px!important;font-size:14px!important}}
footer.site{background:#2d2d2d;color:#cfcfbf;padding:56px 0 36px;font-size:15px;line-height:1.6}
footer.site .fgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px}
footer.site .fbrand{display:flex;align-items:center;gap:10px;color:#fff;font-size:19px;font-weight:700;margin-bottom:12px}
footer.site .fbrand img{width:36px;height:36px;filter:brightness(0) invert(1)}
footer.site h4{color:#fff;font-size:15px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px}
footer.site ul{list-style:none;margin:0;padding:0}
footer.site li{margin:0 0 8px}
#fbs-root footer.site a{color:#6ad3a8!important;text-decoration:none!important}
#fbs-root footer.site a:hover{text-decoration:underline!important}
footer.site .fbase{border-top:1px solid #4a4a4a;margin-top:36px;padding-top:20px;font-size:13.5px;color:#a9a99b}
footer.site details{margin-top:8px}
footer.site summary{cursor:pointer;color:#cfcfbf}
@media(max-width:860px){footer.site .fgrid{grid-template-columns:1fr;gap:28px}}
'''
quotes=json.load(open('src/quotes.json'))['quotes']

def tile(q,L):
    return ('<div style="background:#ffffff;border-radius:6px;padding:22px 20px"><p style="font-size:15.5px;margin-bottom:10px">&ldquo;'
            +html.escape(q['text'],quote=False)+'&rdquo;</p><p class="cite" style="color:#017d61;font-weight:500">'+html.escape(q[L])+'</p></div>')

def footer(L):
    p=PAGES[L]
    nav=''.join('<li><a href="%s">%s</a></li>'%(h,html.escape(t)) for h,t in p['nav'])
    return f'''<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="fbrand"><img src="/wp-content/uploads/2026/09/fbs-logo.webp" alt="" width="36" height="36">Forest Bathing Switzerland</div>
        <p>{html.escape(p['entity'])}</p>
      </div>
      <div><h4>{p['h_explore']}</h4><ul>{nav}</ul></div>
      <div><h4>{p['h_contact']}</h4><ul>
        <li><a href="mailto:{MAIL}">{p['email_label']}</a></li>
        <li><a href="{NRC}">{p['join']}</a></li>
        <li><a href="{CAL}">{p['call']}</a></li>
        <li><a href="{LINKEDIN}">LinkedIn</a></li>
        <li>{p['country']}</li></ul></div>
    </div>
    <div class="fbase">
      <p>{html.escape(p['imp'])}</p>
      <details><summary>{p['privacy_h']}</summary><p>{html.escape(p['privacy'])}</p></details>
      <p style="margin-top:10px">&copy; {datetime.date.today().year} Forest Bathing Switzerland</p>
    </div>
  </div>
</footer>'''

def faq_from(body):
    sec=body[body.find('class="faq"'):]
    out=[]
    for q,a in re.findall(r'<div class="q"><h3>(.*?)</h3><p>(.*?)</p></div>',sec,flags=re.S):
        clean=lambda s: html.unescape(re.sub(r'<[^>]+>','',s)).strip()
        out.append({"@type":"Question","name":clean(q),"acceptedAnswer":{"@type":"Answer","text":clean(a)}})
    assert len(out)>=5, 'FAQ parse failed'
    return out

def schema(L,body):
    p=PAGES[L]; url=DOMAIN+p['path']
    org={"@type":"Organization","@id":DOMAIN+"/#org","name":"Forest Bathing Switzerland","url":DOMAIN+"/",
         "logo":DOMAIN+"/wp-content/uploads/2024/10/cropped-Forest_Bathing_favicon-270x270.png",
         "description":PAGES['en']['entity'],
         "address":{"@type":"PostalAddress","addressLocality":"Zug","addressCountry":"CH"},
         "areaServed":[{"@type":"Place","name":a} for a in AREA],"knowsLanguage":["en","de","it"],"sameAs":SAMEAS,
         "member":[{"@type":"Person","name":"Catherine Peloquin","url":"https://catherinepeloquin.com"},
                   {"@type":"Person","name":"Daniela Weber","url":"https://www.danielaweber.ch"},
                   {"@type":"Person","name":"Lucia Catalano","url":"https://www.imwaldinuster.ch"}]}
    site={"@type":"WebSite","@id":DOMAIN+"/#website","url":DOMAIN+"/","name":"Forest Bathing Switzerland","publisher":{"@id":DOMAIN+"/#org"},"inLanguage":["en","de-CH"]}
    page={"@type":"WebPage","@id":url+"#webpage","url":url,"name":p['title'],"description":p['desc'],"inLanguage":p['lang'],
          "isPartOf":{"@id":DOMAIN+"/#website"},"about":{"@id":DOMAIN+"/#org"},"primaryImageOfPage":DOMAIN+HERO,"dateModified":TODAY}
    faq={"@type":"FAQPage","@id":url+"#faq","inLanguage":p['lang'],"mainEntity":faq_from(body)}
    return json.dumps({"@context":"https://schema.org","@graph":[org,site,page,faq]},ensure_ascii=False,indent=1)

TRACK='''document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a||typeof gtag!=='function')return;var h=a.getAttribute('href')||'';var n=h.indexOf('nature-reset-club')>-1?'join_event_click':h.indexOf('mailto:')===0?'email_click':h.indexOf('calendly.com')>-1?'call_booking_click':null;if(n)gtag('event',n,{link_url:h.split('?')[0],page_language:document.documentElement.lang});});'''

def head(L,body):
    p=PAGES[L]; url=DOMAIN+p['path']; e=html.escape
    return f'''<!doctype html>
<html lang="{p['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{DOMAIN}/">
<link rel="alternate" hreflang="de-CH" href="{DOMAIN}/waldbaden/">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Forest Bathing Switzerland">
<meta property="og:locale" content="{p['og']}">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}{HERO}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/wp-content/uploads/2024/10/cropped-Forest_Bathing_favicon-32x32.png" sizes="32x32">
<link rel="icon" href="/wp-content/uploads/2024/10/cropped-Forest_Bathing_favicon-192x192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/wp-content/uploads/2024/10/cropped-Forest_Bathing_favicon-180x180.png">
<link rel="preload" as="image" href="{HERO}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;900&display=swap">
<style>
{css}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');{TRACK}</script>
<script>(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{CLARITY}");</script>
<script type="application/ld+json">
{schema(L,body)}
</script>
</head>
<body>
'''

import shutil
shutil.rmtree('site',ignore_errors=True)
shutil.copytree('static','site')
for L in ('en','de'):
    b=open(f'src/{L}.html').read()
    b=b.replace('<!--QUOTES-->',''.join(tile(q,L) for q in quotes)).replace('<!--FOOTER-->',footer(L))
    os.makedirs(os.path.dirname(PAGES[L]['out']),exist_ok=True)
    open(PAGES[L]['out'],'w').write(head(L,b)+b+'\n</body>\n</html>\n')

open('site/404.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Forest Bathing Switzerland</title><link rel="icon" href="/wp-content/uploads/2024/10/cropped-Forest_Bathing_favicon-32x32.png"><style>body{{font-family:'Public Sans',Arial,sans-serif;background:#efffe1;color:#2d2d2d;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0;padding:24px;text-align:center}}a{{display:inline-block;margin:8px;background:#017d61;color:#fff;padding:12px 22px;border-radius:3px;text-decoration:none}}</style></head><body><div><img src="/wp-content/uploads/2026/09/fbs-logo.webp" alt="Forest Bathing Switzerland" width="64" height="64"><h1>This page does not exist.</h1><p>Diese Seite gibt es nicht.</p><a href="/">Forest Bathing Switzerland</a><a href="/waldbaden/">Waldbaden auf Deutsch</a></div></body></html>
''')
open('site/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
alts=f'<xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}/"/><xhtml:link rel="alternate" hreflang="de-CH" href="{DOMAIN}/waldbaden/"/><xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/"/>'
open('site/sitemap.xml','w').write(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
<url><loc>{DOMAIN}/</loc><lastmod>{TODAY}</lastmod>{alts}</url>
<url><loc>{DOMAIN}/waldbaden/</loc><lastmod>{TODAY}</lastmod>{alts}</url>
</urlset>
''')
open('site/.htaccess','w').write(open('src/htaccess.txt').read())

# Checks: catch the mistakes that have bitten this site before
USER,DOM=MAIL.split('@')
EMAILJS="<script>(function(){var u='%s',d='%s';document.querySelectorAll('a[href^=\"#email\"]').forEach(function(a){a.setAttribute('href','mailto:'+u+'@'+d+a.getAttribute('href').slice(6));});})();</script>"%(USER,DOM)
for L in ('en','de'):
    f=PAGES[L]['out']; out=open(f).read()
    out=out.replace('mailto:'+MAIL,'#email').replace('</body>',EMAILJS+'\n</body>',1)
    open(f,'w').write(out)
for L in ('en','de'):
    out=open(PAGES[L]['out']).read()
    assert MAIL not in out, L+': email address visible in HTML'

    assert out.count('<h1')==1, L+': exactly one H1'
    assert '—' not in re.sub(r'<script.*?</script>|<style>.*?</style>','',out,flags=re.S), L+': em dash in copy'
    assert 'forestbathingguides.ch/wp-content' not in re.sub(r'<script.*?</script>|<meta[^>]*>','',out,flags=re.S), L+': absolute upload URL left'
    for src in set(re.findall(r'(/wp-content/uploads/[^"\')\s]+)',out)):
        assert os.path.exists('site'+src), L+': missing image '+src
    assert 'Antonelli' not in out
print('built', TODAY)
