import json
from anonymization import anonymize_swe

extraKeywords = []
ignoredSentences = []

filenames = ['raw2018.json', 'raw2019.json']
newfilenames = ['2018_pre.json','2019_pre.json']

anon = anonymize_swe()
anon.initialize()

for index,filename in enumerate(filenames):
    res = []

    with open(filename) as f:
        raw = json.load(f)

    for i,ad in enumerate(raw):
        new_text = anon.anonymizeText(ad['annons_text'],extraKeywords,ignoredSentences)[0]
        new_behov = anon.anonymizeText(ad['behov'],extraKeywords,ignoredSentences)[0]
        ad['annons_text'] = new_text
        ad['behov'] = new_behov
        res.append(ad)
        if i%1000==0:
            print(i)

    # sort by publication date
    # res = sorted(res, key=lambda k: k['publication_date'], reverse=True) 

    with open(newfilenames[index],'w') as f:
        json.dump(res, f)

print('end')