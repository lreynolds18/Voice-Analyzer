import os
import re
import csv
import shutil
import seaborn
seaborn.set(style='ticks')
import numpy as np
import scipy
import mir_eval
import librosa

directory = "/Users/reyno392/Desktop/Programming/bigdataproject/data/"
path, dirs, files = os.walk(directory).next()
total = 0
t = 0 

def construct_header():
    header = ["Directory"]
    for i in range(40):
        header.append("mfcss" + str(i))
    for i in range(12):
        header.append("chroma" + str(i))
    for i in range(128):
        header.append("mel" + str(i))
    for i in range(7):
        header.append("contrast" + str(i))
    for i in range(6):
        header.append("tonnetz" + str(i))
    header.extend(["gender", "age", "dialect"])
    return header

def extract_labels(filename):
    # extract gender, age, and dialect from README file
    gender = ""
    age = ""
    dialect = ""
    fi = open(filename)
    for line in fi.readlines():
        line = line.strip()
        if re.match("[gG]ender", line):
            if re.search("[^(Fe)(fe)][mM]ale", line):
                gender = "Male"
            elif re.search("[fF]emale", line):
                gender = "Female"
        elif re.match("[aA]ge [rR]ange", line):
            if re.search("[yY]outh", line):
                age = "Youth"
            elif re.search("[aA]dult", line):
                age = "Adult"
            elif re.search("[sS]enior", line):
                age = "Senior"
            else:
                print(line.strip())
                print(di)
        elif re.match("[pP]ronunciation [dD]ialect", line):
            if re.search("[aA]merica", line) or re.search("[nN]ew [yY]ork", line) \
              or re.search("[wW]est", line) or re.search("[mM]id-[aA]tlantic", line) \
              or re.search("[cC]ali", line):
                dialect = "American"
            elif re.search("[eE]uropean", line) or re.search("[bB]ritish", line) \
              or re.search("[iI]rish", line) or re.search("[iI]talian", line) or \
              re.search("[fF]rance", line) or re.search("[eE]nglish [eE]nglish", line):
                dialect = "European"
            elif re.search("[cC]anad[(ian)a]", line):
                dialect = "Canadian"
            elif re.search("[iI]ndian", line):
                dialect = "Indian"
            elif re.search("[aA]frican", line):
                dialect = "African"
            elif re.search("[nN]ew [zZ]ealand", line) or re.search("Australian", line):
                dialect = "Australasia"
            elif re.search("[oO]ther", line) or re.search("[uU]nknown", line):
                dialect = "Other"
            else:
                print(line.strip())
                print(di)
    fi.close() 
    return gender, age, dialect

with open("output-final-2.csv", 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    # write header to csvfile
    writer.writerow(construct_header())

    # iterate through each subject's directory
    for di in dirs:
        temp = directory + di
        p, d, f = os.walk(temp + "/wav").next()
        total += int(len(f))
    
        gender, age, dialect = extract_labels(temp + "/etc/README")

        for wav in f:
            row = [di]
            wav_directory = temp + "/wav/" + wav  
            # uses default sample rate of 22050
            y, sr = librosa.load(wav_directory, sr=22050)
            spectrogram = np.abs(librosa.stft(y))
            melspec = librosa.feature.melspectrogram(y=y, sr=sr)
            stft = np.abs(librosa.stft(y))
            mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
            mel = np.mean(librosa.feature.melspectrogram(y, sr=sr).T, axis=0)
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T,axis=0)
            
            for i in range(mfccs.shape[0]):
                row.append(mfccs[i])
            for i in range(chroma.shape[0]):
                row.append(chroma[i])
            for i in range(mel.shape[0]):
                row.append(mel[i]) 
            for i in range(contrast.shape[0]):
                row.append(contrast[i]) 
            for i in range(tonnetz.shape[0]):
                row.append(tonnetz[i])
            
            row.extend([gender, age, dialect])
            writer.writerow(row)

print(t)
print(len(dirs))
print(total)
