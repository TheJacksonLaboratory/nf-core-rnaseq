FROM nfcore/base:1.9
LABEL authors="Phil Ewels, Rickard Hammarén" \
      description="Docker image containing all software requirements for the nf-core/rnaseq pipeline"

# Install the conda environment
COPY environment.yml /
RUN conda env create -f /environment.yml && conda clean -a


RUN mkdir /opt/scripts

COPY ./bin/* /opt/scripts/

RUN find /opt/scripts/ -type f -iname "*.py" -exec chmod +x {} \; && \
    find /opt/scripts/ -type f -iname "*.r"   -exec chmod +x {} \; && \
    find /opt/scripts/ -type f -iname "*2bed" -exec chmod +x {} \;

# Add conda installation dir to PATH (instead of doing 'conda activate')
ENV PATH /opt/conda/envs/nf-core-rnaseq-1.4.3.rsem/bin:$PATH
ENV PATH /opt/scripts:$PATH

# Dump the details of the installed packages to a file for posterity
RUN conda env export --name nf-core-rnaseq-1.4.3.rsem > nf-core-rnaseq-1.4.3.rsem.yml
