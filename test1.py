import anonymization

anonymize = anonymization.anonymize_swe()
anonymize.initialize()

extraKeywords = [] # any extra keywords that will remove entire sentences (default: empty)
ignoredSentences = [] # any sentences forced to keep (default: empty)

#alltext = "Mitt namn är Johan Svensson. Du kan nå mig på 0702-123456."
with open('input.txt') as f:
    allText = f.read()

print('Input text:\n' + allText)

res = anonymize.anonymizeText(allText,extraKeywords,ignoredSentences)

output = res[0]
removedSentences = res[1]
removedCounts = res[2]

print('\n\nOutput text:\n' + output)
print('\n\nRemoved sentences:\n' + ''.join(removedSentences))
print('\n\nRemoval counts:\n' + str(removedCounts))

with open("output.txt", "w") as f:
    f.write(res[0])
with open("removedSentences.txt", "w") as f:
    f.write(''.join(removedSentences))
with open("removedCounts.txt", "w") as f:
    f.write(str(removedCounts))