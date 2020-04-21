nextflow run main.nf \
-resume \
--reads 's3://lifebit-featured-datasets/pipelines/nf-core-rnaseq-data/*.gz' \
--max_cpus 2 \
--max_memory 8.GB \
--single_end \
--subsampFilesizeThreshold 4000000 \
--fasta 'https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/reference/genome.fa' \
--gtf 'https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/reference/genes.gtf' \
--assetsDir "." \
--email chatzipantsiou@gmail.com \
-profile docker