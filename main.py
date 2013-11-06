#Turing-Post Language Simulator
#
#By Greg Wicks


import os
from time import sleep

def encodeMachine(structs,data,outfile):
    output = open(outfile,"w")
    for struct in structs:
        if struct == "STOP":
            output.write("00000000")
        elif struct == "PRINT 0":
            output.write("00000001")
        elif struct == "PRINT 1":
            output.write("00000010")
        elif struct == "RIGHT":
            output.write("00000011")
        elif struct == "LEFT":
            output.write("00000100")
        elif struct == "FLIP":
            output.write("00000101")
    
    output.write("|")

    for bit in data:
        output.write(str(bit))
    output.close()

def decodeStructs(infile):
    instructDict = {"00000000":"STOP","00000001":"PRINT 0","00000010":"PRINT 1","00000011":"RIGHT","00000100":"LEFT","00000101":"FLIP"}
    readfile = open(infile,"r")
    line = readfile.readline()
    line = line.split("|")
    line = line[0]
    iterator = 0
    retArr = []
    while iterator < len(line):
        instruction = line[iterator:iterator + 8]
        instruction = instructDict[instruction]
        retArr.append(instruction)
        iterator += 8
    readfile.close()
    return retArr

def decodeData(infile):
    readfile = open(infile,"r")
    line = readfile.readline()
    line = line.strip('\n')
    line = line.split("|")
    line = line[1]
    retArr = []
    for char in line:
        retArr.append(int(char))
    return retArr


def main(instructs,data):
    pc = 0
    sp = 0

    while pc < len(instructs) and sp <= len(data):
        instruct = instructs[pc]
        currVal = data[sp-1]
        if pc == len(instructs) - 1:
            if instruct == "STOP":
                break
            else:
                pc = -1

        if instruct == "STOP":
            break
        elif instruct == "PRINT 1":
            pc += 1
            data[sp-1] = 1
        elif instruct == "PRINT 0":
            pc += 1
            data[sp-1] = 0
        elif instruct == "RIGHT":
            pc += 1
            sp += 1
        elif instruct == "LEFT":
            pc += 1
            sp += -1
        elif instruct == "FLIP":
            pc += 1
            if sp != 0:
                if data[sp-1] == 0:
                    data[sp-1] = 1
                else:
                    data[sp-1] = 0
        elif "IF" in instruct:
            targetval = int(instruct[3])
            printval = int(instruct[16])
            if data[sp-1] == targetval:
                pc += 1
                data[sp-1] = printval
            else:
                pc += 1
        dp = sp*3 - 1
        if sp == len(data) + 1:
            break
        os.system('cls')
        os.system('clear')
        print("Prog Counter: ",pc)
        print("Instruct: ",instruct)
        print("Stack Pointer:",sp)
        formatStr = '|'.rjust(dp)
        print(formatStr)
        print(data)
        sleep(1)

def progShell():
    validInstructs = ["STOP","PRINT 0","PRINT 1","FLIP","IF 0 THEN PRINT 1","IF 1 THEN PRINT 0","RIGHT","LEFT"]
    print("Turing Post Language Shell")
    print("Type FINISH when done editing program")
    newInst = ""
    newInstructs = []
    while newInst != "FINISH":
        newInst = input(">>> ")
        if newInst in validInstructs:
            newInstructs.append(newInst)
        elif newInst == "HELP":
            print(validInstructs)
        else:
            print("Invalid Instruction")
    return newInstructs

def dataShell():
    print("Data Entry")
    print("Please enter comma-separated 0's and 1's to enter data")
    dat = input(">>> ")
    strArr = dat.split(',')
    retArr = []
    for item in strArr:
            retArr.append(int(item))
    return retArr

def mainMenu(ins,dat):
    selection = 0
    mainins = ins
    maindat = dat
    while selection != 6:
        print("")
        print("Turing Post Language Simulator")
        print("-"*50)
        print("Machine:",mainins)
        print("Data:",maindat)
        print("1) Enter instructions")
        print("2) Enter data")
        print("3) Load Machine")
        print("4) Save Machine")
        print("5) Run")
        print("6) Quit")
        print("")

        selection = int(input("Enter selection: "))
        if selection == 1:
            mainins = progShell()
        if selection == 2:
            maindat = dataShell()
        if selection == 3:
            filename = input("Enter filename: ")
            mainins = decodeStructs(filename)
            maindat = decodeData(filename)
        if selection == 4:
            filename = input("Enter filename: ")
            encodeMachine(mainins,maindat,filename)
        if selection == 5:
            main(mainins,maindat)

instructsin = ["FLIP","RIGHT"]
datain = [0,1,1,0,0,0,0,0]

mainMenu(instructsin,datain)
