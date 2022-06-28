import pandas as pd
import os
def carregar_metadados(path:str):
    """Carrega a tabela com os metadados de todas as bactérias presentes no NCBI-RefSeq
    Parametros:
    path -> diretórion onde a tabela de metadados está
    -----
    Returno:
    Um objeto do tipo pandas.DataFrame com as colunas o nome das colunas editados
    """
    table = pd.read_excel(path)
    table.drop(["FTP","RefSeq","FTP.1","rRNA"], axis = 1, inplace = True)
    table.rename(inplace = True, columns = {
    "#Organism":"Especie",
    "Name":"Taxon",
    "Organism":"FTP_genbank",
    "Groups":"FTP_refseq",
    "GenBank":"rRNA"
    })
    table["Genero"] = table.Especie.apply(lambda x: x.split(" ")[0]) 
    return table

def baixar_genomas(metadados, limite_inferior:int, limite_superior:int,maximo:int, diretorio:str):
    """
    Baixa os dados de rRNA dos genomas bacterianos em intervalor pre definidos para evitar request errors
    Parametros:
        metadados -> tabela contendo metadados dos genomas do RefSeq
        limite_inferior -> inicio do intervalo
        limite_superior -> fim do intervalo
        maximo -> número de genomas a serem baixados
        diretorio -> onde os genomas serão armazenados
    """
    sufix = "_rna_from_genomic.fna.gz"
    while limite_superior < maximo:
        for info in metadados[limite_inferior:limite_superior].itertuples():
            genome_id = info.FTP_refseq.split("/")[-1]
            os.system(f"wget {info.FTP_refseq + '/' + genome_id + sufix} -O {diretorio}/{genome_id}-{info.Taxon.split(';')[-1]}.fasta.gz")            
            limite_inferior += limite_superior
            limite_superior += limite_superior