import argparse
import math
import copy


#This function is the setup for user input
def parseArguments():
    parser = argparse.ArgumentParser(description="CPU Scheduler Simulator")

    #The input file we are pulling from
    parser.add_argument(
        "input_file",
        help=
            "The input text file contains contents for a CPU scheduler")

    #what kind of scheduler are we using
    parser.add_argument(
        "scheduler",
        choices=['FCFS', 'RR', 'SJF'],
        help=
            "Chose FCFS/RR/SJR for which scheduler you would like to choose.")

    #creating optional argument for RR
    parser.add_argument(
        "quantum",
        nargs='*',
        help=
            "Enter an integer that represents the time quantum for the Round Robin scheduler.")

    args = parser.parse_args()

    return args

#main function
def main():
    args = parseArguments()

    #Open the file and parse its contents
    with open(args.input_file, 'r') as file:
        data = file.read().split("\n")

    #Simulate The Scheduler
    data = schedule(data, args)
    
    #Error Checker
    if data == 0:
        return 0

    #Print Scheudler (The if statement covers the RR output)
    if data[0]:
        print("PID\tStart Time\tEnd Time\tRunning Time\n")
        print(''.join(data[0]))
    print("PID\tArrival Time\tStart Time\tEnd Time\tRunning Time\tWaiting Time\n")
    print(''.join(data[1]))

#Simulating the Scheduler
def schedule(data, args):
    sType = args.scheduler
    numLines = int(data[0])

    #initializing simulating variables
    allInfo = []
    subFinal = []
    final = []
    totalTime = 0
    startTime = 0
    endTime = 0
    runTime = 0
    waitTime = 0
    leftTime = 0

    #adding up total time
    for i in range(1, numLines+1, 1):
        info = data[i].split("\t")
        allInfo.append(info)
        totalTime += int(info[2])

    #Sorting the processes by Arrival Time
    allInfo = sorted(allInfo, key=lambda x: x[1])

    #First Come First Serve
    if sType == 'FCFS':
        allInfo = sorted(allInfo, key=lambda x: x[1])

        #Since they are ordered by arrival time, they will be scheduled in that order
        for i in range(0, numLines, 1):
            endTime = startTime + int(allInfo[i][2])
            runTime = int(allInfo[i][2])
            waitTime = startTime - int(allInfo[i][1])
            final.append(f"{allInfo[i][0]}\t\t{allInfo[i][1]}\t\t{startTime}\t\t{endTime}\t\t{runTime}\t\t{waitTime}\n")
            startTime += int(allInfo[i][2])
        return subFinal, final

    #Round-Robin
    elif sType == 'RR':

        #Check to see if there is a quantum
        if not args.quantum:
            print("No Quantum Value Provided")
            return 0

        #Initializing the lists
        skip = []
        subFinal = []

        #Making a copy of the processes to update with the quantum
        processes = copy.deepcopy(allInfo)
        j = 0

        #While Loop simulating the total time that can be dedicated
        while int(startTime) <= int(totalTime):
            if startTime >= totalTime:
                break
            tempq = int(args.quantum[0])
            q = int(args.quantum[0])
    
            #The current index
            curr = j % numLines
            if curr in skip:
                j += 1
                continue

            #Updating the remianing Time needed to complete a process
            processes[curr][2] = int(processes[curr][2]) - tempq

            #IF process is completed, remove the process form schedule
            if processes[curr][2] < 0:
                tempq = q - abs(processes[curr][2])
                skip.append(curr)

            #Append to the final scheudle once completed
            if int(processes[curr][2]) <= 0:
                endTime = startTime + tempq
                runTime = int(allInfo[curr][2])
                waitTime = ((startTime + tempq) - int(allInfo[curr][1])) - int(allInfo[curr][2])
                final.append(f"{allInfo[curr][0]}\t\t{allInfo[curr][1]}\t\t{startTime}\t\t{endTime}\t\t{runTime}\t\t{waitTime}\n")
                endTime = startTime
                runTime = tempq
            endTime = startTime + tempq
            runTime = tempq

            #Update the RR Schedule as well
            subFinal.append(f"{allInfo[curr][0]}\t\t{startTime}\t\t{endTime}\t\t{runTime}\n")
            startTime += tempq
            j += 1        
        final = sorted(final, key=lambda x: x.split("\t\t")[0])
        return (subFinal,final)

    #Shortest Job First
    elif sType == 'SJF':

        #First job arrives first, so immediatly process it
        firstJob = allInfo.pop(0)

        #Sort the rest of the processes by its burst time
        allInfo = sorted(allInfo, key=lambda x: x[2])
        endTime = startTime + int(firstJob[2])
        runTime = int(firstJob[2])
        waitTime = startTime - int(firstJob[1])

        #Complete the processes
        final.append(f"{firstJob[0]}\t\t{firstJob[1]}\t\t{startTime}\t\t{endTime}\t\t{runTime}\t\t{waitTime}\n")
        startTime += int(firstJob[2])
        for i in range(0, numLines - 1, 1):
            endTime = startTime + int(allInfo[i][2])
            runTime = int(allInfo[i][2])
            waitTime = startTime - int(allInfo[i][1])
            final.append(f"{allInfo[i][0]}\t\t{allInfo[i][1]}\t\t{startTime}\t\t{endTime}\t\t{runTime}\t\t{waitTime}\n")
            startTime += int(allInfo[i][2])
        return subFinal, final
    else:
        print("Invalid Scheduler Type!")
        return 0
    return 0
main()
