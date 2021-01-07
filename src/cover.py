#!/usr/bin/env python
#makes a pdf out of a cover.jpg 
from PIL import Image
import PyPDF2 as pd
import  os, sys
EOF_MARKER = b'%%EOF'
#convert the image to pdf
def convert(PATH):
    cover = Image.open(PATH)
    im = cover.convert('RGB')
    new_path = PATH[:-9]+"cover.pdf"
    im.save(new_path)
    print("------» Cover is converted: %s" %PATH)
    return new_path

def coverUP(cover_path, book_path, dest):
    pdfCOVER = open(cover_path, 'rb')
    pdfBOOK = open(book_path, 'rb')
    #Check the file has a an EOF 
    reader1=pdfCOVER.read()
    reader2=pdfBOOK.read()
    print("Checking the EOF MARKERS in the files:")
    if EOF_MARKER in reader1:
        print("-----> Book 1 has an EOF")
    else:
        print("-----> Book 1: no EOF found")
        newcover = reader1[:-5] + EOF_MARKER
        cover_path=cover_path+"_new"
        with open(cover_path, 'wb+') as f:
            f.write(newcover)
    if EOF_MARKER in reader2:
        print("-----> Book 2 has an EOF")
    else:
        print("-----> Book 2: no EOF found")
        newbook = reader2[:-5] + EOF_MARKER
        book_path=book_path+"_new"
        with open(book_path, 'wb+') as f:
            f.write(newbook)
    #Reading files through PyPDF
    pdfCoverReader = pd.PdfFileReader(cover_path)
    pdfBookReader = pd.PdfFileReader(book_path)
    merger = pd.PdfFileMerger()
    if(book_path and cover_path):
        with open(cover_path,'rb') as f:
            print("The cover's path ", cover_path)
            merger.append(pdfCoverReader)
        with open(book_path,'rb') as f:
            print("The cover's path ", book_path)
            merger.append(pdfBookReader)
    Info = pdfBookReader.getDocumentInfo()
    merger.write(dest+os.sep+Info.title+"_Final.pdf")
    merger.close()
    pdfCOVER.close()
    pdfBOOK.close()

def findElements(dirName,fileList):
    #takes in the directory and finds the elements of the transaction
    listPDF=[]
    print('Found directory: %s' % dirName)
    for fname in fileList:
        print('|_____ %s' % fname)
        if (fname == "cover.jpg") :
            cover=dirName+os.sep+fname
            print('-----> Found a cover for: %s' %fname)
        if fname.endswith(".pdf") and fname!="cover.pdf":
            listPDF.append(dirName+os.sep+fname)
    return cover, listPDF[0]

def main():
    while len(sys.argv) != 3:
        print("Too or few or too many arguments")

    Path = sys.argv[1]
    Destination = sys.argv[2]
    for dirName, subdirList, fileList in os.walk(Path, topdown=True):
        cover, book = findElements(dirName,fileList)
        cover= convert(cover)
        print("type of cover ",str(type(cover))," and type of book ",str(type(book)) )
        coverUP(cover, book, Destination)
    return 0
if __name__ == '__main__':
    main()