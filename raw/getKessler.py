#! /usr/bin/env python
# *-* coding:utf-8 *-*

from re import findall,DOTALL

xml = open('comparanda.xml','r').read()

#entries = findall(r'<CONCEPT[^\n]*?S200="yes".*?</CONCEPT>',xml,DOTALL)
entries = findall(r'<CONCEPT[^\n].*?</CONCEPT>',xml,DOTALL)


langs = [
        'ALB',
        'ENG',
        'FRE',
        'GER',
        'HAW',
        'LAT',
        'NAV',
        'TUR',
        ]

kess = {}

for entry in entries:

    ID = findall('<CONCEPT ID="(.*?)"',entry)[0]
    
    kess[ID] = {}
    for lang in langs:
        lng = findall('<'+lang+'.*?</'+lang+'>',entry,DOTALL)[0]
        orth = findall('ORTH="(.*?)"',lng)
        word = findall('<WORD.*? PHON="(.*?)"',lng)
        stem = findall('<STEM.*? PHON="(.*?)"',lng)
        cog = findall('COGN_PROB="(.*?)"',lng)
        # possible cognates
        cogp = findall('COGN_POSS=(.*?)"',lng)
        loan = findall('LOAN="(.*?)"',lng)

        if len(loan) == 0:
            loan = ''
        else:
            loan = loan[0]

        if len(word) == 0:
            word = ''
        else:
            word = word[0]
        if len(orth) == 0:
            orth = ''
        else:
            orth = orth[0]
        if len(stem) == 0:
            stem = ''
        else:
            stem = stem[0]
        if len(cog) == 0:
            cog = ''
        else:
            cog = cog[0].upper().split(',')
        
        if len(cogp) == 0:
            cogp = ''
        else:
            cogp = cogp[0].upper().split(',')

        if cogp == ['']:
            cogp = ''

        try:
            cog += cogp
            print "yes",cog
        except:
            pass

        if cog == ['']:
            cog = ''
        
        #try:
        kess[ID][lang] = [orth,word,stem,cog,loan]

# assign cognate ids
count = 1
for k1 in kess.keys():
    for k2 in kess[k1].keys():
        try:
            for l in kess[k1][k2][3]:
                if kess[k1][l][4] == 'yes':
                    print "loan"
                    kess[k1][l][3] = -count
                else:
                    kess[k1][l][3] = count
            kess[k1][k2][3] = count
            count += 1
        except:
            pass

st = [
        ('tʃ','ʧ'),
        ('ts','ʦ'),
        ('dz','ʣ'),
        ('dʒ','ʤ'),
        ('í', 'i'),
        ('á', 'a'),
        ('pf','p͡f'),
        ('ó', 'o'),
        ('é', 'e'),
        ('ɫ','ł'),
        ('ṍ','õ'),
        ('R','ʀ'),
        ('ẽ','ẽ'),
        ('ã','ã'),
        ('ũ','ũ'),
        ('õ','õ'),
        ('ĩ','ĩ'),
        ]
out = open('kessler.lxs','w')
out.write('Number\tWords\t'+'\tCOG\t'.join(langs)+'\tCOG\n')

for i,k in enumerate(sorted(kess.keys(),key=lambda x:x.lower())):
    out.write(str(i+1) + '\t' + k)
    for lang in langs:
        word = kess[k][lang][2] #stem
        for sub,target in st:
            word = word.replace(sub,target)
        word = word.replace(' ','')
        out.write('\t' + word+'\t')
        out.write(str(kess[k][lang][3]))
    out.write('\n')
out.close()

out = open('KSL.csv','w')

out.write('#KSL\n')
out.write('ID\tTaxon\tGloss\tGlossID\tOrthography\tIPA\tTokens\tCogID\n')
s = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n'

langs = {
        'ALB':'Albanian',
        'ENG':'English',
        'FRE':'French',
        'GER':'German',
        'HAW':'Hawaiian',
        'NAV':'Navajo',
        'TUR':'Turkish',
        'LAT': 'Latin'
        }

z = 1
for i,j in zip(range(1,201),sorted(kess.keys(),key=lambda x:x.upper())):
    out.write('#\n')
    for l,k in sorted(langs.items(),key=lambda K:K[0]):
        x = kess[j][l]
        if x[4] == 'yes':
            cogid = -abs(x[3])
        else:
            cogid = abs(x[3])
        ipa = x[2]
        for ss,t in st:
            ipa = ipa.replace(ss,t)
        print ipa
        out.write(s.format(
            z,
            k,
            j,
            i,
            x[0],
            ipa.replace(' ',''),
            ipa,
            cogid
            ))
        z += 1
out.close()
