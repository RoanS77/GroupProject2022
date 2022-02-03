from flask import Flask, render_template, request
from part1_readfiles import Registry  # the part that guides the program to the correct output


app = Flask(__name__)


@app.route('/')  # homepage
def index_page():
    r = Registry().returnregistry()
    l = Registry().returnlinks()  # to shorten links and not use registry as mentioned in part1
    return render_template('index.html', registry=r, links=l, length=9)

@app.route('/RecNum')  # 2.1
def result_page():
    res = Registry().return_metadata()
    return render_template('metadata.html', result=res)

@app.route('/RecGen')  # 2.2
def result_page2():
    res = Registry().return_general()
    return render_template('general.html', result=res)

@app.route('/RecDiffGenes')  # 2.3
def result_page3():
    res = Registry().return_genes()
    return render_template('genes.html', result=res)

@app.route('/RecDiffDiseases')  # 2.5
def result_page5():
    res = Registry().return_diseases()
    return render_template('diseases.html', result=res)

@app.route('/SentenceListGeneUser')  # 2.4 // user input page
def user_page():
    return render_template('genesentences.html')

@app.route('/SentenceListGene')  # 2.4
def result_page4():
    data = request.args
    userinput = data.get('gene')  # request user input
    resultclass = Registry().return_sentence_genes()  # request class from part1
    res = resultclass.sentences(userinput)  # request combined result
    if res == 'Err404':  # error handling as explained in part2
        return render_template('errorSLG.html')  # specific error page
    else:
        return render_template('sentencelist.html', result=res)

@app.route('/SentenceListDiseaseUser')  # 2.6 // user input page
def user_page2():
    return render_template('diseasesentences.html')

@app.route('/SentenceListDisease')  # 2.6
def result_page6():
    data = request.args
    userinput = data.get('disease')
    resultclass = Registry().return_sentence_diseases()
    res = resultclass.sentences(userinput)
    if res == 'Err404':
        return render_template('errorSLD.html')
    else:
        return render_template('sentencelist.html', result=res)

@app.route('/Top10')  # 2.7
def result_page7():
    res = Registry().return_top10()
    return render_template('top10.html', result=res)

@app.route('/GeneToDiseasesUser')  # 2.8 - user input
def user_page3():
    return render_template('genetodisease.html')

@app.route('/GeneToDiseases')  # 2.8
def result_page8():
    data = request.args
    userinput = data.get('gene')
    resultclass = Registry().return_diseases_from_genes()
    res = resultclass.associate(userinput)
    if res == 'Err404':
        return render_template('errorGTD.html')
    else:
        return render_template('genetodiseaseresult.html', result=res, gene=userinput)

@app.route('/DiseaseToGenesUser')  # 2.9 - user input
def user_page4():
    return render_template('displeased.html')

@app.route('/DiseaseToGenes')  # 2.9
def result_page9():
    data = request.args
    userinput = data.get('disease')
    resultclass = Registry().return_genes_from_diseases()
    res = resultclass.associate(userinput)
    if res == 'Err404':
        return render_template('errorDTG.html')
    else:
        return render_template('diseasetogenesresult.html', result=res, disease=userinput)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
