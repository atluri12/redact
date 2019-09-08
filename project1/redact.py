import google.cloud
import re
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet
import glob
import sys
import os

client = language.LanguageServiceClient()

def redConcept(file, word, stats, stats_values, directory):
    with open(file, 'r') as rf:
        data = rf.read()
    synon = wordnet.synsets(word)
    synonms = []
    for i in synon:
        a = i.lemmas()
        for i in a:
            synonms.append(i.name())
    synonms = set(synonms)
    xdata = sent_tokenize(data)
    delete = []
    for term in synonms:
        for line in xdata:
            if(term in line and line not in delete):
                delete.append(line)
    for token in delete:
        block = len(token)
        data = data.replace(token, '\u2588'*block)
    if(os.path.exists(directory) == False):
        os.system('mkdir ' + directory)
    file = file.split('.')[0]
    if('/' in  file):
        file = file.split('/')[-1]
    filename = directory + '/' + file + '.redacted.txt'
    stats_values.append(delete)
    with open(filename, 'w+') as wf:
        wf.write(data)
    stats.append(len(delete))
    return filename

def redName(file, stats, stats_values, directory):
    with open(file, 'r') as rf:
        data = rf.read()
    doc = types.Document(content = data, type = enums.Document.Type.PLAIN_TEXT)
    entity = client.analyze_entities(doc).entities
    name = []
    for each in entity:
        if(each.type == 1): #PERSON = 1
            for mention in each.mentions:
                if(mention.text.content not in name and mention.type == 1):
                    ename = mention.text.content
                    if('\n' in ename):
                        ename = (re.sub('[\n].*', '', ename)).strip()
                    name.append(ename)
    extra = ['university', 'county', 'college', 'state']
    delete = []
    for i in name:
        if(any((j in i.lower() for j in extra))):
            delete.append(i)
    for i in delete:
        name.remove(i)
    for ent in name:
        block = len(ent)
        data = data.replace(ent, '\u2588'*block)
    if(os.path.exists(directory) == False):
        os.system('mkdir ' + directory)
    file = file.split('.')[0]
    if('/' in  file):
        file = file.split('/')[-1]
    filename = directory + '/' + file + '.redacted.txt'
    stats_values.append(name)
    with open(filename, 'w+') as wf:
        wf.write(data)
    stats.append(len(name))
    return filename

def redPhone(file, stats, stats_values, directory):
    with open(file, 'r') as rf:
        data = rf.read()
    phone = re.compile(r'(\+\d{1,6})? (\s|-)? (\(?\d{3} \)?) (\s|-)? (\(?\d{3} \)?) (\s|-)? (\(?\d{4} \)?)',re.VERBOSE)
    aPhone = phone.findall(data)
    allPhone = []
    for ph in aPhone:
        ph = list(filter(None, ph))
        if(ph[0] == ' '):
            del ph[0]
        ph = ''.join(ph)
        allPhone.append(ph)
        block = len(ph)
        data = data.replace(ph, '\u2588'*block)
    if(os.path.exists(directory) == False):
        os.system('mkdir ' + directory)
    file = file.split('.')[0]
    if('/' in  file):
        file = file.split('/')[-1]
    filename = directory + '/' + file + '.redacted.txt'
    with open(file, 'w+') as wf:
        wf.write(data)
    stats.append(len(allPhone))
    stats_values.append(allPhone)
    return filename

def redAddress(file, stats, stats_values, directory):
    with open(file, 'r') as rf:
        data = rf.read()
    add = re.compile(r'(\d{1,4}\s\w+\s\w+\,) (\s\w+\s\d+\,)? (\s\w+) (\s\w+)? (\,\s\w+\,\s\d{5})', re.VERBOSE)
    a = add.findall(data)
    address = []
    for line in a:
        line = list(filter(None, line))
        line = ''.join(line)
        block = len(line)
        address.append(line)
    doc = types.Document(content = data, type = enums.Document.Type.PLAIN_TEXT)
    entity = client.analyze_entities(doc).entities
    for each in entity:
        if(each.type == 2):
            for mention in each.mentions:
                if(mention.text.content not in address and mention.type == 1):
                    location = mention.text.content
                    if('\n' in location):
                        location = (re.sub('[\n].*', '', location)).strip()
                    address.append(location)
    for ent in address:
        block = len(ent)
        data = data.replace(ent, '\u2588'*block)
    if(os.path.exists(directory) == False):
        os.system('mkdir ' + directory)
    file = file.split('.')[0]
    if('/' in  file):
        file = file.split('/')[-1]
    filename = directory + '/' + file + '.redacted.txt'
    with open(filename, 'w+') as wf:
        wf.write(data)
    stats.append(len(address))
    stats_values.append(address)
    return filename

