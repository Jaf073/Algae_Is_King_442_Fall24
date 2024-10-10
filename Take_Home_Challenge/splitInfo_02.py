'''
ooohhh fancy credits up here ooohhhh
made by the footman at 8:46pm 10/8/24
'''
import sys

'''Modify the names into pretty String'''
def getName(name):
    #Find first Dash to split string into First and Last name
    Dash = name.index('-')

    #Get first Name
    firstName = name[:Dash]
    #Uppercase First Letter
    firstName = firstName[0].upper() + firstName[1:]

    #Find index where last name ends
    if '-' in name[Dash+1:]:
        end = Dash + name[Dash+1:].index('-') + 1 
    else:
        end = len(name)-2
        
    lastName = name[Dash+1:end]
    #Uppercase First Letter
    lastName = lastName[0].upper() + lastName[1:]

    #Make full name and return
    newName = firstName + " " + lastName
    return newName

def getEmail(email):
    stop = email.index("\n")
    return(email[:stop])
                       
'''Open Folder and Split information into emails and names'''
def splitInfo(filename):
    count = 0
    sets = 0
    nameDict1 = {}
    nameDict2 = {}
    nameDict3 = {}
    
    with open(filename) as f:
        for x, line in enumerate(f, start=0): #enumerate file into strings
            if line[:6] == '/name/': #Check if string is a name
                name = getName(line[6:])
            elif line[:6] == 'mailto': #Check if string is emal
                email = getEmail(line[7:])
                    
                #If we have the email, we have the name
                if (len(nameDict1) <= 150):
                    nameDict1[name] = email
                elif (len(nameDict2) <= 150):
                    nameDict2[name] = email
                else:
                    nameDict3[name] = email
                sets += 1
                    
            count += 1
    print(count)
    print(sets)
    return(nameDict1, nameDict2, nameDict3)

Dic1, Dic2, Dic3 = splitInfo('finished')
print(Dic1)
print("---------------")
print(Dic2)
print("---------------")
print(Dic3)
