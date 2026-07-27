#!/usr/bin/env python3
"""
parse_tex.py
------------
Parses S Aditha Krishna Bhat's RenderCV-style resume main.tex into a
plain Python dict. Built specifically around this resume's LaTeX
structure (twocolentry / onecolentry / highlights environments).

If you restructure the .tex significantly (new sections, different
environments), the regexes here will need matching updates.
"""

import re
import sys
import json


def clean(s: str) -> str:
    """Strip LaTeX markup down to plain text."""
    s = re.sub(r'\\textbf\{(.*?)\}', r'\1', s)
    s = re.sub(r'\\textit\{(.*?)\}', r'\1', s)
    s = s.replace(r'\&', '&')
    s = s.replace(r'\%', '%')
    s = s.replace(r'\_', '_')
    s = re.sub(r'--', '\u2013', s)   # -- -> en dash
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def parse(tex: str) -> dict:
    data = {}

    m = re.search(r'\\fontsize\{25 ?pt\}\{25 ?pt\}\\selectfont\s+(.*?)\n', tex)
    data['name'] = clean(m.group(1)) if m else None

    m = re.search(r'\\mbox\{([^{}]+)\}%', tex)
    data['location'] = clean(m.group(1)) if m else None

    m = re.search(r'tel:([^}]+)\}\{([^}]+)\}', tex)
    data['phone'] = clean(m.group(2)) if m else None
    data['phone_href'] = m.group(1).replace('-', '').replace(' ', '') if m else None

    m = re.search(r'mailto:([^}]+)\}\{([^}]+)\}', tex)
    data['email'] = clean(m.group(2)) if m else None

    m = re.search(r'\\hrefWithoutArrow\{(https://[^}]*linkedin[^}]*)\}\{([^}]+)\}', tex)
    data['linkedin_url'] = m.group(1) if m else None
    data['linkedin_text'] = clean(m.group(2)) if m else None

    m = re.search(
        r'\\section\{Summary\}.*?\\begin\{onecolentry\}\s*(.*?)\s*\\end\{onecolentry\}',
        tex, re.S)
    data['summary'] = clean(m.group(1)) if m else None

    exp_m = re.search(r'\\section\{Experience\}(.*?)\\section\{Education\}', tex, re.S)
    exp_section = exp_m.group(1) if exp_m else ''

    m = re.search(
        r'\\begin\{twocolentry\}\{\s*(.*?)\s*\}\s*\\textbf\{(.*?)\}, (.*?)\\end\{twocolentry\}',
        exp_section, re.S)
    data['job'] = {
        'dates': clean(m.group(1)),
        'title': clean(m.group(2)),
        'company': clean(m.group(3)),
    } if m else None

    projects = []
    for pm in re.finditer(
            r'\\item \\textbf\{(PROJECT \d+.*?):\}\s*\\begin\{itemize\}(.*?)\\end\{itemize\}',
            exp_section, re.S):
        tag_title = clean(pm.group(1))
        body = pm.group(2)
        bullets = [clean(b) for b in re.split(r'\\item\s+', body) if b.strip()]
        parts = re.split(r'\s*\u2013\s*', tag_title, maxsplit=1)
        projects.append({
            'tag': parts[0].title(),  # "PROJECT 1" -> "Project 1"
            'title': parts[1] if len(parts) > 1 else '',
            'bullets': bullets,
        })
    data['projects'] = projects

    edu_m = re.search(r'\\section\{Education\}(.*?)\\section\{Technical Skills\}', tex, re.S)
    edu_section = edu_m.group(1) if edu_m else ''

    edu_entries = []
    for em in re.finditer(
            r'\\begin\{twocolentry\}\{\s*(.*?)\s*\}\s*\\textbf\{(.*?)\}, (.*?)\\end\{twocolentry\}',
            edu_section, re.S):
        edu_entries.append({
            'dates': clean(em.group(1)),
            'primary': clean(em.group(2)),
            'secondary': clean(em.group(3)),
        })
    data['education'] = edu_entries

    m = re.search(
        r'\\begin\{highlights\}\s*\\item\s+(.*?)\s*\\end\{highlights\}',
        edu_section, re.S)
    data['education_note'] = clean(m.group(1)) if m else None

    skills_start = tex.find('\\section{Technical Skills}')
    skills_section = tex[skills_start:] if skills_start != -1 else ''
    skills = []
    for sm in re.finditer(
            r'\\begin\{onecolentry\}\s*\\textbf\{([^:]+):\}\s*(.*?)\s*\\end\{onecolentry\}',
            skills_section, re.S):
        cat = clean(sm.group(1))
        items = [clean(x) for x in sm.group(2).split(',')]
        skills.append({'category': cat, 'items': items})
    data['skills'] = skills

    return data


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: parse_tex.py <main.tex>', file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        tex_content = f.read()
    print(json.dumps(parse(tex_content), indent=2, ensure_ascii=False))
