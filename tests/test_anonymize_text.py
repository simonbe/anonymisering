import os
import sys
import pytest
# import requests
import anonymization

anonymize = anonymization.anonymize_swe()
anonymize.initialize()


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_split_sentences_punkt():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening med punkt och mailadress adam@svensson.se. En andra mening med punkt och mailadress adam@svensson.se.'''
    res = anonymize.anonymizeText(input_text, [], [])
    removedSentences = res[1]

    assert len(removedSentences) == 2


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_split_sentences_newline():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan punkt med radbrytning på slutet och mailadress adam@svensson.se
                    En andra mening utan punkt med radbrytning på slutet och mailadress adam@svensson.se
                    En tredje mening utan punkt och utan radbrytning på slutet och mailadress adam@svensson.se'''
    res = anonymize.anonymizeText(input_text, [], [])

    removedSentences = res[1]

    assert len(removedSentences) == 3


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_split_sentences_exclamation_mark():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening med utropstecken på slutet och mailadress adam@svensson.se! En andra mening utan punkt och mailadress adam@svensson.se'''
    res = anonymize.anonymizeText(input_text, [], [])

    removedSentences = res[1]

    assert len(removedSentences) == 2


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_name():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan namn. En andra mening med namnet Bosse Bengtsson. En sista mening utan namn.'''
    res = anonymize.anonymizeText(input_text, [], [])

    output = res[0]
    removedSentences = res[1]

    assert len(removedSentences) == 1
    assert 'Bosse' in removedSentences[0]
    assert 'första' in output
    assert 'sista' in output

# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_phonenumber():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan telefonnummer. En andra mening med telefonnummer 0702-123456. En sista mening utan telefonnummer.'''
    res = anonymize.anonymizeText(input_text, [], [])

    output = res[0]
    removedSentences = res[1]

    assert len(removedSentences) == 1
    assert '0702-123456' in removedSentences[0]
    assert 'första' in output
    assert 'sista' in output


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_email():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan epost.
    En andra mening med epost bosse1.bengtsson@test.se.
    En andra mening med epost bosse2@test.se.
    En sista mening utan epost.'''
    res = anonymize.anonymizeText(input_text, [], [])

    output = res[0]
    removedSentences = res[1]

    assert len(removedSentences) == 2
    assert 'bosse1' in removedSentences[0]
    assert 'bosse2' in removedSentences[1]
    assert 'första' in output
    assert 'sista' in output


# def get_all_top_level_domain_names():
#     tld_url = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'
#     requests.get(tld_url)
#     with requests.get(tld_url) as response:
#         response.raise_for_status()
#         tlds_raw = response.text.split('\n')[1:]
#         tlds = [tld.lower() for tld in tlds_raw if tld]
#
#     return tlds
#
# @pytest.mark.skip(reason="Temporarily disabled")
# @pytest.mark.parametrize("tld", get_all_top_level_domain_names())
# @pytest.mark.unit
# def test_anonymize_email_all_top_level_domains(tld):
#     print('\n============================', sys._getframe().f_code.co_name, '============================')
#     input_text = '''En första mening utan epost.
#     En andra mening med epost bosse.bengtsson@test123.%s.
#     En sista mening utan epost.''' % tld
#     res = anonymize.anonymizeText(input_text, [], [])
#
#     output = res[0]
#     removedSentences = res[1]
#
#     assert len(removedSentences) == 1
#     assert 'bosse' in removedSentences[0]
#     assert 'första' in output
#     assert 'sista' in output



# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_all_types():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''Start rad 1. Lars Magnus Ericsson var son till hemmansägaren Erik Ericsson (18041858) från Vegerbol i Värmskog. Slut rad 1.
                    Start rad 2. Hej! Mitt namn är Adam Svensson. Min epost-adress är adam@svensson.se. Du kan nå mig på telefon 0702-123456. Slut rad 2.
                    Start rad 3. Var god kontakta Abbe på lagret. Eller Ibrahim på ibra@sweco.se. Slut rad 3.'''

    extraKeywords = []
    ignoredSentences = []

    res = anonymize.anonymizeText(input_text, extraKeywords, ignoredSentences)

    output = res[0]
    removedSentences = '\n'.join(res[1])
    removedCounts = res[2]

    print('\n\nOutput text:\n' + output)
    print('\n\nRemoved sentences:\n' + removedSentences)
    print('\n\nRemoval counts:\n' + str(removedCounts))

    assert 'Lars Magnus Ericsson' in removedSentences
    assert 'Adam Svensson' in removedSentences
    assert 'adam@svensson.se' in removedSentences
    assert '0702-123456' in removedSentences
    assert 'Abbe' in removedSentences
    assert 'ibra@sweco.se' in removedSentences

# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_with_extra_keywords():
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan extra keywords.
                    En andra mening med extra keywords, facklig företrädare hos oss är XYZ.
                    En tredje mening med extra keywords, fackliga företrädare hos oss är XYZ och ZYX.
                    En sista mening utan extra keywords.'''

    extraKeywords = ['facklig företrädare', 'fackliga företrädare']
    ignoredSentences = []

    res = anonymize.anonymizeText(input_text, extraKeywords, ignoredSentences)

    removedSentences = res[1]

    assert len(removedSentences) == 2
    assert extraKeywords[0] in removedSentences[0]
    assert extraKeywords[1] in removedSentences[1]


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__), '-svv', '-ra', '-m unit'])
