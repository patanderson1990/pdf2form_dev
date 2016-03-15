import time, glob, os, subprocess, argparse;
from os import listdir;
from PIL import Image;

import pdf2form; 

# Print out the current time at the start of script execution.
print(time.strftime("%H:%M:%S")+": Beginning of script execution...");

# Parse any arugments that may have been passed to the file. -f is the name of the file, -p (if implemented) will be name of the protocol.
parser = argparse.ArgumentParser(description="Takes filename & protocol name");
parser.add_argument('-f',default="osr.pdf");
parser.add_argument('-p',default="test protocol");
args = parser.parse_args();
pdf2convert = args.f;
irbProtocol = args.p;

# Set the current working directory to the shared directory path.
sharedDirectoryPath = "/mnt/hgfs/images";
os.chdir(sharedDirectoryPath);

# Create an OSR object and set the following attributes to the OSR object.
pdf = pdf2form.OSR(pdf2convert,irbProtocol);
pdf.readInfo("subjectAge",810,535,860,575);
pdf.readInfo("subjectSex",880,530,930,560,True);
pdf.readInfo("agent",215,975,1135,1000);
pdf.readInfo("eventDay",945,530,990,560,True);
pdf.readInfo("eventMonth",1000,530,1060,560,True);
pdf.readInfo("eventYear",1080,530,1120,560);
pdf.readInfo("drugCompany",215,1590,690,1610);
pdf.readInfo("reportNum",500,1700,780,1730);
pdf.readInfo("toxicity",215,605,1110,635);
pdf.readInfo("toxicityComments",215,635,1110,660);
pdf.readInfo("issuedDate",285,1835,415,1860);

#List of variables that correspond to the data in the OSR report.
agent = pdf.agent;
eventDate = pdf.eventMonth+"/"+pdf.eventDay+"/"+pdf.eventYear;
issuedDate = pdf.issuedDate;
drugCompany = pdf.drugCompany;
reportNum = pdf.reportNum;
subjectDescription = pdf.subjectAge+" y.o. "+pdf.subjectSex;
sponsorComments = "This does not need to be reported to the IRB.";
toxicityCategory = "Pulmonary/Upper Resipratory";
toxicity = pdf.toxicity;
toxicityComments = pdf.toxicityComments;
toxicityGrade = "3";
protocolNum = irbProtocol;
recievedDate = "";
piNotified = "";
piSigned = "";

#Create a representation of the data contained in the OSR report.
rawOSR = {"agent":agent,"eventDate":eventDate,"issuedDate":issuedDate,"drugCompany":drugCompany, "reportNum":reportNum,"subjectDescription":subjectDescription,"sponsorComments":sponsorComments,"toxicityCategory":toxicityCategory,"toxicity":toxicity,"toxicityComments":toxicityComments,"toxicityGrade":toxicityGrade,"protocolNum":protocolNum,"recievedDate":recievedDate,"piNotified":piNotified,"piSigned":piSigned};

#Create a representation of the new OSR form in onCore. The numbers are the coordinates of the various UI elements on the screen, which will vary on different resolution monitors. 
oncoreOSR_form = {"agent": pdf2form.element(777,212),"eventDate": pdf2form.element(975,212),"issuedDate": pdf2form.element(1189,212),"drugCompany": pdf2form.element(805,233), "reportNum": pdf2form.element(1025,233), "subjectDescription": pdf2form.element(718,255), "deathWithin": pdf2form.element(793,279), "hospital": pdf2form.element(1026,276,type="checkbox"),"followUpNum": pdf2form.element(1135,279), "reviwedDSMB": pdf2form.element(851,299), "sponsorComments": pdf2form.element(720,334), "toxicityCategory": pdf2form.element(723,416), "toxicity": pdf2form.element(867,415), "toxicityComments": pdf2form.element(1013,416), "toxicityGrade": pdf2form.element(1159,417), "addTox": pdf2form.element(1308,416,tag="button",type=""),"protocolNum": pdf2form.element(722,531), "recievedDate": pdf2form.element(864,530), "piNotified": pdf2form.element(1010,529), "attribution": pdf2form.element(1155,530), "piComments": pdf2form.element(1299,529), "icfChanged": pdf2form.element(794,345,type="checkbox"), "piSigned": pdf2form.element(725, 570), "notReportable": pdf2form.element(864,573,type="checkbox"), "reported2IRB": pdf2form.element(1011,570), "addTracking": pdf2form.element(1101,594,tag="button",type=""), "submitOSR": pdf2form.element(1272,628), "clearOSR": pdf2form.element(1324,628), "closeOSR": pdf2form.element(1372,628)};

#Match the data in the OSR to the appropriate element in the form. Then enter the appropriate values.
for data in rawOSR:
    print(data);
    oncoreOSR_form[data].enterValue(rawOSR[data]);

# Click the "Add" button in the toxicity section.
oncoreOSR_form["addTox"].click();

# Move the converted JPEG file into the archive folder.
convertedJPEG = pdf2convert[:-4]+".jpeg";

pdf2form.archiveJPEG(convertedJPEG);
# Print the current system time now that the execution of the script is complete.
print(time.strftime("%H:%M:%S")+": Script execution complete");
