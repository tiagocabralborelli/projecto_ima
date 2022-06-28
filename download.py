import pandas as pd
import os
from refsef_download import carregar_metadados
refseq_metadados = carregar_metadados("prokaryotes.xlsx")
refseq_metadados.dropna(inplace = True)
refseq_metadados = refseq_metadados[refseq_metadados.rRNA > 0]
print(f"Número de genomas com RNA ribossomal: {len(refseq_metadados)}")
sufix = "_rna_from_genomic.fna.gz"
genomas_max = 10000
for info in refseq_metadados[0:genomas_max].itertuples():
    genome_id = info.FTP_refseq.split("/")[-1]
    os.system(f"wget {info.FTP_refseq + '/' + genome_id + sufix} -O teste/{genome_id}-{info.Taxon.split(';')[-1]}.fasta.gz")   