# Credits for the Dockerfile template style to the https://nf-co.re/ community
FROM nfcore/base:1.7
LABEL authors="Christina Chatzipantsiou <chatzipantsiou@gmail.com>" \
      description="Docker image for Ontologizer"

# Install the conda environment
COPY environment.yml /
RUN conda env update --name base --file /environment.yml && \
    wget http://ontologizer.de/cmdline/Ontologizer.jar -P /opt/conda/envs/base/ 

# Add conda installation dir to PATH (instead of doing 'conda activate')
ENV PATH /opt/conda/envs/base/:$PATH

# Add alias for ontologizer
RUN echo "alias ontologizer=java -jar /opt/conda/envs/base/Ontologizer.jar" >> ~/.bashrc

# Dump the details of the installed packages to a file for posterity
RUN conda env export  --name ontologizer | grep -v "^prefix: " > ontologizer_environment.yml
