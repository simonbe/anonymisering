# simple anonymization
# - removes entire sentences which contain phone numbers, email adresses, names or other manually defined keywords
# - uses nltk for Swedish tokenization
# - files with most common Swedish names in 'names' directory

import re
import csv
import nltk.data

class anonymize_swe:

    def initialize(self):
        # load names
        names_m = self.__load_csv('names/names_m.csv')
        names_f = self.__load_csv('names/names_f.csv')
        names_efternamn = self.__load_csv('names/names_efternamn100.csv')

        self._all_names = []
        self._all_names.extend(names_m)
        self._all_names.extend(names_f)
        self._all_names.extend(names_efternamn)

        self._tokenizer = nltk.data.load('tokenizers/punkt/swedish.pickle')

        # by default not using advanced regex for phone numbers - only removing any long numbers
        self._regexPhoneNumberComplex = re.compile(r'^([+]46)\s*(7[0236])\s*(\d{4})\s*(\d{3})$')
        self._regexpPhoneNumberSimple = re.compile(r'[0-9]{6,7}')


    def __containsPhoneNumber(self,s, useSimpleVersion = True):

        if useSimpleVersion:
            if self._regexpPhoneNumberSimple.search(s.replace(' ','')) is not None:
                return True
        else:
            if self._regexpPhoneNumberComplex.search(s.replace(' ','')) is not None:
                return True
        
        return False

    def __load_csv(self,filename):
        data = []
        with open(filename, 'rt') as csvfile:
            readr = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in readr:
                data.append(row[0])

        return data

    def textRemoveSentences(self,text,keywords,ignored):
        # returns new text and removed sentences
        removedSentences = []

        # counts
        removedTypes = { 'Name&Email&Phone': 0, 'Name&Email': 0, 'Name&Phone':0,'Name':0,'EmailPhone':0,'Email':0,'Phone':0 }

        finalText = ''

        splitted = []

        #newText = text.replace('   ','\n') # special case
        sections = text.split('\n')

        for section in sections:
            splitted = self._tokenizer.tokenize(section)

            for s in splitted:
                containsEmail = False
                containsPhone = False
                containsName = False
                containsKeyword = False

                if s not in ignored:
                    words = s.split()
                    doNotUse = False

                    # check if contains any keyword (default this only checks for names)
                    for k in keywords:
                        if k in words:
                            doNotUse = True
                            containsName = True

                            # but skip if the word is first in sentence ('Dina kompetenser ar...') - this will still get found by second word ('Dina Svensson är ...')
                            if words[0] == k:
                                doNotUse = False;

                    # check if contains e-mail
                    if '@' in s:
                        doNotUse = True
                        containsEmail = True

                    # check if contains phone number
                    if self.__containsPhoneNumber(s):
                        doNotUse = True
                        containsPhone = True

                    # update counts
                    if doNotUse == True:
                        removedSentences.append(s)
                        if containsEmail == True and containsPhone == True and containsName == True:
                            removedTypes['Name&Email&Phone'] = removedTypes['Name&Email&Phone'] + 1
                        elif containsName == True and containsEmail == True:
                            removedTypes['Name&Email'] = removedTypes['Name&Email'] + 1
                        elif containsName == True and containsPhone == True:
                            removedTypes['Name&Phone'] = removedTypes['Name&Phone'] + 1
                        elif containsName == True:
                            removedTypes['Name'] = removedTypes['Name'] + 1
                        elif containsEmail == True and containsPhone == True:
                            removedTypes['Email&Phone'] = removedTypes['Email&Phone'] + 1
                        elif containsEmail == True:
                            removedTypes['Email'] = removedTypes['Email'] + 1
                        elif containsPhone == True:
                            removedTypes['Phone'] = removedTypes['Phone'] + 1
                    else:
                        finalText = finalText + s
                else: # do not check this sentence
                    finalText = finalText + s

            if section != sections[len(sections)-1]:
                finalText = finalText + '   '

        return [finalText, removedSentences, removedTypes]

    def anonymizeText(self, str, extraKeywords = [], ignoredSentences = []):
        newStr = ""

        allKeywords = []
        allKeywords.extend(self._all_names) # names by default
        allKeywords.extend(extraKeywords)

        res = self.textRemoveSentences(str,allKeywords, ignoredSentences)
        print(res)

        return res
