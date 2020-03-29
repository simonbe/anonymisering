import json

filenames = ['2018_pre.json','2019_pre.json']
filenames_new = ['2018.json','2019.json']

fields_rem_adresser = [
                    ['adresser','ARBETSORTADRESS','id'],['adresser','ARBETSORTADRESS','raderad'],['adresser','ARBETSORTADRESS','rekryteringsbehov_id'],['adresser','ARBETSORTADRESS','typ'],['adresser','ARBETSORTADRESS','visa_ej_adress'],
                    ['adresser','BESOKSADRESS','id'],['adresser','BESOKSADRESS','raderad'],['adresser','BESOKSADRESS','rekryteringsbehov_id'],['adresser','BESOKSADRESS','typ'],['adresser','BESOKSADRESS','visa_ej_adress'],
                    ['adresser','POSTADRESS','id'],['adresser','POSTADRESS','raderad'],['adresser','POSTADRESS','rekryteringsbehov_id'],['adresser','POSTADRESS','typ'],['adresser','POSTADRESS','visa_ej_adress']
                    ]

fields_rem_matchningsprofil = [ ['matchningsprofil','GEOADRESS','id'],['matchningsprofil','GEOADRESS','matchningsprofil_id'], ['matchningsprofil','GEOADRESS','typ'],
                                ['matchningsprofil','YRKESROLL','id'],['matchningsprofil','YRKESROLL','matchningsprofil_id'], ['matchningsprofil','YRKESROLL','typ'],
                                ['matchningsprofil','YRKE','id'],['matchningsprofil','YRKE','matchningsprofil_id'], ['matchningsprofil','YRKE','typ']
                                ]

fields_rem_rekr = [ ['rekryteringsbehov','anvandarid'], ['rekryteringsbehov','arbetsgivareid'], ['rekryteringsbehov','epost'], ['rekryteringsbehov','id'], 
                    ['rekryteringsbehov','kalla'], ['rekryteringsbehov','kalla'], ['rekryteringsbehov','matchningsprofilid'], ['rekryteringsbehov','telefonnummer'],
                    ['rekryteringsbehov','raderad'], ['rekryteringsbehov','skapad_av'], ['rekryteringsbehov','skapad_tid'], ['rekryteringsbehov','uppdaterad_av'],
                    ['rekryteringsbehov','uppdaterad_tid'], ['rekryteringsbehov','visa_ej_antal_platser'], ['rekryteringsbehov','visa_ej_arbetsgivare']]

subfields_to_remove = []
subfields_to_remove.extend(fields_rem_adresser)
subfields_to_remove.extend(fields_rem_matchningsprofil)
subfields_to_remove.extend(fields_rem_rekr)

fields_to_remove = ['ansokningssatt_epost','ansokningssatt_via_af','avpublicerad_av','avpubliceringsdatum','exporterad_status',
                    'exporterad_tid','fel_vid_export','godkand_tid','granskning_id','id','inskickad_antal_forsok',
                    'inskickad_tid','pubkan_ais','pubkan_platsbanken','pubkan_platsjournalen','raderad','status',
                    'rekryteringsbehov_id','status','statusdatum','timestamp','version_major','version_minor']

for index,filename in enumerate(filenames):
    res = []
    print(filename)

    with open(filename) as f:
        data = json.load(f)

    nrFirst = 0
    nrSecond = 0
    nrThird = 0

    print('first-level fields')
    for d in data:
        for field in fields_to_remove:
            if field in d:
                del d[field]
                nrFirst+=1

    print('second-/third-level fields')
    for d in data:
        for subfield in subfields_to_remove:
            if len(subfield) == 2:
                if subfield[0] in d and subfield[1] in d[subfield[0]]:
                    del d[subfield[0]][subfield[1]]
                    nrSecond+=1
            elif len(subfield) == 3:
                if subfield[0] in d and subfield[1] in d[subfield[0]] and subfield[2] in d[subfield[0]][subfield[1]]:
                    del d[subfield[0]][subfield[1]][subfield[2]]
                    nrThird+=1

    print('first:',nrFirst)
    print('second:',nrSecond)
    print('third:',nrThird)

    print('saving',filenames_new[index])

    with open(filenames_new[index],'w') as f:
        json.dump(data,f)

print('end')