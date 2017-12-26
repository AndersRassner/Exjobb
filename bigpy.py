import os
import sys
import re
import datetime
from time import sleep, time
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
# TODO: replace float() castings to the more future safe from __future__ import divison

def main(simtorun_, realtime_, caramount_="400"):
    """Runs a simulation using sumo and config files.

    Args:
        simtorun_ -- 1, 2 or 3 which corresponds to no-, weighted- or block-TM
        realtime_ -- 1 or 2 where 1 means don't run in realtime and 2 means run in realtime
        caramount_ -- 400, 600, 800, 960, 1000, 1200, 1400, 1600, 2400 or 2800
    """
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # pylint: disable=too-many-lines,maybe-no-member,c0103
    # variable declarations
    Weight = 1.00
    CarsOnInner = 0

    edges = {}
    filename = "link_big4_inner_edges_block.xml"
    inputfile = open(filename)
    for line in inputfile:
        edge_id = re.findall(r"(?<=edge id\=\").+(?=\" trave)", line)
        traveltime = re.findall(r"(?<=traveltime\=\").+(?=\"/>)", line)
        if edge_id:
            edges[edge_id[0]] = float(traveltime[0])
    inputfile.close()
    BlockTM = False
    RealTime = False
    Now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #NowStr = str(Now.hour()) + str(Now.minute()) + str(Now.second())
    SUMOBIN = "C:\\Sumo\\bin\\sumo.exe"
    SUMOBING = "C:\\Sumo\\bin\\sumo-gui.exe"

    ChosenTM = ""
    # Valid values are 400, 600, 800, 960, 1000, 1200, 1400, 1600, 2400 and 2800
    CARAMOUNT = caramount_
    NOTM = "C:\\Users\\Anders\\Sumo\\big_" + CARAMOUNT + ".sumocfg"
    WEIGHTTM = "C:\\Users\\Anders\\Sumo\\big_weighted_" + CARAMOUNT + ".sumocfg"
    BLOCKCHAINTM = "C:\\Users\\Anders\\Sumo\\big_blockchain_" + CARAMOUNT + ".sumocfg"
    SumName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_" + CARAMOUNT + "_"
    LogName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_" + CARAMOUNT + "_"
    BlockLogName = "C:\\Users\\Anders\\Sumo\\logs\\" + Now + "big_" + CARAMOUNT + ".log"
    RatioName = "C:\\Users\\Anders\\Sumo\\logs\\ratio.log"
    RatioString = ""

    # simulation selection
    #simulationToRun = raw_input("Which simulation type? 1=noTM, 2=weighted and 3=blockchain: ")
    simulationToRun = simtorun_
    if simulationToRun == '1':
        ChosenTM = NOTM
        LogName = LogName + "no_tm.log"
        SumName = SumName + "no_tm_sum.xml"
        RatioString = "noTM - "
    elif simulationToRun == '2':
        ChosenTM = WEIGHTTM
        LogName = LogName + "weight_tm.log"
        SumName = SumName + "weight_tm_sum.xml"
        RatioString = "weightedTM - "
    elif simulationToRun == '3':
        ChosenTM = BLOCKCHAINTM
        BlockTM = True
        LogName = LogName + "block_tm.log"
        SumName = SumName + "block_tm_sum.xml"
        RatioString = "blockchainTM - "
        cars = []
        web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
        MyContract = web3.eth.contract([{"constant":True,"inputs":[],"name":"maxTraffic","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"priceRatio","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"zeroCurrentTraffic","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[],"name":"withdrawBalance","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getMaxPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"currentPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"newMaxTraffic","type":"uint256"}],"name":"setMaxTraffic","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"timeSinceLoweredTraffic","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"buyPassage","outputs":[],"payable":True,"stateMutability":"payable","type":"function"},{"constant":True,"inputs":[],"name":"maxPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getCurrentPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"newMaxPrice","type":"uint256"}],"name":"setMaxPrice","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"currentTraffic","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"inputs":[{"name":"initMaxTraffic","type":"uint256"},{"name":"initMaxPrice","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"}]
        )
        MyContract.address = '0xa6da455b1d90d4d2e7f463e5e7a91a101416a4eb'

        BlockLogString = "Contract Address: " + MyContract.address + "\n"
        # Unlock first 3 accounts if not unlocked.    
        web3.personal.unlockAccount(web3.personal.listAccounts[0], 'traffic', 10000)
        web3.personal.unlockAccount(web3.personal.listAccounts[1], 'traffic', 10000)
        web3.personal.unlockAccount(web3.personal.listAccounts[2], 'traffic', 10000)
        MyContract.call().zeroCurrentTraffic()
        cur_price = MyContract.call().getCurrentPrice()
        cur_traffic = MyContract.call().currentTraffic()
        # Max Price/Traffic assumed constant, otherwise should be added to simulation loop
        max_traffic = MyContract.call().maxTraffic()
        #cur_max = MyContract.call().getMaxPrice()


    else:
        sys.exit(-1)

    #if raw_input("Run in real time y/n? ") == 'y':
    if realtime_ == '2':
        RealTime = True
    sumocommand = [SUMOBIN, "-c", ChosenTM, "--summary", SumName, "--duration-log.statistics"
                   , "--verbose", "--log", LogName]
    #if raw_input("Run simulation in GUI y/n? ") == 'n':
    #    sumocommand = [SUMOBIN, "-c", ChosenTM, "--summary", SumName, "--duration-log.statistics"
    #                   , "--verbose", "--log", LogName]
    #else:
    #    sumocommand = [SUMOBING, "-c", ChosenTM, "--summary", SumName, "--duration-log.statistics"
    #                   , "--verbose", "--log", LogName]

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
                #cars.append(int(carID))
                traci.vehicle.rerouteTraveltime(carID, False)
                for edge in traci.vehicle.getRoute(carID):
                    if edge in edges:
                        # Why reroute again?
                        # traci.vehicle.rerouteTraveltime(carID, False)
                        
                        # BUY PASSAGE
                        cur_price = MyContract.call().getCurrentPrice()
                        estimatedGas = 2*(web3.eth.estimateGas({'to': MyContract.address, 'from': web3.eth.accounts[1], 'value': cur_price}))
                        try:
                            transaction_ = MyContract.transact({'from': web3.eth.accounts[1], 'value': estimatedGas+cur_price}).buyPassage()
                        except ValueError:
                            BlockLogString += "\n\n****\nValueError\n****\n\n"
                            print "\n\n****\nValueError\n****\n\n"
                        cur_traffic = MyContract.call().currentTraffic()
                        Weight = 1 + (cur_traffic / float(max_traffic))

                        # RECALCULATE EDGE TIMES
                        for edge2, traveltime in edges.iteritems():
                            traci.edge.adaptTraveltime(edge2, (traveltime * Weight))
                        break
            """ Crudely simulated before smart contract by following lines
            # Average real-life time to clear inner ring is 8-16 minutes
            # depending on time of day and traffic.
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
            """

        # Keep track of ratio on inner ring
        for carID in traci.simulation.getDepartedIDList():
            for edge in traci.vehicle.getRoute(carID):
                if edge in edges:
                    CarsOnInner += 1
                    break

        if RealTime:
            RealTimeString = "Step " + str(Step)
            RealTimeString += "\ncur_traffic   = " + str(cur_traffic)
            RealTimeString += "\ncur_price     = " + str(cur_price)
            RealTimeString += "\nWeight        = " + str(Weight)
            RealTimeString += "\n"
            print RealTimeString
            
            BlockLogString += RealTimeString
            
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
    with open(RatioName, "a") as ratiofile:
        ratiofile.write("\n" + RatioString + Now)
        ratiofile.write("\nTotal Cars: " + str(CARAMOUNT))
        ratiofile.write("\nInner Cars: " + str(CarsOnInner))
        ratiofile.write("\nRatio:      " + str(float(CarsOnInner)/float(CARAMOUNT)) + "\n")
    print "Wrote Ratio to " + RatioName
    if(BlockTM):
        with open(BlockLogName, "w") as blocklogfile:
            blocklogfile.write("\n\n" + BlockLogString + Now + "\n")
        print "Wrote BlockChainLog to " + BlockLogName
    return

if __name__ == '__main__':
    print __name__
    if len(sys.argv) != 3:
        print "Please call this program with 2 arguments"
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2], '400')
    sys.exit(0)
