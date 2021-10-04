#---------------------------------------------------------------------------------------------------------------------
# Very important note: This must be run in Python 3 due to the printing syntax I use to keep things on the same line
# Command: python3 NB.py
#---------------------------------------------------------------------------------------------------------------------

import sys
import math

#This fucntion parses a single line of a file
#Essentially goes through charachter by charachter and only keeps ones that are in the alphabet, also makes everything lower case
#REturns a new string with only the good parts of the origional
def parseLine(line):
	valChar = []
	for i in range(0, len(line)):
		asci = ord(line[i])
		if (asci >= 65 and asci <= 90) or (asci >= 97 and asci <= 122) or asci == 32:#Only take in letters 
			if (asci >= 65 and asci <=90):#Turn the upper case into lower case
				asci += 32
			valChar.append(chr(asci))

	valChar.pop(-1)
	valChar.pop(-1)
	if line[-3] == '1':#Add back on the class label to the end
		valChar.append('1')
	else:
		valChar.append('0')
	parsed = "".join(valChar) #Join everything back together
	return parsed

#This fucntion writes out the preprocessed data to a file
#This function takes in the preprocessed data, the vocab, and the file to output to
#This function returns nothing
def outputPreproc(preproc, vocab, outfile):
	sys.stdout = open(outfile, 'w')#Redirect stdout to a file
	for i in range(0, len(vocab)):
		if i != len(vocab):
			#sys.stdout.write(vocab[i] + ",")
			print(vocab[i], end = ",")
	print("classlabel")
			#sys.stdout.write(vocab[i] + "\n")
	for i in range(0, len(preproc)):
		for j in range(0, len(preproc[i])):
			if j != len(preproc[i]) - 1:
				#sys.stdout.write(str(preproc[i][j]) + ",")
				#sys.stdout.write(",")
				print(preproc[i][j], end = ",")
			else:
				#sys.stdout.write(str(preproc[i][j]) + "\n")
				print(preproc[i][j])
	sys.stdout = open("/dev/stdout", 'w')
	return

#This fuction featurizes the data by putting marking 1's and 0's for which words from the vocab are in the current sentece
#This function takes in the parsedLiens which is an array of words in the sentence, as well as the vocab
#This fucntion returns a featurized form of every sentence in the parsed lines
def featurizeData(parsedLines, vocab):
	preproc = []
	for i in range(0, len(parsedLines)):
		featurized = []
		classLabel = parsedLines[i].pop(-1)
		for j in range(0, len(vocab)):#Go through the vocab and add a 1 if the word is in the parsed and 0 if not
			if vocab[j] in parsedLines[i]:
				featurized.append(1)
			else:
				featurized.append(0)
		featurized.append(int(classLabel))#Finally add the class label to the end
		preproc.append(featurized)
	return preproc

	
#This function processes the training data and the vocabulary
#This function reads in the training set and parses each line in the file, then creates the vocab by adding words that are in the sentences
#This function returns the covab and the preprocessed training data
def procTraining():
	f = open("trainingSet.txt", 'r')
	parsedLines = []
	vocab = []
	counter = 0
	for line in f:#Iterate through each line in the file
		parsed = parseLine(line).split()
		for word in parsed:#Also iterates through the parsed line and adds the word to the vocab if its not already there
			if word not in vocab and word != parsed[-1]:
				vocab.append(word)
		parsedLines.append(parsed)
		counter += 1

	vocab.sort()#Sort the vocab

	preproc = featurizeData(parsedLines, vocab)#Finalize the preprocesesing by featurizing the training data
	return vocab, preproc

#This fucntion calculates the probability of the class label (It being a good review)
#This fcuntion takes in the data which is the parsed lines
#This function returns the probability that the class label is true (Prob of it being a good review)
def calculateCL(data):
	classSum = 0
	for i in range(0, len(data)):
		classSum += data[i][-1]

	return float(classSum) / float(len(data))

