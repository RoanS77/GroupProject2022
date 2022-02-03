from abc import ABC, abstractmethod  # needed for recycling of the same class-base
import re   # needed for removal of HTML <span> strings from dataset sentences

class RecordMetadata:
    def __init__(self, df1, df2):
        self.__df1 = df1
        self.__df2 = df2

    def metadata(self):  # shape automatically returns number of rows and columns
        return list(self.__df1.shape) + list(self.__df2.shape)


class RecordSemantics:
    def __init__(self, df1, df2):
        self.__df1 = df1
        self.__df2 = df2

    def semantics(self):  # the first row (obtained via .head) contains the column names
        return [self.__df1.head(0).columns, self.__df2.head(0).columns]


class RecordDifferent(ABC):     # The abstract class points 3 and 5 are based on
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def record(self):
        pass


class RecordGenes(RecordDifferent):
    def __init__(self, df2):
        self.__df2 = df2

    def record(self):   # all new ids are saved into a dictionary geneid : frequency

        t = self.__df2['geneid']
        l = []
        for el in t:
            l.append(el)

        d = {}
        for el in l:
            if el in d.keys():
                d[el] += 1
            else:
                d[el] = 1

        tl = sorted(d.items(), key=lambda x: x[1])  # the way to order a dictionary through its values (frequency)
        sorted_d = {k: v for k, v in tl}   # creation of an ordered dictionary from previous items
        return sorted_d


class RecordDiseases(RecordDifferent):
    def __init__(self, df1):
        self.__df1 = df1

    def record(self):  # all new ids are saved into a dictionary diseaseid : frequency

        t = self.__df1['diseaseid']
        l = []
        for el in t:
            l.append(el)

        d = {}
        for el in l:
            if el in d.keys():
                d[el] += 1
            else:
                d[el] = 1

        tl = sorted(d.items(), key=lambda x: x[1])  # same as before
        sorted_d = {k: v for k, v in tl}
        return sorted_d


class SentenceList(ABC):  # The abstract class points 4 and 6 are based on
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def sentences(self, ui):
        pass

class GeneSentences(SentenceList):
    def __init__(self, df2):
        self.__df2 = df2

    def sentences(self, ui):  # based on the presence of the substring "<span class='disease covid cdisease'"
        sentences = []        # if it is present, the sentence is added to a sentence-list to later be processed
        for el in range(len(self.__df2)):
            if ui == str(self.__df2.at[el, 'geneid']) or ui in self.__df2.at[el, 'gene_symbol']:  # check user input
                if "<span class='disease covid cdisease'" in self.__df2.at[el, 'sentence']:
                    s = re.sub('<[^<]+?>', '', self.__df2.at[el, 'sentence'])  # reg.ex. way of cleaning a string
                    sentences.append(s)                                        # from HTML <span> text

        if len(sentences) == 0:  # later needed for occasional user errors, typos
            return 'Err404'
        else:
            return sentences


class DiseaseSentences(SentenceList):
    def __init__(self, df1):
        self.__df1 = df1

    def sentences(self, ui):  # same as before, with the other dataset
        sentences = []
        for el in range(len(self.__df1)):
            if ui == self.__df1.at[el, 'diseaseid'] or ui in self.__df1.at[el, 'disease_name']:
                if "<span class='disease covid cdisease'" in self.__df1.at[el, 'sentence']:
                    s = re.sub('<[^<]+?>', '', self.__df1.at[el, 'sentence'])
                    sentences.append(s)

        if len(sentences) == 0:
            return 'Err404'
        else:
            return sentences

class RecordTop10:  # taking one database simplifies the algorithm and lightens it
    def __init__(self, df2):  # each database has enough information to create a top 10:
        self.__df2 = df2      # the gene IDs in the first column and the disease IDs inside sentences

    def record10(self):
        d = {}
        genes = self.__df2['geneid']
        counter = 1
        for sentence in self.__df2['sentence']:  # iteration on sentences avoids repetitions
            diseases = []
            if "<span class='disease' id='" in sentence:  # take advantage of the "<span class='disease' id='" string
                for el in range(len(sentence)):           # present in all diseases
                    if sentence[el:el + 26] == "<span class='disease' id='":  # COVID was purposely avoided
                        new = sentence[el + 26:]                              # to prevent over-saturation of top10
                        new_dis = ''
                        for el2 in new:  # loop to save the disease(s)
                            if el2 != '-':
                                new_dis += el2
                            else:        # finding a - interrupts the construction of the diseaseID
                                break

                        if '_' in new_dis:  # multiple diseases per gene are separated by _
                            new = new_dis.split('_')  # they are split into two separated elements
                            for el2 in new:           # but remain linked to the same gene
                                diseases.append(el2)
                        else:
                            diseases.append(new_dis)  # those are all the diseases per each gene

                for disease in diseases:
                    tup = disease, genes[counter]     # saves ALL diseases in tuples linked to their respective gene
                    if tup in d.keys():               # and also saves how many times this couple appears
                        d[tup] += 1
                    else:
                        d[tup] = 1
                counter += 1                          # only AFTER the sentence ends the counter increases
        sorted_dict = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}  # frequency-based dictionary sort
        top10 = list(sorted_dict)[:-11:-1]  # a top 10 would be better represented in descending frequency order
        return top10                        # this will be later represented in HTML with an ordered list


class Associated(ABC):  # The abstract class points 8 and 9 are based on
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def associate(self, ui):
        pass


class AssociatedDiseases(Associated):  # both databases are needed in this case. Linked through pmids.
    def __init__(self, df1, df2):
        self.__df1 = df1
        self.__df2 = df2

    def associate(self, ui):
        pmids = []
        for el in range(len(self.__df2)):  # save all relevant pmids based on user input
            if ui == str(self.__df2.at[el, 'geneid']) or ui in self.__df2.at[el, 'gene_symbol']:
                pmids.append(self.__df2.at[el, 'pmid'])

        diseases = []
        for el in range(len(self.__df1)):  # switch database and save all diseases linked to saved pmids
            if (self.__df1.at[el, 'pmid'] in pmids) and (self.__df1.at[el, 'disease_name'] not in diseases):
                diseases.append(self.__df1.at[el, 'disease_name'])  # avoid repetition of dame element

        if len(diseases)==0:  # same user-error handling as before
            return 'Err404'
        else:
            return diseases

class AssociatedGenes(Associated):
    def __init__(self, df1, df2):
        self.__df1 = df1
        self.__df2 = df2

    def associate(self, ui):  # same as before, with the other database
        pmids = []
        for el in range(len(self.__df1)):
            if ui == str(self.__df1.at[el, 'diseaseid']) or ui in self.__df1.at[el, 'disease_name']:
                pmids.append(self.__df1.at[el, 'pmid'])
        genes = []
        for el in range(len(self.__df2)):
            if self.__df2.at[el, 'pmid'] in pmids and self.__df2.at[el, 'gene_symbol'] not in genes:
                genes.append(self.__df2.at[el, 'gene_symbol'])

        if len(genes)==0:
            return 'Err404'
        else:
            return genes