def redDate(file, stats, stats_values, directory):
    with open(file, 'r') as rf:
        data = rf.read()
    date = []
    years = re.compile(r'([0-2]{1}[0-9]{3})', re.VERBOSE)
    month = '(January|February|March|April|May|June|July|August|September|October|November|December)'
    time = re.compile('(' + month + '\s[0-3]{1}?[0-9]{1}?) (\,\s)? (\d{4})?', re.VERBOSE)
    atime = time.findall(data)
    for d in atime:
        d = list(filter(None, d))
        del d[1]
        d = ''.join(d)
        block = len(d)
        date.append(d)
        data = data.replace(d, '\u2588'*block)
    mtime = re.findall(month, data, re.IGNORECASE)
    ytime = re.findall(years, data)
    for y in ytime:
        date.append(y)
        data = data.replace(y, '\u2588'*4)
    for m in mtime:
        block = len(m)
        date.append(m)
        data = data.replace(m, '\u2588'*4)
    if(os.path.exists(directory) == False):
        os.system('mkdir ' + directory)
    file = file.split('.')[0]
    if('/' in  file):
        file = file.split('/')[-1]
    filename = directory + '/' + file + '.redacted.txt'
    with open(filename, 'w+') as wf:
        wf.write(data)
    stats.append(len(date))
    stats_values.append(date)
    return filename

def redGender(file, stats, stats_values, directory):
    with open(file, 'r') as rf:
        data = rf.read()
    example = ['He', 'She', 'Himself', 'Herself', 'Male', 'Female', 'Him', 'Her', 'His', 'Hisself', 'Man', 'Woman', 'Men', 'Women', 'Husband', 'Wife', 'Gay']
    matchGender = []
    for gender in example:
        block = len(gender)
        allGender = re.findall('\\b' + gender.lower() + '\\b', data, re.IGNORECASE)
        matchGender.extend(allGender)
        capital = re.compile('\\b' + gender + '\\b')
        data = capital.sub('\u2588'*block, data)
        low = re.compile('\\b' + gender.lower() + '\\b')
        data = low.sub('\u2588'*block, data)
    if(os.path.exists(directory) == False):
        os.system('mkdir ' + directory)
    file = file.split('.')[0]
    if('/' in  file):
        file = file.split('/')[-1]
    filename = directory + '/' + file + '.redacted.txt'
    for every in stats_values:
        for token in every:
            block = len(token)
            data = data.replace(token, '\u2588'*block)
    with open(filename, 'w+') as wf:
        wf.write(data)
    stats.append(len(matchGender))
    stats_values.append(matchGender)
    return filename

def redStats(fileList, stats, stats_values, filename):
    data = ''
    for index in range(len(stats_values)):
        data = 'filename: ' + fileList[index] + '\n'
        for every in stats_values[index]:
            data = data + ','.join(every) + '\n'
    filename = filename.split('.')[0]
    with open(filename, 'w+') as wf:
        wf.write(data)
    print(data)
    return filename

if __name__ == '__main__':
    parameters = len(sys.argv)
    fileList = []
    nametoken, datetoken, addresstoken, phonetoken, gendertoken = 0, 0, 0, 0, 0
    concepttoken, stattoken = 0, 0
    for token in range(parameters):
        sys.argv[token] = sys.argv[token].strip()
        if(sys.argv[token] == '--input'):
            fileList.extend(glob.glob(sys.argv[token+1], recursive = True))
        elif(sys.argv[token] == '--output'):
            directory = sys.argv[token+1].rstrip('/')
        elif(sys.argv[token] == '--names'):
            nametoken = 1
        elif(sys.argv[token] == '--dates'):
            datetoken = 1
        elif(sys.argv[token] == '--addresses'):
            addresstoken = 1
        elif(sys.argv[token] == '--phones'):
            phonetoken = 1
        elif(sys.argv[token] == '--genders'):
            gendertoken = 1
        elif(sys.argv[token] == '--concept'):
            concepttoken = 1
            conceptword = sys.argv[token+1]
        elif(sys.argv[token] == '--stats'):
            stattoken = 1
            statname = sys.argv[token+1]
    stats = [[] for i in range(len(fileList))]
    stats_values = [[] for i in range(len(fileList))]
    for index in range(len(fileList)):
        if(concepttoken == 1):
            conceptdata = redConcept(fileList[index], conceptword, stats[index], stats_values[index], directory)
        if(nametoken == 1):
            namedata = redName(fileList[index], stats[index], stats_values[index], directory)
        if(phonetoken == 1):
            phonedata = redPhone(fileList[index], stats[index], stats_values[index], directory)
        if(addresstoken == 1):
            addressdata = redAddress(fileList[index], stats[index], stats_values[index], directory)
        if(datetoken == 1):
            datedata = redDate(fileList[index], stats[index], stats_values[index], directory)
        with open(fileList[index], 'r') as rf:
            data = rf.read()
        for every in stats_values[index]:
            for token in every:
                block = len(token)
                data = data.replace(token, '\u2588'*block)
        if(os.path.exists(directory) == False):
            os.system('mkdir ' + directory)
        filename = fileList[index].split('.')[0]
        if('/' in  filename):
            filename = filename.split('/')[-1]
        filename = directory + '/' + filename + '.redacted.txt'
        with open(filename, 'w+') as wf:
            wf.write(data)
        if(gendertoken == 1):
            genderdata = redGender(fileList[index], stats[index], stats_values[index], directory)
    if(stattoken == 1):
        statdata = redStats(fileList, stats, stats_values, statname)
