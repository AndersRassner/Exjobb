import os
import sys
import re
import datetime
from time import sleep, time

def main():
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # pylint: disable=too-many-lines,maybe-no-member,c0103
    
    # variable declarations
    Weight = 1.00
    BlockTM = False
    RealTime = False
    Now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #NowStr = str(Now.hour()) + str(Now.minute()) + str(Now.second())
    SUMOBIN = "C:\\Sumo\\bin\\sumo.exe"
    SUMOBING = "C:\\Sumo\\bin\\sumo-gui.exe"

    ChosenTM = ""
    # Valid values are 960, 1600 and 2800
    CARAMOUNT = "2800"
    NOTM = "C:\\Users\\Anders\\Sumo\\big_" + CARAMOUNT + ".sumocfg"
    WEIGHTTM = "C:\\Users\\Anders\\Sumo\\big_weighted_" + CARAMOUNT + ".sumocfg"
    BLOCKCHAINTM = "C:\\Users\\Anders\\Sumo\\big_blockchain_" + CARAMOUNT + ".sumocfg"
    SumName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_" + CARAMOUNT + "_"
    LogName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_" + CARAMOUNT + "_"

    # simulation selection
    simulationToRun = raw_input("Which simulation type? 1=noTM, 2=weighted and 3=blockchain: ")
    if simulationToRun == '1':
        ChosenTM = NOTM
        LogName = LogName + "no_tm.log"
        SumName = SumName + "no_tm_sum.xml"
    elif simulationToRun == '2':
        ChosenTM = WEIGHTTM
        LogName = LogName + "weight_tm.log"
        SumName = SumName + "weight_tm_sum.xml"
    elif simulationToRun == '3':
        ChosenTM = BLOCKCHAINTM
        BlockTM = True
        LogName = LogName + "block_tm.log"
        SumName = SumName + "block_tm_sum.xml"
        filename = "link_big4_inner_edges_block.xml"
        edges = {}
        cars = []
        inputfile = open(filename)
        for line in inputfile:
            edge_id = re.findall(r"(?<=edge id\=\").+(?=\" trave)", line)
            traveltime = re.findall(r"(?<=traveltime\=\").+(?=\"/>)", line)
            if edge_id:
                edges[edge_id[0]] = float(traveltime[0])
        inputfile.close()
    else:
        sys.exit(-1)

    if raw_input("Run in real time y/n? ") == 'y':
        RealTime = True

    if raw_input("Run simulation in GUI y/n? ") == 'n':
        sumocommand = [SUMOBIN, "-c", ChosenTM, "--summary", SumName, "--duration-log.statistics"
                       , "--verbose", "--log", LogName]
    else:
        sumocommand = [SUMOBING, "-c", ChosenTM, "--summary", SumName, "--duration-log.statistics"
                       , "--verbose", "--log", LogName]

    # simulation starts
    import traci
    print sumocommand
    traci.start(sumocommand)
    Step = 0
    STEPEND = 10000
    #StepSim = True

    print "started bigpy.py"
    #t_end = time() + 30.0   # End of run
    t_end2 = time() + 1.0   # Step interval
    t_now = time()          # Present time
    #traci.multientryexit.subscribe("e3Detector_0")
    while Step < STEPEND and traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        Step += 1

        if BlockTM:
            # Average real-life time to clear inner ring is 8-16 minutes
            # depending on time of day and traffic.
            # Crudely simulated before smart contract by following line
            if Step%60 == 0 and Weight > 0.99:
                Weight -= 0.1
                if Weight < 1.00:
                    Weight = 1.00
                elif Weight > 2.00:
                    Weight = 2.00
            for carID in traci.simulation.getDepartedIDList():
                #cars.append(int(carID))
                traci.vehicle.rerouteTraveltime(carID, False)
                for edge in traci.vehicle.getRoute(carID):
                    if edge in edges:
                        traci.vehicle.rerouteTraveltime(carID, False)
                        # BUY PASSAGE
                        # RECALCULATE EDGE TIMES
                        Weight += 0.01
                        for edge2, traveltime in edges.iteritems():
                            traci.edge.adaptTraveltime(edge2, (traveltime * Weight))
                        break

        if RealTime:
            print "Step " + str(Step) + ": [Insert debug text]"
            while time() < t_end2:
                sleep(50.0 / 1000.0)
            t_end2 += 1.0
            t_now = time()
        elif Step%100 == 0 and BlockTM:
            print "Step " + str(Step) + ": Weight is currently " + str(Weight)

    print "ended bigpy.py at step " + str(Step)
    # DEBUG
    #print cars
    #print "Highest carID: " + str(max(cars))
    #print "Lowest carID: " + str(min(cars))
    # DEBUG END
    #print Step
    traci.close()

    sys.exit(0)

    print "Never print"

if __name__ == '__main__':
    main()
