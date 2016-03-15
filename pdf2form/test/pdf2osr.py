import time, glob, os, subprocess, argparse;
from os import listdir;
from PIL import Image;

import pdf2form; 
from pdf2form.pdf2form import element;
from pdf2form.pdf2form import pdfForm;
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
sharedDirectoryPath = "/mnt/hgfs/pdf2form/test";
os.chdir(sharedDirectoryPath);

# Create an OSR object and set the following attributes to the OSR object.
pdf = pdf2form.pdf2form.pdfForm(pdf2convert,toBeProcessedDir="/mnt/hgfs/pdf2form/test/toBeProcessed");
pdf.protocolNum = irbProtocol;
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
oncoreOSR_form = {"agent": pdf2form.pdf2form.element(748,195),"eventDate": pdf2form.pdf2form.element(931,195),"issuedDate": pdf2form.pdf2form.element(1114,195),"drugCompany": pdf2form.pdf2form.element(787,215), "reportNum": pdf2form.pdf2form.element(976,215), "subjectDescription": pdf2form.pdf2form.element(1196,215), "deathWithin": pdf2form.pdf2form.element(777,235), "hospital": pdf2form.pdf2form.element(977,235,type="checkbox"),"followUpNum": pdf2form.pdf2form.element(1062,235), "reviwedDSMB": pdf2form.pdf2form.element(830,255), "sponsorComments": pdf2form.pdf2form.element(811,270), "toxicityCategory": pdf2form.pdf2form.element(716,340), "toxicity": pdf2form.pdf2form.element(840,340), "toxicityComments": pdf2form.pdf2form.element(959,340), "toxicityGrade": pdf2form.pdf2form.element(1082,340), "addTox": pdf2form.pdf2form.element(1212,345,tag="button",type=""),"protocolNum": pdf2form.pdf2form.element(717,440), "recievedDate": pdf2form.pdf2form.element(841,440), "piNotified": pdf2form.pdf2form.element(960,440), "attribution": pdf2form.pdf2form.element(1155,530), "piComments": pdf2form.pdf2form.element(1083,440), "icfChanged": pdf2form.pdf2form.element(1328,442,type="checkbox"), "piSigned": pdf2form.pdf2form.element(715,475), "notReportable": pdf2form.pdf2form.element(842,480,type="checkbox"), "reported2IRB": pdf2form.pdf2form.element(1011,570), "addTracking": pdf2form.pdf2form.element(1035,497,tag="button",type=""), "submitOSR": pdf2form.pdf2form.element(1293,526), "clearOSR": pdf2form.pdf2form.element(1324,628), "closeOSR": pdf2form.pdf2form.element(1372,628)};


#for data in oncoreOSR_form:
#	print(data);
#	if(rawOSR[data]):
#		print(".");
#	else:
#		rawOSR[data] = "";

import time;
import re;
import selenium;
from selenium import webdriver;
from selenium.webdriver.common.keys import Keys;
from selenium.webdriver.common.alert import Alert;


values = [
rawOSR["agent"],
rawOSR["eventDate"],
rawOSR["issuedDate"],
rawOSR["drugCompany"],
rawOSR["reportNum"],
rawOSR["subjectDescription"],
#rawOSR["deathWithin"],
"",
#rawOSR["hospital"],
True,
#rawOSR["followUpNum"],
"1",
#rawOSR["reviwedDSMB"],
False,
rawOSR["sponsorComments"],
rawOSR["toxicityCategory"],
rawOSR["toxicity"],
rawOSR["toxicityComments"],
rawOSR["toxicityGrade"],
rawOSR["protocolNum"],
rawOSR["recievedDate"],
rawOSR["piNotified"],
#rawOSR["attribution"],
"",
#rawOSR["piComments"],
"",
#rawOSR["icfChanged"],
False,
rawOSR["piSigned"],
#rawOSR["notReportable"],
True,
#rawOSR["reported2IRB"]
""
];



print("Starting automated form fillout...");

offcore = webdriver.Firefox();
offcore.get("file:///mnt/hgfs/images/offcore.html");

inputs = offcore.find_elements_by_tag_name("input");

