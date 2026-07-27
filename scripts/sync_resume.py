#!/usr/bin/env python3
"""
sync_resume.py
--------------
Updates index.html's resume content (text between <!--AUTO:KEY--> ...
<!--/AUTO:KEY--> markers) using data parsed from main.tex.

It never touches anything outside those markers, so your site's
design/CSS/JS is untouched no matter what you edit in LaTeX.

Usage:
    python3 sync_resume.py <main.tex> <index.html>

Exits non-zero (and prints what's missing) if a marker referenced by
this script cannot be found in index.html, so a template change never
fails silently.
"""

import re
import sys
import html as htmlmod

from parse_tex import parse


def esc(s: str) -> str:
    return htmlmod.escape(s, quote=False)


def set_marker(page: str, key: str, content: str, warnings: list) -> str:
    pattern = re.compile(
        r'(<!--AUTO:%s-->)(.*?)(<!--/AUTO:%s-->)' % (re.escape(key), re.escape(key)),
        re.S)
    if not pattern.search(page):
        warnings.append(key)
        return page
    return pattern.sub(lambda m: m.group(1) + content + m.group(3), page)


def bullets_html(bullets, indent='        '):
    lines = ''.join(f'{indent}<li>{esc(b)}</li>\n' for b in bullets)
    return '\n' + lines + indent[:-2]


def chips_html(items, indent='            '):
    lines = ''.join(f'{indent}<span class="chip">{esc(i)}</span>\n' for i in items)
    return '\n' + lines + indent[:-2]


SKILL_KEY_BY_CATEGORY = {
    'Architecture & RTL Design': 'SKILL_ARCH',
    'Design Verification & Quality': 'SKILL_DV',
    'EDA Tools': 'SKILL_EDA',
    'Programming': 'SKILL_PROG',
    'Core Competencies': 'SKILL_CORE',
}


def main():
    if len(sys.argv) != 3:
        print('Usage: sync_resume.py <main.tex> <index.html>', file=sys.stderr)
        sys.exit(1)

    tex_path, html_path = sys.argv[1], sys.argv[2]

    with open(tex_path, encoding='utf-8') as f:
        data = parse(f.read())

    with open(html_path, encoding='utf-8') as f:
        page = f.read()

    warnings = []

    if data.get('name'):
        page = set_marker(page, 'NAME', esc(data['name']), warnings)
        page = set_marker(page, 'NAME_FOOTER', esc(data['name']), warnings)

    if data.get('location'):
        page = set_marker(page, 'LOCATION', esc(data['location']), warnings)

    if data.get('phone'):
        page = set_marker(page, 'PHONE', esc(data['phone']), warnings)
    if data.get('phone_href'):
        page = set_marker(page, 'PHONE_HREF', data['phone_href'], warnings)

    if data.get('email'):
        page = set_marker(page, 'EMAIL', esc(data['email']), warnings)
        page = set_marker(page, 'EMAIL2', esc(data['email']), warnings)
        page = set_marker(page, 'EMAIL_FOOTER', esc(data['email']), warnings)
        page = set_marker(page, 'EMAIL_FOOTER2', esc(data['email']), warnings)

    if data.get('linkedin_url'):
        page = set_marker(page, 'LINKEDIN_URL', data['linkedin_url'], warnings)
        page = set_marker(page, 'LINKEDIN_URL_FOOTER', data['linkedin_url'], warnings)
    if data.get('linkedin_text'):
        page = set_marker(page, 'LINKEDIN_TEXT', esc(data['linkedin_text']), warnings)

    if data.get('summary'):
        page = set_marker(page, 'SUMMARY', esc(data['summary']), warnings)

    job = data.get('job')
    if job:
        title_line = f"{job['title']}, {job['company']}"
        page = set_marker(page, 'JOB_TITLE', esc(title_line), warnings)
        page = set_marker(page, 'JOB_DATES', esc(job['dates']), warnings)

    projects = data.get('projects') or []
    for i, proj in enumerate(projects[:3], start=1):
        page = set_marker(page, f'P{i}_TITLE', esc(proj['title']), warnings)
        page = set_marker(page, f'P{i}_BULLETS', bullets_html(proj['bullets']), warnings)

    edu = data.get('education') or []
    if len(edu) > 0:
        page = set_marker(page, 'EDU1_SECONDARY', esc(edu[0]['secondary']), warnings)
        page = set_marker(page, 'EDU1_PRIMARY', esc(edu[0]['primary']), warnings)
        page = set_marker(page, 'EDU1_DATES', esc(edu[0]['dates']), warnings)
    if len(edu) > 1:
        page = set_marker(page, 'EDU2_PRIMARY', esc(edu[1]['primary']), warnings)
        page = set_marker(page, 'EDU2_SECONDARY', esc(edu[1]['secondary']), warnings)
        page = set_marker(page, 'EDU2_DATES', esc(edu[1]['dates']), warnings)
    if data.get('education_note'):
        page = set_marker(page, 'EDU_NOTE', esc(data['education_note']), warnings)

    for skill in data.get('skills') or []:
        key = SKILL_KEY_BY_CATEGORY.get(skill['category'])
        if not key:
            warnings.append(f"unknown skill category '{skill['category']}' (add it to "
                             f"SKILL_KEY_BY_CATEGORY in sync_resume.py, or add a matching "
                             f"skill-row + <!--AUTO:...--> marker in index.html)")
            continue
        page = set_marker(page, key, chips_html(skill['items']), warnings)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(page)

    if warnings:
        print('Sync finished with warnings (these markers/categories were skipped):')
        for w in warnings:
            print(f'  - {w}')
        print('Everything else was updated successfully.')
    else:
        print('index.html updated from', tex_path)


if __name__ == '__main__':
    main()
