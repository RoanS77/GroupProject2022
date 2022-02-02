# GroupProject2022
Authors: Spadazzi Roan, Bertozzi Jacopo, Martinengo Lucia, Sperandio Luca

-------------------------------------------------------------------------
# FILES & FOLDERS

.py files

Libraries used & needed: pandas, re, abc, flask.

part1_readfiles.py includes:
  - operation registry
  - database reading (df1 & df2)
  - operation coordination

part2_classes_operations.py includes:
  - classes containing operations performable on the dataset
  
 part3_webapp.py includes:
  - Flask-based web application
  - load of HTML pages
  - start of the local-host web server
  - link: http://127.0.0.1:8080/
  - user-input error handling

Further explanations on methodologies used inside the code (comments)

CRC Cards includes:
  .PNG Images for each class used in part2

templates includes:
  .html files for web-page loading

GroupProject.vpp is:
  a .vpp file that can be loaded with Visual Paradigm for the UML diagram

UML Diagram.PNG is:
  the PNG equivalent of the .vpp file
  
.tsv files are:
  the two databases the operations work on, respectively:
    - disease_evidences.tsv also known as df1 in the code
    - gene_evidences.tsv also know as df2 in the code
