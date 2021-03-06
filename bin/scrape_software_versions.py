#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
import re

regexes = {
    'nf-core/rnaseq': ['v_ngi_rnaseq.txt', r"(\S+)"],
    'Nextflow': ['v_nextflow.txt', r"(\S+)"],
    'FastQC': ['v_fastqc.txt', r"FastQC v(\S+)"],
    'Cutadapt': ['v_cutadapt.txt', r"(\S+)"],
    'Trim Galore!': ['v_trim_galore.txt', r"version (\S+)"],
    'SortMeRNA': ['v_sortmerna.txt', r"SortMeRNA version (\S+),"],
    'STAR': ['v_star.txt', r"(\S+)"],
    'HISAT2': ['v_hisat2.txt', r"version (\S+)"],
    'Picard MarkDuplicates': ['v_markduplicates.txt', r"([\d\.]+)-SNAPSHOT"],
    'Samtools': ['v_samtools.txt', r"samtools (\S+)"],
    'featureCounts': ['v_featurecounts.txt', r"featureCounts v(\S+)"],
    'RSEM': ['v_rsem.txt', r"RSEM v(\S+)"],
    'Salmon': ['v_salmon.txt', r"salmon (\S+)"],
    'deepTools': ['v_deeptools.txt', r"bamCoverage (\S+)"],
    'StringTie': ['v_stringtie.txt', r"(\S+)"],
    'Preseq': ['v_preseq.txt', r"Version: (\S+)"],
    'RSeQC': ['v_rseqc.txt', r"read_duplication.py ([\d\.]+)"],
    'Qualimap': ['v_qualimap.txt', r"QualiMap v(\S+)"],
    'dupRadar': ['v_dupRadar.txt', r"(\S+)"],
    'edgeR': ['v_edgeR.txt', r"(\S+)"],
    'MultiQC': ['v_multiqc.txt', r"multiqc, version (\S+)"],
    'umi_tools': ['v_umi_tools.txt', r"UMI-tools version: (\S+)"]
}
results = OrderedDict()
results['nf-core/rnaseq'] = '<span style="color:#999999;">N/A</span>'
results['Nextflow'] = '<span style="color:#999999;">N/A</span>'
results['FastQC'] = '<span style="color:#999999;">N/A</span>'
results['Cutadapt'] = '<span style="color:#999999;">N/A</span>'
results['Trim Galore!'] = '<span style="color:#999999;">N/A</span>'
results['SortMeRNA'] = '<span style="color:#999999;">N/A</span>'
results['STAR'] = False
results['HISAT2'] = False
results['Picard MarkDuplicates'] = '<span style="color:#999999;">N/A</span>'
results['Samtools'] = '<span style="color:#999999;">N/A</span>'
results['featureCounts'] = '<span style="color:#999999;">N/A</span>'
results['Salmon'] = '<span style="color:#999999;">N/A</span>'
results['StringTie'] = '<span style="color:#999999;">N/A</span>'
results['Preseq'] = '<span style="color:#999999;">N/A</span>'
results['deepTools'] = '<span style="color:#999999;">N/A</span>'
results['RSeQC'] = '<span style="color:#999999;">N/A</span>'
results['dupRadar'] = '<span style="color:#999999;">N/A</span>'
results['edgeR'] = '<span style="color:#999999;">N/A</span>'
results['Qualimap'] = '<span style="color:#999999;">N/A</span>'
results['MultiQC'] = '<span style="color:#999999;">N/A</span>'

# Search each file using its regex
for k, v in regexes.items():
    try:
        with open(v[0]) as x:
            versions = x.read()
            match = re.search(v[1], versions)
            if match:
                results[k] = "v{}".format(match.group(1))
    except IOError:
        results[k] = False

# Strip STAR or HiSAT2
for k in results:
    if not results[k]:
        del results[k]

# Dump to YAML
print(
    """
id: 'software_versions'
section_name: 'nf-core/rnaseq Software Versions'
section_href: 'https://github.com/nf-core/rnaseq'
plot_type: 'html'
description: 'are collected at run time from the software output.'
data: |
    <dl class="dl-horizontal">
"""
)
for k, v in results.items():
    print("        <dt>{}</dt><dd><samp>{}</samp></dd>".format(k, v))
print("    </dl>")

# Write out regexes as csv file:
with open("software_versions.csv", "w") as f:
    for k, v in results.items():
        f.write("{}\t{}\n".format(k, v))
