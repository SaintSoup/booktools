#!/usr/bin/env

import PyPDF2 as pd
import os
import sys
#Define 
#DBG
#Splitting
#Uploading
def main( ):

    debug = 1
    #parsing command-line flags
    #make sure you catch errors
    #command line is the z
    #put the iterator in here to actually reduce calls
    
    #let's test the command line 
    print("The elements of the command-line")
    for k in sys.argv:
        print(k)
    
    pdf_file_path = sys.argv[-1]
    cleaning(pdf_file_path)
    #splitting(pdf_file_path)
    


def dbg(*values):
    print(*values)     
                                                                     #Here's an idea, make your own print
def print_metadata(file_stream):
    reader = pd.pdfFileReader(file_stream)
    #This is done to get a feel for the file
    print("-----------------------------------------------------")
    print("The file's XMP metdata is")
    xmp_info = reader.getXmpMetadata()
    print("dc_contributor: ",xmp_info.dc_contributor)
    print("dc_coverage: ",xmp_info.dc_coverage)
    print("dc_creator: ",xmp_info.dc_creator)
    print("dc_date: ",xmp_info.dc_date)
    print("dc_description: ",xmp_info.dc_description)
    print("dc_format: ",xmp_info.dc_format)
    print("dc_identifier: ",xmp_info.dc_identifier)
    print("dc_language: ",xmp_info.dc_language)
    print("pdf_keywords: ",xmp_info.pdf_keywords)
    print("dc_relation: ",xmp_info.dc_relation)
    print("dc_title: ",xmp_info.dc_title)
    print("xmp_metadataDate: ",xmp_info.xmp_metadataDate)
    print("xmpmm_documentId: ",xmp_info.xmpmm_documentId)
    print("xmp_modifyDate: ",xmp_info.xmp_modifyDate)
    print("-----------------------------------------------------")

def print_outline(file_stream):
    #this prints a readable version of the outline
    reader = pd.pdfFileReader(file_stream)
    print("-----------------------------------------------------")
    print("The outline of this doc")
    outline = reader.getOutlines()
    for dest,page in ouline:
        print(dest," : ",page)
    print("-----------------------------------------------------")

def cleaning(folder_path):
    #Fetches files and cleans the name and metadata 
    #We make sure that the folder structure is set
    dbg("[DBG] setting up the folder structure")
    if not os.path.exists(folder_path+os.sep+"cln"):
        os.mkdir(folder_path+os.sep+"cln")   
    dbg("[DBG] Starting cleaning")  
    with os.scandir(folder_path) as it:                                                  #This is the way to iterate through files
        for entry in it:
            if not(entry.name.startswith(os.curdir)) and entry.is_file() and entry.name.endswith(".pdf"):
                print(entry.name)
                newname = entry.name.rstrip(".pdf")
                newname.replace("_"," ")
                pos_bracket1 = newname.find("(")
                pos_bracket2 = newname.find(")")
                newname = newname[:pos_bracket1]+ newname[pos_bracket2+1:]
                #newname.trim()
                dbg("[DBG] Done name formating: ",newname," , proceeding to metadata")  #Add metadata elements before this
                os.mkdir(folder_path+os.sep+"cln"+os.sep+newname) #The command had lots of spaces
                comlin="cp "+folder_path+os.sep+'"'+entry.name+'"'+" "+folder_path+os.sep+"cln"+os.sep+'"'+newname+'"'+os.sep+'"'+newname+".pdf"+'"'            #I can rename it here
                print("The command to copy: ",comlin)           
                os.system(comlin)
                print("The command is executed")
                #data= open(folder_path+os.sep+"cln"+os.sep+'"'+newname+'"'+os.sep+'"'+newname+".pdf"+'"',"r")
                #print_metadata(data)    
                #print_outline(data)
                #data=os.close('"'+folder_path+os.sep+"cln"+os.sep+newname+os.sep+newname+".pdf"+'"')                                              #For  portability reasons, add win and mac options
                #data.close()    
    dbg("[DBG] Done cleaning")

def splitting(folder_path):
    # After the cleaning, we check the outline, if the outline is less than the number of pages 
    # (it means it hasn't taken an outline of the pages) it makes the outline as a list 
    with os.scandir(folder_path) as it:
        for entry in it:
            if not(entry.name.startswith(os.curdir)) and not(entry.is_file()):
                #we go into the entry
                os.chdir(folder_path+os.sep+"cln"+os.sep+str(entry))
                data = open(entry+".pdf").read()
                reader = pd.pdfFileReader(data)
                outline = reader.getOutline()
                count=0
                if  len(outline) != reader.getNumPages():
                    outline_list = outline.values().sort()
                for i in range(len(outline_list)): 
                    count+=1
                    for j in range(outline_list[i],outline_list[i+1]):
                        writer = pd.pdfFileWriter()
                        writer.addPage(reader.getPage(j))
                    output = entry+' '+str(count)+'.pdf'
                    with open(output, 'wb') as output_pdf:
                        writer.write(output_pdf)
                        writer.close()
                        close(output_pdf)
                reader.close()
                #we exit the entry
                os.chdir(os.pardir)
if __name__ == '__main__':
    main()





            
    


