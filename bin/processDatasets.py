# purpose of this script -- organize the information in the various datasets and output a table with factors
import re
import csv
from collections import defaultdict


MULTIPLE_WHITESPACE = re.compile(r"\s+")
NO_CATEGORY = 'n/a'


class SraExperiment:
    def __init__(self, srp, run, assay_type, spotlen, bases, cellline, experiment,  infection, librarylayout, treatment, time, pmid):
        self.srp = srp
        self.run = run
        self.assay_type = assay_type
        self.spotlen = spotlen
        self.bases = bases
        self.cellline = cellline
        self.experiment = experiment
        self.infection = infection
        self.librarylayout = librarylayout
        self.treatment = treatment
        self.time = time
        self.pmid = pmid
        self.category = NO_CATEGORY

    def set_category2(self, cell_line, infection, category):
        if cell_line == self.cellline and infection == self.infection:
            self.category = category

    def set_category(self, cat):
        self.category = cat

    def output_row(self):
        outfields = [self.srp, self.run, self.assay_type, self.spotlen, self.bases,self.cellline,
                     self.experiment, self.infection, self.librarylayout, self.treatment, self.time, self.pmid, self.category]
        return "\t".join(outfields)

    def get_infection(self):
        return self.infection

    def set_infection(self, infect):
        self.infection = infect

    def get_experiment(self):
        return self.experiment

    def set_experiment(self, exp):
        self.experiment = exp

    def get_assaytype(self):
        return self.assay_type

    def set_time(self, time):
        self.time = time

    def get_run(self):
        return self.run

    def get_treatment(self):
        return self.treatment

    def get_cellline(self):
        return self.cellline

    def set_cellline(self, cl):
        self.cellline = cl

    @classmethod
    def header(cls):
        return "\t".join(['srp', 'run', 'assay_type', 'spotlen', 'bases', 'cellline',
                          'experiment', 'infection', 'library','treatment', 'time', 'pmid','category'])



def process_sra_runtable(path, ind, srp, pmid):
    '''
    Unfortunately, the indices are not consistent across datasets
    ind has the indices for the current dataset of these fields
    [0] Run
    [1] Assay Type
    [2] AvgSpotLen
    [3] Bases
    [4] Cell_Line
    [5] Experiment
    [6] infection
    [7] layout
    optionally [8] treatment
    optionally [9] time of treatment
    -- optionally, a seventh field for treatment can be added
    -- The script figures this out according to the length of ind
    :param path: path to one of the SraRunTable files
    :return:
    '''
    experiments = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader) # skip header
        for fields in reader:
            run = fields[ind[0]]
            assay_type = fields[ind[1]]
            spotlen = fields[ind[2]]
            bases = fields[ind[3]]
            cellline = fields[ind[4]]
            experiment = fields[ind[5]]
            infection = fields[ind[6]]
            layout = fields[ind[7]]
            if len(ind) < 9:
                treatment = 'n/a'
            else:
                treatment = fields[ind[8]]
            if len(ind) < 10:
                time = 'n/a'
            else:
                time = fields[ind[9]]
            exp = SraExperiment(srp, run, assay_type, spotlen, bases, cellline, experiment, infection,layout, treatment, time, pmid)
            experiments.append(exp)
    return experiments






def process_SRP230823():
    '''
    DONE
    PMID: 31776276
    Viral Determinants in H5N1 Influenza A Virus Enable Productive Infection of HeLa Cells
    Here, we tested the growth of influenza A virus in a subset of human cell lines and found
    that abortive replication of H1N1 viruses in HeLa cells can be circumvented upon the introduction
    of H5N1 virus HA and NP. Overall, this work leverages the genetic diversity of multiple human cell
    lines to highlight viral determinants that could contribute to H5N1 virus pathogenesis and tropism.
    OUR PLAN -- Just analyze H5N1
    :return:
    '''
    runtable = "../data/SRP230823_SraRunTable.txt"
    ind = [0, 1, 2, 3, 7, 13, 15, 17]
    experiments = process_sra_runtable(runtable, ind, 'SRP230823', 'PMID:31776276')
    print(SraExperiment.header())
    for e in experiments:
        e.set_category2('HeLa', 'H5N1 HALo', 'H5N1.infected')
        e.set_category2('HeLa', 'mock', 'mock')
        # do not analyze the H1N1
        # e.set_category('HeLa', 'H1N1 WSN', 'H1N1.WSN')
    return experiments




