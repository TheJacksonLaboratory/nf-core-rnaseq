# This script takes the output of processDatasets and makes a simpler file with just the contrasts we want
import os
import csv
from collections import defaultdict

infile = "covid.ingest.tsv"
if not os.path.exists(infile):
    raise ValueError("You need to run the script processDatasets.py first")

datasets = defaultdict(list)

cohort_index = 0 # global


def get_cohort_index():
    """
    Each cohort (comparison) gets its own number, from 1 to N
    :return:
    """
    global cohort_index
    cohort_index += 1
    return cohort_index


class Experiment:
    def __init__(self, srp, srr, categ):
        self.srp = srp
        self.srr = srr
        self.category = categ

    def get_category(self):
        return self.category

    def output_row(self, itr, item):
        return "{}\t{}\t{}\t{}\t{}".format(itr, self.srp, self.srr, self.category,  item)

    @classmethod
    def get_header(cls):
        fields = ['cohort', 'srp', 'srr', 'category','status']
        return "\t".join(fields)

def get_rows(lst, case_str, control_str):
    """
    A convenience function that returns rows that correspond to one case/control cohort
    :param lst:
    :param case_str:
    :param control_str:
    :return:
    """
    rows = []
    idx = get_cohort_index()
    for e in lst:
        cat = e.get_category()
        if cat == case_str:
            rows.append(e.output_row(idx, 'case'))
        elif cat == control_str:
            rows.append(e.output_row(idx, 'control'))
    if len(rows) == 0:
        raise ValueError("Could not get cohort data for {}/{}".format(case_str, control_str))
    return rows

def show_categories(lst):
    """
    A convenience method to list out all of the categories we want to us
    :param lst:
    :return:
    """
    s = set()
    for l in lst:
        cat = l.get_category()
        s.add(cat)
    for it in s:
        print(it)



def SRP230823(dct, writer):
    lst = dct['SRP230823']
    rows = get_rows(lst, 'H5N1.infected', 'mock')
    for r in rows:
        writer.write(r + "\n")


def SRP040070(dct, writer):
    lst = dct['SRP040070']
    # show_categories(lst)
    rows = []
    rows2 = get_rows(lst, 'MRC5lowMOI.SARS.n/a.24h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5HighMOI.SARS.n/a.24h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5lowMOI.SARS.n/a.48h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5HighMOI.SARS.n/a.48h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5lowMOI.MERS.n/a.24h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5HighMOI.MERS.n/a.24h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5lowMOI.MERS.n/a.48h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5HighMOI.MERS.n/a.48h', 'MRC5.MOCK.n/a.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.SARS.IFNbeta.24h', 'MRC5lowMOI.SARS.n/a.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.SARS.IFNbeta.48h', 'MRC5lowMOI.SARS.n/a.48h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.SARS.Gleevec.24h', 'MRC5lowMOI.SARS.n/a.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.SARS.Gleevec.48h', 'MRC5lowMOI.SARS.n/a.48h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.MERS.Gleevec.24h', 'MRC5HighMOI.MERS.n/a.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.MERS.Gleevec.48h','MRC5lowMOI.MERS.n/a.48h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.MERS.IFNbeta.24h', 'MRC5HighMOI.MERS.n/a.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'MRC5.MERS.IFNbeta.48h','MRC5lowMOI.MERS.n/a.48h')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + "\n")


def SRP076102(dct, writer):
    lst = dct['SRP076102']
    rows = []
    rows2 = get_rows(lst, 'fluA.2h', 'control')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'fluA.4h', 'control')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'fluA.8h', 'control')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + "\n")





def SRP091886(dct, writer):
    lst = dct['SRP091886']
    # show_categories(lst)
    rows = []
    rows2 = get_rows(lst, 'H1N1.03h', 'mock.03h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H1N1.06h', 'mock.06h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H1N1.12h', 'mock.12h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H1N1.18h', 'mock.18h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H3N2.03h', 'mock.03h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H3N2.06h', 'mock.06h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H3N2.12h', 'mock.12h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H3N2.18h', 'mock.18h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H5N1.03h', 'mock.03h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H5N1.06h', 'mock.06h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H5N1.12h', 'mock.12h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'H5N1.18h', 'mock.18h')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + '\n')


def SRP118721(dct, writer):
    lst = dct['SRP118721']
    # show_categories(lst)
    rows = []
    rows2 = get_rows(lst, 'infA.no.treatment', 'mock')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'infA.lariciresinol.low', 'infA.no.treatment')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'infA.lariciresinol.high', 'infA.no.treatment')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + '\n')


def SRP170549(dct, writer):
    lst = dct['SRP170549']
    # show_categories(lst)
    rows = []
    rows2 = get_rows(lst, 'MERS', 'mock')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'AM580', 'mock')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + '\n')


def SRP227272(dct, writer):
    lst = dct['SRP227272']
    # show_categories(lst)
    rows2 = get_rows(lst, 'MERS', 'mock')
    for r in rows2:
        writer.write(r + '\n')


def SRP254688(dct, writer):
    lst = dct['SRP254688']
    # show_categories(lst)
    rows = []
    rows2 = get_rows(lst, 'covid.sputum', 'covid.BAL')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'covid.sputum', 'covid.throatswap')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + '\n')


def SRP253951(dct, writer):
    lst = dct['SRP253951']
    # show_categories(lst)
    rows = []
    rows2 = get_rows(lst, 'A549.RSV.0h', 'A459.mock.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'A549.RSV.24h', 'A459.mock.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'A549.IAV.0h', 'A459.mock.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'A549.covid.0h', 'A459.mock.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'A549.covid.24h', 'A459.mock.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'calu-3.covid.24h', 'calu-3.mock.24h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'covid.lung.biopsy', 'healthy.lung.biopsy')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'NHBE.covid.0h', 'NHBE.mock.0h')
    rows.extend(rows2)
    rows2 = get_rows(lst, 'A549.covid.ACE2.24h', 'A549.mock.ACE2.24h')
    rows.extend(rows2)
    for r in rows:
        writer.write(r + '\n')


#########################################################################
##########  Main execution begins here ##################################
#########################################################################

with open(infile) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if len(row) != 13:
            raise ValueError("Expecting 13 fields")
        srp = row[0]
        srr = row[1]
        category = row[12]
        if category == 'n/a':
            continue
        datasets[srp].append(Experiment(srp, srr, category))

with open('case_control.tsv', 'wt') as f:
    f.write(Experiment.get_header() + "\n")
    SRP230823(datasets, f)
    SRP040070(datasets, f)
    SRP076102(datasets, f)
    SRP091886(datasets, f)
    SRP118721(datasets, f)
    SRP170549(datasets, f)
    SRP227272(datasets, f)
    SRP254688(datasets, f)
    SRP253951(datasets, f)
