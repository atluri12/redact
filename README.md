# The  Redactor
The Redactor is a program for hiding sensitive information such as *Names*, and *places* from the public. The process of redacting is a time taking and expensive  process. In this project, a program to redact the sensitive information such as *Names*, *Genders*, *Addresses*, *Dates* and *Phone numbers*. The project is compatible with Python 3.7.2 and the packages used are *google.cloud* and *nltk*. These packages are used to perform natural language processing on the text extracted so as to identify the named-entities from the files and hide them.

### Natural Language Processing Packages
* #### google.cloud
    The packages *google.cloud* and *nltk* are used for performing Natural Language Processing. The *google.cloud* package is the google's own version for performing Natural Language Processing. The google.cloud.language package can be used for performing effective named-entity recognition. It is installed to the virtual environment of python using following command

    `pipenv install google.cloud`

    The language, enums and types packages present in the google.cloud are used as
    ```python
    import google.cloud
    from google.cloud import language
    from google.cloud import enums
    from google.cloud import types
    ```
    The language package is used to identify the entities in a document. This used *analyze_entities()* function to get the named-entitie present within the document. The enums and types packages are used to convert the data into a PLAIN_TEXT document, as the analyze_entities function accepts only a document as the parameter. The google.cloud is a Google NLP API and valid google console credentials are required to use this package. The *LanguageServiceClient()* is a function which is used to connect to the google server as a client.
* #### nltk
    The *nltk* package is the most used package for Natural Language Processing. In this project, the nltk package is used to perform sentance tokenization and find synonms of a given word using *wordnet* corpus. The nltk package can be installed in the virtual environment of python using the following command

    `pipenv install nltk`

    Then open the python environment and execute the following commands
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')
    ```
    The punkt package contains the function *sent_tokenize()* used for breaking the given text into sentances and the wordnet package contains the *synsets()* function for finding the synonms for a given word.

### redact.py
The redact.py file contains the python program for performing the redaction. This program contains the functions *redConcept()*, *redName()*, *redGender()*, *redPhone()*, *redAddress()* and *redDate()*.These functions are used to perform the redaction of concepts, names, genders, phone numbers, addresses and dates respectively.
* #### redConcept()
    The *redConcept()* function takes five arguments which are file, word and stats. The variable file represents the file name, word represents the word or the concept which needs to be redacted and the stats is a list containing the statistics of the redaction process. The wordnet.synsets() function from the wordnet package is used to find the synonms of the given word. 
    ```python
    synon = wordnet.synsets(word)
    ```
    The synonms of the word are matched with the sentences present within the text file and the sentences matched are redacted with a unicode full block character ('\u2588').
* #### redName()
    The *redName()* function takes four arguments which are file and stats. The variable file represents the  file name and stats is a list containing the statistics of the redaction process. In this function *google.cloud.language* package is used to perform named-entity identification. The data from the input file is converted into a PLAIN_TEXT document using the types and enums packages. This document is passed as an argument to *analyze_entities()* function as shown below
    ```python
    doc = types.Document(content = data, type = enums.Document.Type.PLAIN_TEXT)
    entity = client.analyze_entities(doc).entities
    ```
    The google.cloud.language package performs the entity recognition and stores the data in the form of a JSON file. This JSON data contains the information about each and every entity. The  *entity.type* is a value which defines the type of the entity. `entity.type = 1` represents that the entity is a PERSON. This JSON file contains the data about every mention of the entity with the file and the type of mention which is generally two types 'COMMON' and 'PROPER'. The 'PROPER' mention of a name is only considered for this project  to identify the names. The 'PROPER' mention is defined as `entity.mentions.type = 1`. All the names identified within this function are redacted.
* #### redGender()
    The *redGender()* function takes four arguments. The file represents the file name and stats represent the list containing the  statistics of the redaction process. In this function, the terms defining the gender of a person such as *'he, she, him, her, husband, wife'* are listed. This function finds all the occurances of these words listed using the regular expressions and they are redacted using the unicode full block character ('\u2588').

