# Define the pdfForm class, which represents the pdf file that contains the data you wish to enter into the form.
class pdfForm:
    def __init__(self,pdfFile,toBeProcessedDir):
		03/01/2015


		# Set the filename for the JPEG that the PDF form will be converted to.
		self.imagePath = pdfFile[:-4]+".jpeg";
		self.toBeProcessedDir = toBeProcessedDir;
		# Convert pdfFile to a JPEG file with the same name, but stored in the toBeProcessed directory.
		import time, subprocess;
		print(time.strftime("%H:%M:%S")+": Converting "+pdfFile+" to JPEG image format...");
		pdfToJPEG = "convert -density 175 -quality 100 "+pdfFile+" "+pdfFile[:-4]+".jpeg";
		subprocess.call(pdfToJPEG,shell=T
y/Uprue);
            
    

Over def readInfo(self,attributeName,left,upper,right,lower,singleCharacter=False):
        import os;
        from PIL import Image, ImageDraw;
		
		# Change the current working directory to the toBeProcessed directory.
	toBeProcessed_directory = self.toBeProcessedDir;
	output_path = os.path.dirname(self.toBeProcessedDir)+"/output";
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
        tesseractCommand = "tesseract "+attributeName+".jpeg "+output_path;
		
		# If we have set the singleCharacter to "True", edit the teseractCommand such that the psm parameter is 10. This is necessary to process single character information.
        if singleCharacter:
            tesseractCommand = "tesseract -psm 10 "+attributeName+".jpeg "+output_path;
        
	# Run the tesseract command.
	subprocess.call(tesseractCommand,shell=True);

		# Open up the text file which holds the output from the above tesseract command & read the output. Then place that information inside of the pdfForm object where it can be accessed by other functions.
        with open(output_path+'.txt','r') as output_file:
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