def explore_indices(path):
    '''
    Used to figure out which indices we want. Basically, show the fields with one example
    Use this when we are starting to make the function for the dataset. Does not need to
    be used for the final parsing -- we want the indices for the following
    [0] Run
    [1] Assay Type
    [2] AvgSpotLen
    [3] Bases
    [4] Cell_Line
    [5] Experiment
    [6] infection
    [7] treatment
    :param path:
    :return:
    '''
    headers = []
    examples = []
    examples2 = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)
        line = next(reader)
        line2 = next(reader)
        if len(header) != len(line):
            # should never happen
            raise ValueError("Lengths of line and header do not match!")
        for i in range(len(line)):
            print("[%d] %s: %s // %s" % (i, header[i], line[i], line2[i]))

def process_SRP040070():
    """
    DONE
    We will use the EMC/2012 strain of the novel beta Coronavirus called Middle East Respiratory Syndrome Coronavirus
    (MERS-CoV). It was initially passaged on Vero E6 cells in Saudi Arabia before being sequenced at the Erasmus Medical
    College in Rotterdam, Netherlands by Dr Ron Fouchier.
    :return:
    """
    runtable = '../data/SRP040070_SraRunTable.txt'
    explore_indices(runtable)
    srp = 'SRP040070'
    pmid = 'n/a'
    # requires special processing
    experiments = []
    print(SraExperiment.header())
    with open(runtable) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # skip header
        for fields in reader:
            run = fields[0]
            assay_type = fields[1]
            spotlen = fields[2]
            bases = fields[3]
            librarylayout = fields[15]
            str = fields[21]
            experiment = str
            if str.startswith('VMERS_'):
                str = str[6:]
            A = str.split("-")
            infection = A[0]
            cellline = A[1]
            if '24hr' in str:
                time = '24h'
            elif '48hr' in str:
                time = '48h'
            else:
                time = '0h' # assume no time course
            if 'Gleevec' in str:
                treatment = 'Gleevec'
            elif 'IFNbeta' in str:
                treatment = 'IFNbeta'
            else:
                treatment = 'n/a'
            srae = SraExperiment(srp, run, assay_type, spotlen, bases, cellline, experiment, infection, librarylayout, treatment, time,
            pmid)
            experiments.append(srae)
            print(srae.output_row())
    for e in experiments:
        categ = "{}.{}.{}.{}".format(e.cellline,e.infection, e.treatment, e.time)
        e.set_category(categ)
        print(e.output_row())
    return experiments



def process_SRP056612():
    '''
    DONE
    Gene expression profile in Calu-3 cells infected with MERS-CoV or SARS-CoV

    :return:
    '''
    runtable = "../data/SRP056612_SraRunTable.txt"
    gsm = "../data/SRP056612_GSM_expanded.txt"
    # requires special treatment
    srp = 'SRP056612'
    pmid = 'n/a'
    assay_type = 'RNA-Seq'
    cellline = 'calu-3'
    librarylayout = 'PAIRED'
    spotlen = "202"
    bases = 'see.run.table'
    treatment = 'n/a'
    experiment = 'n/a'
    experiments = []
    with open(gsm) as f:
        next(f)
        for line in f:
            z = re.search(r"(SRS\d+)", line)
            if z:
                run = z.group()
            else:
                raise ValueError("Could not find SRS")
            if "SARS infection" in line:
                infection = 'SARS'
            elif "MERS-CoV infection" in line:
                infection = 'MERS-CoV'
            else:
                raise TypeError("Could not find infection")
            y = re.search(r"at (\d+) hour", line)
            if y:
                time = "{}h".format(str(y.group()))
            else:
                raise ValueError("Could not find time")
            srae = SraExperiment(srp, run, assay_type, spotlen, bases, cellline, experiment, infection, librarylayout,
                                 treatment, time,
                                 pmid)
            experiments.append(srae)
    for e in experiments:
        e.set_category2('calu-3', 'SARS', 'SARS')
        e.set_category2('calu-3', 'MERS-CoV', 'MERS-CoV')
        print(e.output_row())
    return experiments




