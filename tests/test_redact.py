import pytest
import google.cloud
from google.cloud import language
from project1 import redact

testfile = '/projects/cs5293sp19-project1/docs/test_sample.txt'
destination = '/projects/cs5293sp19-project1/docs'

def test_redConcept():
    stats = []
    stats_values = []
    word = 'man'
    cfile = redact.redConcept(testfile, word, stats, stats_values, destination)
    totalstring = ''.join(stats_values[0])
    length = len(totalstring)
    with open(cfile, 'r') as rf:
        data = rf.read()
    count = data.count('\u2588')
    assert count == length

def test_redName():
    stats = []
    stats_values = []
    nfile = redact.redName(testfile, stats, stats_values, destination)
    assert nfile

def test_redGender():
    stats = []
    stats_values = []
    gfile = redact.redGender(testfile, stats, stats_values, destination)
    assert gfile

def test_redAddress():
    stats = []
    stats_values = []
    afile = redact.redAddress(testfile, stats, stats_values, destination)
    assert afile

def test_redPhone():
    stats = []
    stats_values = []
    pfile = redact.redPhone(testfile, stats, stats_values, destination)
    assert pfile

def test_redDate():
    stats = []
    stats_values = []
    dfile = redact.redDate(testfile, stats, stats_values, destination)
    assert dfile
