import pandas as pd
from part2_classes_operations import *  # import all the classes containing operations of Part 2


class Registry:  # Selects correct method based on user input
    def __init__(self):  # Data Readers & Registry
        self.__df1 = pd.read_csv('disease_evidences.tsv', delimiter="\t")
        self.__df2 = pd.read_csv('gene_evidences.tsv', delimiter="\t")
        self.__operations = ['Record numerical metadata',
                             'Record general semantics',
                             'Record different genes',
                             'Record different diseases',
                             'Provide list of sentences given gene symbol/ID related to COVID-19',
                             'Provide list of sentences given disease name/ID related to COVID-19',
                             'Record top 10 associations genes-diseases',
                             'Provide disease list given gene symbol/ID',
                             'Provide gene list given disease name/ID']
        self.__links = ['RecNum', 'RecGen', 'RecDiffGenes', 'RecDiffDiseases',
                        'SentenceListGeneUser', 'SentenceListDiseaseUser', 'Top10',
                        'GeneToDiseasesUser', 'DiseaseToGenesUser']

    def returnregistry(self):  # needed for HTML homepage
        return self.__operations

    def returnlinks(self):  # needed for HTML homepage / avoid long names of self.__operations
        return self.__links

    def return_metadata(self):  # 2.1
        return RecordMetadata(self.__df1, self.__df2).metadata()

    def return_general(self):  # 2.2
        return RecordSemantics(self.__df1, self.__df2).semantics()

    def return_genes(self):  # 2.3
        return RecordGenes(self.__df2).record()

    def return_diseases(self):  # 2.5
        return RecordDiseases(self.__df1).record()

    def return_sentence_genes(self):  # 2.4
        return GeneSentences(self.__df2)

    def return_sentence_diseases(self):  # 2.6
        return DiseaseSentences(self.__df1)

    def return_top10(self):  # 2.7
        return RecordTop10(self.__df2).record10()

    def return_diseases_from_genes(self):  # 2.8
        return AssociatedDiseases(self.__df1, self.__df2)

    def return_genes_from_diseases(self):  # 2.9
        return AssociatedGenes(self.__df1, self.__df2)