def process_SRP076102():
    '''
    DONE
    Bercovich-Kinori A, Tai J, Gelbart IA, Shitrit A et al. A systematic view on influenza induced host shutoff.
    Elife 2016 Aug 15;5. PMID: 27525483
    :return:
    '''
    runtable = '../data/SRP076102_SraRunTable.txt'
    ind = [0, 1, 2, 3, 7, 25, 21, 17]
    srp = 'SRP076102'
    pmid = 'PMID:27525483'
    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        if 'RNA-seq_2h' == e.get_experiment():
            e.set_category2('A549','Influenza A', 'fluA.2h')
        elif 'RNA-seq_4h' == e.get_experiment():
            e.set_category2('A549', 'Influenza A', 'fluA.4h')
        elif 'RNA-seq_8h' == e.get_experiment():
            e.set_category2('A549', 'Influenza A', 'fluA.8h')
        elif 'RNA-seq_uninfected' == e.get_experiment():
            e.set_category2('A549', 'none', 'control')
    return experiments



def process_SRP091886():
    '''
    DONE
    Heinz S, Texari L, Hayes MGB, Urbanowski M et al. Transcription Elongation Can Affect
    Genome 3D Structure. Cell 2018 Sep 6;174(6):1522-1536.e22.
     PMID: 30146161
    :return:
    '''
    runtable = '../data/SRP091886_SraRunTable.txt'
    ind = [0, 1, 2, 3, 8, 27, 16, 18]
    srp = 'SRP091886'
    pmid = 'PMID:30146161'
    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        time = e.get_experiment() # this was a hack
        e.set_time(time)
        e.set_experiment('n/a')
        infect = e.get_infection()
        #print(infect)
        if 'H3N2' in infect:
            categ = "{}.{}".format('H3N2', time)
        elif 'H1N1' in infect:
            categ = "{}.{}".format('H1N1', time)
        elif 'H5N1' in infect:
            categ = "{}.{}".format('H5N1', time)
        elif 'mock' in infect:
            categ = "{}.{}".format('mock', time)
        else:
            categ = 'n/a'
        e.set_category(categ)
        print(e.output_row())
    return experiments


def process_SRP118721():
    '''
    DONE
    Forst CV, Zhou B, Wang M, Chou TW et al. Integrative gene network analysis identifies key signatures,
    intrinsic networks and host factors for influenza virus A infections. NPJ Syst Biol Appl 2017;3:35.
    PMID: 29214055
    :return:
    '''
    runtable = '../data/SRP118721_SraRunTable.txt'
    ind = [0, 1, 2, 3, 7, 14, 25, 17]
    srp = 'SRP118721'
    pmid = 'PMID:29214055'
    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        infect = e.get_infection()
        print(infect)
        if 'without IAV infection' in infect:
            e.set_category('mock')
        elif 'A549 cells with IAV infection' == infect:
            e.set_category('infA.no.treatment')
        elif 'A549 cells infected with A/PR8/34/(H1N1) at the low' in infect:
            e.set_category('infA.lariciresinol.low')
        elif 'A549 cells infected with A/PR8/34/(H1N1) at the high' in infect:
            e.set_category('infA.lariciresinol.high')
        else:
            raise ValueError('did not recognize category')
        print(e.output_row())
    return experiments


def process_SRP170549():
    '''
    DONE
       Yuan S, Chu H, Chan JF, Ye ZW et al. SREBP-dependent lipidomic reprogramming as a broad-spectrum antiviral target.
        Nat Commun 2019 Jan 10;10(1):120. PMID: 30631056
    :return:
    '''
    runtable = '../data/SRP170549_SraRunTable.txt'
    ind = [0, 1, 2, 3, 7, 14, 25, 17]
    srp = 'SRP170549'
    pmid = 'PMID:30631056'
    SRP170549dict = defaultdict(str)
    SRP170549dict["SRR8239997"] = "AM580"
    SRP170549dict["SRR8239996"] = "AM580"
    SRP170549dict["SRR8239995"] = "AM580"
    SRP170549dict["SRR8239994"] = "MERS"
    SRP170549dict["SRR8239993"] = "MERS"
    SRP170549dict["SRR8239992"] = "MERS"
    SRP170549dict["SRR8239991"] = "mock"
    SRP170549dict["SRR8239990"] = "mock"
    SRP170549dict["SRR8239989"] = "mock"

    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        #print(e.output_row())
        run = e.get_run()
        categ = SRP170549dict.get(run)
        if categ is None:
            raise ValueError("Could not find category")
        e.set_category(categ)
    return experiments

