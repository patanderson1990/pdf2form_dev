import time, glob, os, subprocess, argparse;
from os import listdir;
from PIL import Image;

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

# Define the OSR class, which represents the data contained on the OSR's that are sent by the study sponsor.
class OSR:
    def __init__(self,pdfFile,protocol):
		#Set the protocol that this OSR is associated with, as well as the file name for the JPEG file we are about to create.        
		self.protocolNum = protocol;
		self.imagePath = pdfFile[:-4]+".jpeg";
        
		# Convert pdfFile to a JPEG file with the same name, but stored in the toBeProcessed directory.
		print(time.strftime("%H:%M:%S")+": Converting "+pdfFile+" to JPEG image format...");
		pdfToJPEG = "convert -density 175 -quality 100 "+pdfFile+" toBeProcessed/"+pdfFile[:-4]+".jpeg";
		subprocess.call(pdfToJPEG,shell=True);
            
    def readInfo(self,attributeName,left,upper,right,lower,singleCharacter=False):
        import os;
        from PIL import Image, ImageDraw;
		
		# Change the current working directory to the toBeProcessed directory.
	toBeProcessed_directory = "/mnt/hgfs/images/toBeProcessed";
        os.chdir(toBeProcessed_directory);
		
		# Crop the converted JPEG file according to the specified coordinates. This cropped image will be used to extract the information to be entered.
	filename = self.imagePath;
        print("Extracting "+attributeName+" from "+filename+" ... ");
        top = upper; bottom = lower;
        croppedFile = Image.open(filename);
        croppedFile.crop((left,upper,right,lower)).save(attributeName+".jpeg","JPEG");

		# Draw a rectangle on the converted JPEG file the corresponds to the cropped area that is being used to extract information. Save the JPEG file.
        drawRectangle = ImageDraw.Draw(croppedFile);
        drawRectangle.line((left,top)+(right,top),fill=128);
        drawRectangle.line((right,top)+(right,bottom),fill=128);
        drawRectangle.line((right,bottom)+(left,bottom),fill=128);
        drawRectangle.line((left,bottom)+(left,top),fill=128);
        del drawRectangle;
        croppedFile.save(filename,"JPEG");

		# Use tesseract to extract the relevant information from the cropped file. 
        import subprocess;
        tesseractCommand = "tesseract "+attributeName+".jpeg /mnt/hgfs/images/output";
		
		# If we have set the singleCharacter to "True", edit the teseractCommand such that the psm parameter is 10. This is necessary to process single character information.
        if singleCharacter:
            tesseractCommand = "tesseract -psm 10 "+attributeName+".jpeg /mnt/hgfs/images/output";
        
	# Run the tesseract command.
	subprocess.call(tesseractCommand,shell=True);

		# Open up the text file which holds the output from the above tesseract command & read the output. Then place that information inside of the OSR object where it can be accessed by other functions.
        with open('/mnt/hgfs/images/output.txt','r') as output_file:
            output = output_file.read();
        
	setattr(self,attributeName,output);

		# Delete cropped file.
        os.remove(attributeName+".jpeg");
        print(attributeName+": "+output);


# Define the element class, which represents the elements on the web page and provides methods to facilitate program interactions with those elements.
class element:
    def __init__(self,xCoord,yCoord,tag="input",type="text"):
        self.xCoord = xCoord;
        self.yCoord = yCoord;
        self.tag = tag;
        self.type = type;

	# Click on the x & y coordinates on the screen that corespond to those of the element.
    def click(self):
        import pyautogui;
        x = self.xCoord;
        y = self.yCoord;
        pyautogui.click(x,y,button='left');
    
	# Click on the x & y coordinates on the screen that correspond to those of the element and then type whatever is represented by the `value` variable.     
    def enterValue(self,value):
        import pyautogui;
        self.click();
        pyautogui.typewrite(value,0.1);

