"""Builds the English page, the Arabic page, the sitemap and the preview from template.html.
The template holds English text; each translatable element carries its Arabic in data-ar."""
import re, sys, os
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('OUT', os.path.join(SRC, '..'))
# Public address of the site, no trailing slash. Change it here when the domain changes.
SITE = os.environ.get('SITE', 'https://elsherbini26.github.io/harvest')
T = open(os.path.join(SRC, 'template.html'), encoding='utf-8').read()

PAGES = {
 'en': dict(lang='en', dir='ltr', p='', url=SITE + '/', locale='en_US', locale_alt='ar_EG',
   title='Harvest Training &amp; Education Center',
   desc='Harvest Training &amp; Education Center, Egypt, since 1987. Language, computer and management courses for individuals and organisations. Licensed by the Ministry of Education and accredited by ITIDA.',
   og_desc='Language, computer and management courses for individuals and organisations since 1987.',
   other_href='ar/', other_lang='ar', other_label='العربية', theme_label='Dark'),
 'ar': dict(lang='ar', dir='rtl', p='../', url=SITE + '/ar/', locale='ar_EG', locale_alt='en_US',
   title='هارفست للتدريب والتعليم | دورات لغات وحاسب آلي وبرامج إدارية',
   desc='مركز هارفست للتدريب والتعليم في مصر منذ 1987. دورات لغة إنجليزية وحاسب آلي وICDL وبرامج إدارية للأفراد والمؤسسات، بترخيص من وزارة التربية والتعليم واعتماد ITIDA.',
   og_desc='دورات لغات وحاسب آلي وبرامج إدارية للأفراد والمؤسسات منذ 1987.',
   other_href='../', other_lang='en', other_label='English', theme_label='داكن'),
}

def fill(html, v):
    for k, val in dict(v, site=SITE).items():
        html = html.replace('{{' + k + '}}', val)
    assert '{{' not in html, re.findall(r'\{\{\w+\}\}', html)
    return html

def to_arabic(html):
    html = re.sub(r'(<(\w+)\b[^>]*\bdata-ar="([^"]*)"[^>]*>)[^<]*(</\2>)', lambda m: m.group(1) + m.group(3) + m.group(4), html)
    def attr(m, name):
        tag = m.group(0); ar = re.search(r'data-ar-%s="([^"]*)"' % name[0], tag).group(1)
        return re.sub(r'\b%s="[^"]*"' % name[1], lambda _: '%s="%s"' % (name[1], ar), tag, count=1)
    html = re.sub(r'<[^>]*\bdata-ar-label="[^>]*>', lambda m: attr(m, ('label', 'aria-label')), html)
    html = re.sub(r'<[^>]*\bdata-ar-alt="[^>]*>', lambda m: attr(m, ('alt', 'alt')), html)
    return html

def strip(html):
    return re.sub(r' data-ar(?:-label|-alt)?="[^"]*"', '', html)

en = strip(fill(T, PAGES['en']))
ar = strip(to_arabic(fill(T, PAGES['ar'])))
os.makedirs(os.path.join(OUT, 'ar'), exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(en)
open(os.path.join(OUT, 'ar', 'index.html'), 'w', encoding='utf-8').write(ar)
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
alt = ''.join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n' % (l, PAGES[l]['url']) for l in PAGES)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
 + ''.join('  <url>\n    <loc>%s</loc>\n%s  </url>\n' % (PAGES[l]['url'], alt) for l in PAGES) + '</urlset>\n')

# Single-file preview: English body that keeps data-ar, plus a shim that swaps language in place
if len(sys.argv) > 1:
    body = fill(T, PAGES['en']); body = body[body.index('<body>') + 6: body.index('<!--/BODY-->')]
    css = open(os.path.join(OUT, 'css', 'style.css'), encoding='utf-8').read()
    js = open(os.path.join(OUT, 'js', 'main.js'), encoding='utf-8').read()
    shim = r'''
(function(){var r=document.documentElement,b=document.getElementById("lang-toggle");
var T=[].slice.call(document.querySelectorAll("[data-ar]"));T.forEach(function(e){e.setAttribute("data-en",e.textContent)});
b.addEventListener("click",function(ev){ev.preventDefault();var l=r.lang==="ar"?"en":"ar";r.lang=l;r.dir=l==="ar"?"rtl":"ltr";
T.forEach(function(e){e.textContent=e.getAttribute("data-"+l)});b.textContent=l==="ar"?"English":"العربية";
document.dispatchEvent(new Event("harvest:lang"))});})();'''
    open(sys.argv[1], 'w', encoding='utf-8').write(
      '<title>Harvest Training Center</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
      '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap">\n'
      '<style>\n' + css + '\n</style>\n' + body + '\n<script>\n' + js + shim + '\n</script>\n')
print('built', len(en), len(ar))