#This function creates the confusion matrix which is each possible combination of the conditional probability P(Word | Class Label)
#This funciton takes in the training data and calculates the different probability for each word appearing in the vocab
#This function returns the confusion matrix called accuracies. (An array which each element being a list of the 4 possible conditional probabilities)
def createCM(data):
	accuracies = []

	for i in range(0, len(data[0])):
		sumNotCLFeat = sumCLFeat = sumCLNotFeat = sumNotCLNotFeat = 0 #Initialize the 4 conditional probability values 

		sumCL = sumNotCL = 0
		for j in range(0, len(data)):
			if data[j][-1] == 1:
				sumCL += 1
			else:
				sumNotCL += 1

			if data[j][i] == 1 and data[j][-1] == 1: #P(Word | Class Label)
				sumCLFeat += 1
			elif data[j][i] == 0 and data[j][-1] == 1: #P(~Word | Class Label)
				sumCLNotFeat += 1
			elif data[j][i] == 1 and data[j][-1] == 0: #P(Word | ~Class Label)
				sumNotCLFeat += 1
			elif data[j][i] == 0 and data[j][-1] == 0: #P(~Word | ~Class Label)
				sumNotCLNotFeat += 1
		condProb = []
		condProb.append(float(sumNotCLNotFeat + 1)/ float(sumNotCL + 2)) #Claculates the probability with uniform priors
		condProb.append(float(sumCLNotFeat + 1)/ float(sumCL + 2))
		condProb.append(float(sumNotCLFeat + 1)/ float(sumNotCL + 2))
		condProb.append(float(sumCLFeat + 1)/ float(sumCL + 2))
		accuracies.append(condProb)
	return accuracies

#Accuracies:
#index 0: false given false
#index 1: false given true
#index 2: true given false
#index 3: true given true
#This function calculates the accuracy of knowledge base for being able to predict whether a review is positive or negative.
#This funciton takes in the confusion matrix, the preprocessed data, the class label probability, and the names of the training file and testing file
#This function returns nothing but prints out the accuracy of the model and which files were used for training and testing
def trainPred(accuracies, trainProc, CLProb, trainingSet, testingSet):
	right = 0
	#print(CLProb)

	for i in range(0, len(trainProc)):
		classOneSum = 0
		classZeroSum = 0
		guess = 0
		for j in range(0, len(trainProc[0])-1):
			if trainProc[i][j] == 1:
				xGivenNotY = accuracies[j][2] #P(Word | ~Class Label)
				xGivenY = accuracies[j][3]    #P(Word | Class Label)
			else:
				xGivenNotY = accuracies[j][0] #P(~Word | ~Class Label)
				xGivenY = accuracies[j][0]    #P(Word | Class Label)
			classOneSum += math.log(xGivenY)
			classZeroSum += math.log(xGivenNotY)
		classOneSum += math.log(CLProb)
		classZeroSum += math.log(1 - CLProb)

		#classZeroSum += 0.1

		#If class One is bigger than class two and the class label is 1 then it is correct, same if they are both 0
		if (classOneSum >= classZeroSum and trainProc[i][-1] == 1) or (classZeroSum > classOneSum and trainProc[i][-1] == 0):
			right += 1
	print("Accuracy: " + str(float(right) / float(len(trainProc))))
	print("Training on " + trainingSet + ", and testing on " + testingSet)
	#testResults(accuracies, testProc, CLProb)

	return

def main():
	f = open("testSet.txt", 'r')
	parsedLines = []
	for line in f:
		parsed = parseLine(line).split()
		parsedLines.append(parsed)
	f.close()
	
	vocab, trainProc = procTraining()
	testProc = featurizeData(parsedLines, vocab)
	outputPreproc(trainProc, vocab, "preprocessed_train.txt")
	outputPreproc(testProc, vocab, "preprocessed_test.txt")


	probCL = calculateCL(trainProc)
	#probNewCL = calculateCL(testProc)
	CM = createCM(trainProc)
	
	sys.stdout = open("results.txt", 'w')
	trainPred(CM, trainProc, probCL, "trainingSet.txt", "trainingSet.txt")
	print("")
	trainPred(CM, testProc, probCL, "trainingSet.txt", "testSet.txt")
	sys.stdout = open("/dev/stdout", 'w')

	return

main()