# Create an OSR object and set the following attributes to the OSR object.
pdf = OSR(pdf2convert,irbProtocol);
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
oncoreOSR_form = {"agent": element(777,212),"eventDate": element(975,212),"issuedDate": element(1189,212),"drugCompany": element(805,233), "reportNum": element(1025,233), "subjectDescription": element(718,255), "deathWithin": element(793,279), "hospital": element(1026,276,type="checkbox"),"followUpNum": element(1135,279), "reviwedDSMB": element(851,299), "sponsorComments": element(720,334), "toxicityCategory": element(723,416), "toxicity": element(867,415), "toxicityComments": element(1013,416), "toxicityGrade": element(1159,417), "addTox": element(1308,416,tag="button",type=""),"protocolNum": element(722,531), "recievedDate": element(864,530), "piNotified": element(1010,529), "attribution": element(1155,530), "piComments": element(1299,529), "icfChanged": element(794,345,type="checkbox"), "piSigned": element(725, 570), "notReportable": element(864,573,type="checkbox"), "reported2IRB": element(1011,570), "addTracking": element(1101,594,tag="button",type=""), "submitOSR": element(1272,628), "clearOSR": element(1324,628), "closeOSR": element(1372,628)};

#Match the data in the OSR to the appropriate element in the form. Then enter the appropriate values.
for data in rawOSR:
    print(data);
    oncoreOSR_form[data].enterValue(rawOSR[data]);

# Click the "Add" button in the toxicity section.
oncoreOSR_form["addTox"].click();

# Move the converted JPEG file into the archive folder.
convertedJPEG = pdf2convert[:-4]+".jpeg";

def archiveJPEG(convertedJPEG,openAfter=True):
	import random;
	import pyautogui;
	import time;
	import shutil;
	import re;
	from PIL import Image, ImageDraw, ImageFont;
	
	# Move the JPEG copy of the PDF file to the archive folder.	
	archivePath = "/mnt/hgfs/images/archive/";
	shutil.move(convertedJPEG,archivePath+convertedJPEG);
	archivedJPEG = Image.open(archivePath+convertedJPEG);
	draw = ImageDraw.Draw(archivedJPEG);

	# Import a font
	fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",40);
	
	# Move the cursor to the right-hand side of the screen, and save a copy of the completed OSR submission.
	pyautogui.moveTo(980,792,1);
	pyautogui.hotkey('ctrl','s');
	time.sleep(5);
	pyautogui.hotkey('enter');
	time.sleep(1);
	pyautogui.hotkey('enter');
	time.sleep(2);

	# Read the contents of the OSR.html file which we saved in the preceeding block of code. Scan the contents for the element that contains the OSR number assigned by the CTMS. 
	with file("/mnt/hgfs/images/OSR.html") as f:
    		html=f.read();
	osrNumber = re.findall("\>OSR# (.*)\<",html);

	# Write the OSR number from the preceeding block of code as well as a timestamp on the archived JPEG.
	draw.text((10,10),"OSR# "+osrNumber[0],font=fnt,fill='#000000');
	timestamp = time.strftime("%m-%d-%Y  %H:%M:%S");
	fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",20);
	draw.text((10,50),"Processed on: "+timestamp,font=fnt,fill="#000000");
	del draw;
	
	# Save the timestamped JPEG and get rid of the orginally archived one.
	archivedJPEG.save(archivePath+convertedJPEG[:-5]+"_osr"+osrNumber[0]+".jpeg","JPEG");
	os.remove(archivePath+convertedJPEG);

	# If the openAfter parameter has not been explicity set to false, open the archived JPEG.
	if openAfter == True:
		openProcessedOSR = "xdg-open "+archivePath+convertedJPEG[:-5]+"_osr"+osrNumber[0]+".jpeg";
		import subprocess;
		subprocess.call(openProcessedOSR,shell=True);


archiveJPEG(convertedJPEG);
# Print the current system time now that the execution of the script is complete.
print(time.strftime("%H:%M:%S")+": Script execution complete");
