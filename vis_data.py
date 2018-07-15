# data visualisation

import csv
import matplotlib as mpl
from os import system
import sys


mpl.rcParams['font.size'] = 12
resolution = 300 # dpi

import matplotlib.pyplot as plt
import os


class Component(object):

    def __init__(self, data):
        self.correct = int(data[0])
        if len(data) == 6:
            self.oneUpAP = int(data[1])
            self.oneUpML = int(data[2])
            self.oneDownAP = int(data[3])
            self.oneDownML = int(data[4])
            self.incorrect = int(data[5])

        elif len(data) == 4:
            self.oneUp = int(data[1])
            self.oneDown = int(data[2])
            self.incorrect = int(data[3])


class Surgeon(object):

    def __init__(self, line):
        self.initials = line[0]
        self.cases = int(line[1])
        self.correct = int(line[2])
        self.fracCorrect = self.correct / self.cases
        self.incorrect = self.cases - self.correct

        self.femur = Component(line[4:10])
        self.tibia = Component(line[10:16])
        self.patella = Component(line[16:20])


def import_data(filename):

    surgeons = []

    with open(filename) as f:
        i = 0
        for line in f:
            if i >= 1:
                data = line.split(',')
                surgeons.append(Surgeon(data))
            i += 1

    return {s.initials:s for s in surgeons}


def my_autopct(pct):
    return ('%.2f%%' % pct) if pct > 10 else ''


def plot_data(s, plotCategory='all'):

    titleFontSize = 20
    currentDir = os.path.dirname(os.path.realpath(__file__))
    figureDir = currentDir + '/figures'


    if plotCategory == 'all':
        labels = ['All Correct','Incorrect']
        values = [s.correct, s.incorrect]


        title = 'ALL IMPLANTS'



    elif plotCategory == 'femur':

        fem = s.femur

        labels = ['Correct Size', '1 Size Up (AP)', '1 Size Up (ML)',
                        '1 Size Down (AP)', '1 Size Down (ML)', 'Incorrect']
        values = [fem.correct, fem.oneUpAP, fem.oneUpML,
                        fem.oneDownAP, fem.oneDownML, fem.incorrect]
        title = 'FEMUR COMPONENT'

    elif plotCategory == 'tibia':

        tib = s.tibia

        labels = ['Correct Size', '1 Size Up (AP)', '1 Size Up (ML)',
                        '1 Size Down (AP)', '1 Size Down (ML)', 'Incorrect']
        values = [tib.correct, tib.oneUpAP, tib.oneUpML,
                        tib.oneDownAP, tib.oneDownML, tib.incorrect]
        title = 'TIBIA COMPONENT'

    elif plotCategory == 'patella':

        pat = s.patella

        labels = ['Correct Size', '1 Size Up', '1 Size Down', 'Incorrect']
        values = [pat.correct, pat.oneUp, pat.oneDown, pat.incorrect]
        title = 'PATELLA COMPONENT'



    # remove empty categories
    i = 0
    removeEmpty = True
    while removeEmpty and i < len(values):
        if values[i] == 0:
            values.pop(i)
            labels.pop(i)
        else:
            i += 1



    fig1, ax1 = plt.subplots()
    patches = ax1.pie(values, labels=labels,
                shadow=False, startangle=90, autopct=my_autopct)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.set_cmap('hot')

    plt.title(title, fontSize=titleFontSize, fontweight="bold")

    #plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.1, 1.),
    #       fontsize=8)


    fname = '/' + s.initials + '_' + plotCategory + '.png'
    fullPath = figureDir + fname
    fig1.savefig(fname=fullPath,format='png',bbox_inches='tight',
                pad_inches=0.1, transparent=True, dpi=resolution)
    plt.close()


def plot_text(s):

    fig = plt.figure()
    plt.axis('off')

    text = 'All correct: {:.1f}%'.format(s.fracCorrect*100)

    renderer = fig.canvas.get_renderer()
    t = plt.text(0.001, 0.001, text, fontsize=32)
    wext = t.get_window_extent(renderer=renderer)

    fig.set_size_inches(wext.width / 65, wext.height / 80, forward=True)


    #plt.show()

    currentDir = os.path.dirname(os.path.realpath(__file__))
    figureDir = currentDir + '/figures'
    fname = '/' + s.initials + '_' + 'text.png'
    fullPath = figureDir + fname
    fig.savefig(fname=fullPath,format='png',bbox_inches='tight',
                pad_inches=0, transparent=True, dpi=resolution)
    plt.close()


def generate_latex(s, file):

    lineRep = ['\\newcommand{\\var}{' + s.initials + '}',
            '\\newcommand{\\varx}{figures/' + s.initials + '_text.png}',
            '\\newcommand{\\vara}{figures/' + s.initials + '_femur.png}',
            '\\newcommand{\\varb}{figures/' + s.initials + '_tibia.png}',
            '\\newcommand{\\varc}{figures/' + s.initials + '_patella.png}']

    lineNumber = 1
    output = []
    for L in open(file):
        line = L.strip()

        if lineNumber >= 10 and lineNumber <= 14:
            i = lineNumber-10
            output.append(lineRep[i])

        else:
            output.append(line)

        lineNumber += 1

    fname = 'slide_' + s.initials
    fname_ext = fname + '.tex'

    with open(fname_ext, 'wt') as outF :
        for line in output :
            outF.write(line + '\n')


    system('pdflatex ' + fname_ext)


    for ext in ['.snm', '.toc', '.out', '.nav', '.aux', '.log']:
        system('rm ' + fname + ext)

    return fname_ext

def process_data(filename):
    surgeons = import_data(filename)
    filenames = []

    n, length = 1, len(surgeons)
    for s in surgeons.values():
        #plot_data(s, 'all')

        plot_data(s, 'femur')
        plot_data(s, 'tibia')
        plot_data(s, 'patella')
        print("DONE {}/{} surgeons".format(n, length))
        n += 1
        plot_text(s)

        file = 'slide-generator.txt'
        fname = generate_latex(s, file)
        filenames.append(fname)

    return filenames


if __name__ == '__main__':

    filename = 'out.csv'
    process_data(filename)