def process_SRP227272():
    '''
    DONE
    Zhang X, Chu H, Wen L, Shuai H et al. Competing endogenous RNA network profiling reveals novel host dependency
    factors required for MERS-CoV propagation. Emerg Microbes Infect 2020 Dec;9(1):733-746. PMID: 32223537
    :return:
    '''
    runtable = '../data/SRP227272_SraRunTable.txt'
    ind = [0, 1, 2, 3, 7, 14, 16, 18]
    srp = 'SRP227272'
    pmid = 'PMID:32223537'

    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        assay = e.get_assaytype()
        if assay == 'RNA-Seq':
            infect = e.get_infection()
            if 'MERS' in infect:
                e.set_category('MERS')
            elif 'mock' in infect:
                e.set_category('mock')
        print(e.output_row())

    return experiments


def process_SRP253951():
    '''
    The  tenOever  dataset
    https://doi.org/10.1101/2020.03.24.004655
    TODO
    :return:
    '''
    runtable = '../data/SRP253951_SraRunTable.txt'
    srp ='SRP253951'
    pmid = 'bioRxiv:https://doi.org/10.1101/2020.03.24.004655'
    ind = [0, 1, 2, 3, 26, 12, 22, 15, 24, 27]
    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        treatment = e.get_treatment()
        cell = e.get_cellline()
        infect = e.get_infection()
        time = e.time
        if time is None or len(time) == 0:
            time = "0h"
        elif time == '24 hours':
            time = '24h'
        elif time == '12 hours':
            time = '12h'
        if 'Ferret' in infect:
            continue # this will be an n/a
        if 'Ferret' in treatment or 'Ferret' in cell:
            continue
        if 'human IFNB treated NHBE cells' == cell:
            e.set_cellline('NHBE')
        if 'A549 cells' in cell:
            cell = 'A549'
        elif 'primary human bronchial epithelial cells' == cell:
            e.set_cellline('NHBE')
        if e.cellline == 'A549' and 'IFNB' in e.treatment:
            categ = 'A549.IFNB.{}'.format(time)
            e.set_category(categ)
        elif e.cellline == 'NHBE' and 'IFNB' in e.treatment:
            categ = 'NHBE.IFNB.{}'.format(time)
            e.set_category(categ)
        if e.cellline == 'A549' and 'Mock' in e.treatment:
            categ = 'A459.mock.{}'.format(time)
            e.set_category(categ)
        elif e.cellline == 'NHBE' and 'Mock' in e.treatment:
            categ = 'NHBE.mock.{}'.format(time)
            e.set_category(categ)
        elif 'Mock treated A549 cells' == infect:
            e.set_cellline('A549')
            categ = 'A459.mock.{}'.format(time)
            e.set_category(categ)
        elif 'Mock treated A549 cells trasnduced with a vector expressing human ACE2' == infect:
            e.set_cellline('A549')
            categ = 'A549.mock.ACE2.{}'.format(time)
            e.set_category(categ)
        elif 'SARS-CoV-2 infected A549 cells trasnduced with a vector expressing human ACE2' == infect:
            e.set_cellline('A549')
            categ = 'A549.covid.ACE2.{}'.format(time)
            e.set_category(categ)
        elif 'Lung biopsy for heatly negative control' == infect:
            e.set_category('healthy.lung.biopsy')
        elif 'Mock treated Calu-3 cells' == infect:
            categ = 'calu-3.mock.{}'.format(time)
            e.set_category(categ)
        elif 'SARS-CoV-2 infected Calu-3 cells' == infect:
            categ = 'calu-3.covid.{}'.format(time)
            e.set_category(categ)
        elif 'Lung sample from postmortem COVID-19' == infect or 'Lung sample from postmortem COVID-19 patient' == infect:
            e.set_category('covid.lung.biopsy')
        elif 'SARS-CoV-2 infected A549 cells' == infect:
            e.set_cellline('A549')
            categ = 'A549.covid.{}'.format(time)
            e.set_category(categ)
        elif 'SARS-CoV-2 infected NHBE cells' == infect:
            e.set_cellline('NHBE')
            categ = 'NHBE.covid.{}'.format(time)
            e.set_category(categ)
        elif 'RSV infected A549' == infect or 'RSV infected A549 cells' == infect:
            e.set_cellline('A549')
            categ = 'A549.RSV.{}'.format(time)
            e.set_category(categ)
        elif 'HPIV3 infected A549 cells' == infect:
            e.set_cellline('A549')
            categ = 'A549.HPIV3.{}'.format(time)
            e.set_category(categ)
        elif 'IAV infected A549 cells' == infect:
            e.set_cellline('A549')
            categ = 'A549.IAV.{}'.format(time)
            e.set_category(categ)
        elif 'Mock treated NHBE cells' == infect:
            e.set_cellline('NHBE')
            categ = 'NHBE.mock.{}'.format(time)
            e.set_category(categ)
        elif 'IAVdNS1 infected NHBE cells' == infect:
            e.set_cellline('NHBE')
            categ = 'NHBE.IAVdNS1.{}'.format(time)
            e.set_category(categ)
        elif 'IAV infected NHBE cells' == infect:
            e.set_cellline('NHBE')
            categ = 'NHBE.IAV.{}'.format(time)
            e.set_category(categ)
        if (e.category == 'n/a'):
            print("OOPS")
            print(SraExperiment.header())
            print("cell", e.cellline)
            print("infection", e.infection)
        print(e.output_row())
    return experiments


