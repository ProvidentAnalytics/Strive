import json, os

def load(fname):
    with open(fname) as f:
        return f.read()

def build():
    with open('dashboard_template_v2.html') as f:
        html = f.read()

    replacements = {
        'INJECT_SD':    load('data_split.json'),
        'INJECT_DAILY': load('data_daily_full.json'),
        'INJECT_RECS':  load('data_recordings.json'),
        'INJECT_LOG':   load('data_log.json'),
        'INJECT_FORMS': load('data_forms.json'),
        'INJECT_MKT':   load('data_marketing.json'),
        'INJECT_EXTRA': load('data_extra.json'),
        'INJECT_HMD':   load('data_hm_daily.json'),
    }

    for key, data in replacements.items():
        html = html.replace('/*' + key + '*/null', data, 1)

    with open('strive_ctm_clean.html', 'w') as f:
        f.write(html)

    print(f'Built: strive_ctm_clean.html — {len(html)//1024} KB')
    return html

if __name__ == '__main__':
    build()