inc = 0;

for input in inputs:
    inputType = input.get_attribute("type");
    if inputType == "checkbox":
        if values[inc] == True:
            input.click();
        inc = inc + 1;
    else:
        input.send_keys(values[inc]);
        inc = inc + 1;    

buttons = offcore.find_elements_by_tag_name("button")
b = 0;
for button in buttons:
    b = b + 1;

addToxButton = buttons[8];
addToxButton.click();

osrNumber = offcore.find_element_by_id("osrDiv").text[5:];
print(osrNumber);
print("This form will be stored as OSR number: "+osrNumber);
offcore.save_screenshot("/mnt/hgfs/pdf2form/test/archive/"+osrNumber+"_screenshot.png");

time.sleep(1);

submitButton = buttons[10];
submitButton.click();
#alert = offcore.switch_to_alert();
Alert(offcore).accept();




print("Form submitted.");



time.sleep(3);
offcore.close();






# Move the converted JPEG file into the archive folder.
convertedJPEG = pdf2convert[:-4]+".jpeg";
#convertedJPEF = 'mnt/hgfs/pdf2form/test/archive//mnt/hgfs/pdf2form/test/testForm1.jpeg'

def archiveJPEG(convertedJPEG,osrNumber,openAfter=True):
	import random;
	import pyautogui;
	import time;
	import shutil;
	import re;
	import os;
	from PIL import Image, ImageDraw, ImageFont;
	
	# Move the JPEG copy of the PDF file to the archive folder.	
	archivePath = "/mnt/hgfs/pdf2form/test/archive/";
	f = os.path.basename(convertedJPEG);
	shutil.move(convertedJPEG,archivePath+f);
	archivedJPEG = Image.open(archivePath+f);
	draw = ImageDraw.Draw(archivedJPEG);

	# Import a font
	fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",40);
	





















































	#remove existing OSR.html file.
	#os.remove("/mnt/hgfs/pdf2form/test/OSR.html");
	
	# Move the cursor to the right-hand side of the screen, and save a copy of the completed OSR submission.
	#pyautogui.moveTo(980,792,1);
	#pyautogui.hotkey('ctrl','s');
	#time.sleep(5);
	#pyautogui.hotkey('enter');
	#time.sleep(1);
	#pyautogui.hotkey('enter');
	#time.sleep(5);

	# Read the contents of the OSR.html file which we saved in the preceeding block of code. Scan the contents for the element that contains the OSR number assigned by the CTMS. 
	#with file("/mnt/hgfs/pdf2form/test/OSR.html") as f:
    #		html=f.read();
	#osrNumber = re.findall("\>OSR# (.*)\<",html);

	# Write the OSR number from the preceeding block of code as well as a timestamp on the archived JPEG.
	draw.text((10,10),"OSR# "+osrNumber,font=fnt,fill='#000000');
	timestamp = time.strftime("%m-%d-%Y  %H:%M:%S");
	fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",20);
	draw.text((10,50),"Processed on: "+timestamp,font=fnt,fill="#000000");
	del draw;
	
	g = os.path.basename(convertedJPEG);
	d = os.path.dirname(convertedJPEG);

	print(g);
	print(d);

	# Save the timestamped JPEG and get rid of the orginally archived one.
	archivedJPEG.save("/mnt/hgfs/pdf2form/test/archive/"+osrNumber+"_processedForm.jpeg","JPEG");

	os.remove(archivePath+g);

	# If the openAfter parameter has not been explicity set to false, open the archived JPEG.
	if openAfter == True:
		openProcessedOSR = "xdg-open /mnt/hgfs/pdf2form/test/archive/"+osrNumber+"_processedForm.jpeg";
		#time.sleep(3);
		#openScreenshot= "xdg-open /mnt/hgfs/pdf2form/test/archive/"+osrNumber+"_screenshot.png";
		import subprocess;
		subprocess.call(openProcessedOSR,shell=True);
		#subprocess.call(openScreenshot,shell=True);
archiveJPEG(convertedJPEG,osrNumber);
# Print the current system time now that the execution of the script is complete.
print(time.strftime("%H:%M:%S")+": Script execution complete");
