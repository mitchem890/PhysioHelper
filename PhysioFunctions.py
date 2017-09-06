import os

#merges the dictionaries to using the Keys in dict1 and the values from dict2
def mergeDictionaries(dict1, dict2):
    dictMerge = {}
    for key, value in dict1.items():
        dictMerge[key] = dict2[dict1[key]]
    return dictMerge

#Finds the longest value of the dictionary and returns the length
def FindMaxLengthValue(dictionary):
    keyLongestName = max(dictionary, key = lambda k: len(dictionary[k]))
    return len(dictionary[keyLongestName])


# Build Matrix String based on
# runnames = [['Axcpt' sessidshort '1_AP ']; ['Axcpt' sessidshort '2_PA '];
#             ['Cuedts' sessidshort '1_AP']; ['Cuedts' sessidshort '2_PA'];
#             ['Stern' sessidshort '1_AP ']; ['Stern' sessidshort '2_PA '];
#             ['Stroop' sessidshort '1_AP']; ['Stroop' sessidshort '2_PA']];
# if Physio file for scan doesnt exist it will be replaced with a blank space
# all stings within an array must be the same length so padding is added on to the end of the file names and the
def BuildMatrix(dict1):
    maxLength = FindMaxLengthValue(dict1)

    ExpectedTrialList = ['Axcpt1_AP', 'Axcpt2_PA','Cuedts1_AP', 'Cuedts2_PA',\
                         'Stern1_AP', 'Stern2_PA', 'Stroop1_AP','Stroop2_PA']
    uuidMatrix = '['
    runnames = '['
    for trial in ExpectedTrialList:
        if trial in dict1:

            uuidMatrix = uuidMatrix + '\''+dict1[trial].ljust(maxLength)+'\';'
            run = trial[:-4] + '\' sessidshort \'' + trial[-4:]
            runnames = runnames + '[\'' + run.ljust(25) + '\'];'

            if '2' in trial:
                uuidMatrix = uuidMatrix + '\n\t\t'
                runnames = runnames + '\n\t\t\t'

    uuidMatrix = uuidMatrix + '];\n'
    runnames = runnames + '];\n'

    return uuidMatrix, runnames


def GetPhysioData(project, subject, session):
    # Get the list of physio Files and store in to tmp.csv
    os.system("curl -s -k -n https://intradb.humanconnectome.org/data/projects/" + project + "/subjects/" \
              + subject + "/experiments/" + subject + "_" + session + \
              "/scans?format=csv | grep \"Physio\" | cut -d, -f7,8 > tmp.csv")

def DownloadPhysioFiles(directory, project, subject, session):
    print 'Downloading Physio Data from intraDB:'
    os.system('bash intraDBPhysioDownload.sh -s ' + subject + ' -e ' + session + ' -p ' + project + ' -d ' + directory)


#makes a CSVs with the UUIDS and scan Numbers
def findUUIDs(sn, project, subject, session):
    baseScanNumber = [int(numbers) - 1 for numbers in sn]
    print baseScanNumber
    os.system('curl -k -n https://intradb.humanconnectome.org/data/projects/' + project + '/subjects/' + subject + \
              '/experiments/' + subject + '_' + session + '/scans?format=csv\&columns=xnat:mrScanData/fileNameUUID>UUID.csv')
