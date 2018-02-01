#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''textgrid_distinction_conversion.py: Uses audiolabel to go through all of the aligned .TextGrid files in a directory and replace S on the phone tier with Z where it is appropriate in Castilian Spanish, based on orthography on the corresponding word tier.

The script takes two arguments: the directory containing the text grids and the directory for the output files. Note that this script assumes that your tiers are in order with phone tier first, then word tier, then phone tier, then word tier, and so on, with no extra tiers, and that words are in uppercase - standard output format for the FASE aligner.'''

#__author__ = "Duna Gylfadottir"



import os
import re
import codecs
import audiolabel
import glob
import sys
from audiolabel import LabelManager
import numpy as np


def replaceThetas(phoneTier, wordTier):
    '''Loops through words in a tier, finds words that have ce, ci, or z in them, finds all letters that will correspond to an S in Latin American transcription, gets positions of the ones that should be corrected to Z, replaces the corresponding S phones on the phone tier.'''
    for interval in wordTier:
        word = interval.text
        if containsTheta(word):
            instances = re.findall('X|S|Z|CE|CI|C\xc9|C\xcd', word)
            to_replace = np.where([x in ['Z','CE','CI','C\xc9','C\xcd'] for x in instances])[0]
            count = -1
            phones = phoneTier.tslice(interval.t1, interval.t2, lstrip=True, rstrip=True)
            phoneList = [phone.text for phone in phones]
            if phoneList.count('s') != len(instances):
                print("Unexpected number of S in " + word)
            else:
                for idx, phone in enumerate(phones):
                    if phone.text == 's':
                        count += 1
                        if count in to_replace:
                            phone.text = 'z'
                            continue


def containsTheta(word):
    return len(re.findall('Z|CE|CI|C\xc9|C\xcd', word)) >0


def getTextGridFiles(directory):
    '''Returns full path of all .TextGrid files in the directory'''
    tgs = glob.glob(os.path.join(directory,"*.TextGrid"))
    return tgs



def newTgFromLabelManager(lm, new_name, directory):
    '''takes a label manager object, a new file basename, and an output directory and calls as_string to create a new TextGrid file'''
    outfile = os.path.join(directory, new_name)
    with codecs.open(outfile,'w','utf-8') as o:
        o.write(lm.as_string('praat_short'))

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    indirectory = sys.argv[1]
    outdirectory = sys.argv[2]
    tgs = getTextGridFiles(indirectory)
    for tg in tgs:
        current_name = os.path.basename(tg)
        new_name = os.path.splitext(current_name)[0] + "_z" + ".TextGrid"
        lm = LabelManager(tg, 'praat', codec = 'utf-8')
        for ix in range(0,len(lm.names),2):
            replaceThetas(lm.tier(ix), lm.tier(ix+1))
        ensure_dir(outdirectory)
        newTgFromLabelManager(lm, new_name, outdirectory)

        
