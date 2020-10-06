// Import generic module functions
include { saveFiles; getSoftwareName } from './functions'

process SALMON_TXIMPORT {
    tag "$meta.id"
    label "process_medium"
    publishDir "${params.outdir}",
        mode: params.publish_dir_mode,
        saveAs: { filename -> saveFiles(filename:filename, options:options, publish_dir:getSoftwareName(task.process), publish_id:meta.id) }

    container "quay.io/biocontainers/bioconductor-tximeta:1.6.2--r40_0"
    //container https://depot.galaxyproject.org/singularity/bioconductor-tximeta:1.6.2--r40_0

    conda (params.conda ? "bioconda::bioconductor-tximeta=1.6.2" : null)
    
    input:
    tuple val(meta), path("salmon/*")
    path  tx2gene
    val   options

    output:
    tuple val(meta), path("*gene_tpm.tsv")         , emit: tpm_gene
    tuple val(meta), path("*gene_counts.tsv")      , emit: counts_gene
    tuple val(meta), path("*transcript_tpm.tsv")   , emit: tpm_transcript
    tuple val(meta), path("*transcript_counts.tsv"), emit: counts_transcript
    path  "*.version.txt"                          , emit: version

    script: // This script is bundled with the pipeline, in nf-core/rnaseq/bin/
    """
    salmon_tximport.r NULL salmon $meta.id
    Rscript -e "library(tximeta); write(x=as.character(packageVersion('tximeta')), file='bioconductor-tximeta.version.txt')"
    """
}