def process_SRP254688():
    '''
    DONE
    '''
    runtable = '../data/SRP254688_SraRunTable.txt'
    ind = [0, 1, 2, 3, 7, 15, 29, 26]
    srp = 'SRP254688'
    pmid = 'n/a'
    SSRP254688dict = defaultdict(str)
    SSRP254688dict["SRR11454606"] = "throatswap"
    SSRP254688dict["SRR11454607"] = "BAL"
    SSRP254688dict["SRR11454608"] = "throatswap"
    SSRP254688dict["SRR11454609"] = "throatswap"
    SSRP254688dict["SRR11454610"] = "throatswap"
    SSRP254688dict["SRR11454611"] = "throatswap"
    SSRP254688dict["SRR11454612"] = "sputum"
    SSRP254688dict["SRR11454613"] = "BAL"
    SSRP254688dict["SRR11454614"] = "BAL"
    SSRP254688dict["SRR11454615"] = "BAL"

    experiments = process_sra_runtable(runtable, ind, srp, pmid)
    print(SraExperiment.header())
    for e in experiments:
        run = e.get_run()
        cellline = SSRP254688dict.get(run)
        if cellline is None:
            raise ValueError("Could not find cellline for " + run)
        e.set_cellline(cellline)
        categ = 'covid.{}'.format(cellline)
        e.set_category(categ)
    return experiments


def process_all_datasets():
    all_experiments = []
    exp = process_SRP230823()
    all_experiments.extend(exp)
    exp = process_SRP040070()
    all_experiments.extend(exp)
    exp = process_SRP056612()
    all_experiments.extend(exp)
    exp = process_SRP076102()
    all_experiments.extend(exp)
    exp = process_SRP091886()
    all_experiments.extend(exp)
    exp = process_SRP118721()
    all_experiments.extend(exp)
    exp = process_SRP170549()
    all_experiments.extend(exp)
    exp = process_SRP227272()
    all_experiments.extend(exp)
    exp = process_SRP253951()
    all_experiments.extend(exp)
    exp = process_SRP254688()
    all_experiments.extend(exp)
    return all_experiments




# SRP248940 -- omit because single-end 75 bp
#process_SRP253951()


def print_omit():
    print("Omitting SRP049988 -- not a virus infection")
    print("Omitting SRP056612 -- just two samples, no repeats")
    print("Omitting SRP139919 -- just uninfected A549 samples")
    print("Omitting SRP189350-- Sequencing of influenza A/H1N1 virus from human challenge study and natural infections")


runtable = '../data/SRP254688_SraRunTable.txt'
# explore_indices(runtable)


def process_gsm():
    '''
    Hack to get info -- need to change for each dataset
    :return:
    '''
    path = '../data/SRP254688_GSM_expanded.txt'
    print('SSRP254688dict = defaultdict(str)')
    with open(path) as f:
        next(f)
        for line in f:
            #print(line)
            z = re.search(r"(SRR\d+)", line)
            srs = 'n/a'
            if z:
                srs = z.group(1)
            else:
                raise ValueError("Could not find SRS")
            categ = 'n/a'
            if 'Throat swab' in line:
                categ = 'throatswap'
            elif 'Sputum' in line:
                categ = 'sputum'
            elif 'Bronchoalveolar lavage':
                categ = 'BAL'
            else:
                raise TypeError("Could not id sample type")
            print('SSRP254688dict["%s"] = "%s"' % (srs, categ))
# process_gsm()


experiments = process_all_datasets()
for e in experiments:
    print(e.output_row())

outfilename = 'covid.ingest.tsv'
with open(outfilename, 'wt') as f:
    for e in experiments:
        f.write(e.output_row() +'\n')
