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
    BlockTM = False
    RealTime = False
    Now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #NowStr = str(Now.hour()) + str(Now.minute()) + str(Now.second())
    SUMOBIN = "C:\\Sumo\\bin\\sumo.exe"
    SUMOBING = "C:\\Sumo\\bin\\sumo-gui.exe"

    ChosenTM = ""
    NOTM = "C:\\Users\\Anders\\Sumo\\big.sumocfg"
    WEIGHTTM = "C:\\Users\\Anders\\Sumo\\big_weighted.sumocfg"
    BLOCKCHAINTM = "C:\\Users\\Anders\\Sumo\\big_blockchain.sumocfg"
    SumName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_"
    LogName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_"

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
        cars = {}
        inputfile = open(filename)
        for line in inputfile:
            edge_id = re.findall(r"(?<=edge id\=\").+(?=\" trave)", line)
            traveltime = re.findall(r"(?<=traveltime\=\").+(?=\"/>)", line)
            if edge_id:
                edges[edge_id[0]] = traveltime[0]
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
            for carID in traci.simulation.getDepartedIDList():
                if carID in cars:
                    cars[carID] += 1
                else:
                    cars[carID] = 1
                for edge in traci.vehicle.getRoute(carID):
                    if edge in edges:
                        traci.vehicle.rerouteTraveltime(carID, False)
                        break
                        #print "rerouted. "
            #if Step % 100 == 0:

        if RealTime:
            while time() < t_end2:
                sleep(50.0 / 1000.0)
            t_end2 += 1.0
            t_now = time()
    # Old testcode from simplepy.py
    #   e3Sub = traci.multientryexit.getSubscriptionResults()
    #   curInnerCount = e3Sub["e3Detector_0"][16]

        # DEBUG/TINKERING OUTPUTS
        #if e3Sub["e3Detector_0"][16] != 0:
            #print e3Sub["e3Detector_0"]
            #print traci.multientryexit.getLastStepVehicleIDs("e3Detector_0")
            #print traci.vehicle.getIDList()

        # MAX 10 VEHICLES ON INNER ROAD!
    #   if curInnerCount > 9:
    #       for vehicle in traci.vehicle.getIDList():
    #           if vehicle not in traci.multientryexit.getLastStepVehicleIDs("e3Detector_0"):
                    # Change route
    #                traci.vehicle.rerouteTraveltime(vehicle)
                    # print "Changed route somehow"

    #    if StepSim:
    #        if raw_input("Keep stepping through simulation y/n?") == 'n':
    #            StepSim = False

    #for val in e3Sub["e3Detector_0"]:
    #    print val
    print "ended bigpy.py at step " + str(Step)
    #print Step
    traci.close()

    # DEBUG
    for key in cars:
        if cars[key] > 1:
            print key + str(cars[key])
    # DEBUG END
    sys.exit(0)

    print "Never print"

if __name__ == '__main__':
    main()
