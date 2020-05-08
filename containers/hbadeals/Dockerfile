FROM nfcore/base:1.9

LABEL authors="cgpu" \
      description="Docker image containing dependencies for the HBA-DEALS R package"

COPY environment.yml /
COPY install.R /
COPY rsem2hbadeals.R /

RUN conda env update --name base --file /environment.yml &&  \
    Rscript /install.R && \
    conda clean -a

RUN mv /rsem2hbadeals.R /opt/conda/envs/rsem2hbadeals.R

ENV PATH /opt/conda/envs/base/bin:$PATH
ENV PATH /opt/conda/envs/:$PATH