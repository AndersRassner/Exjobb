from datetime import datetime
import bigpy

def main():
    """
    Runs all simulations including the simulated blockchain ones
    """
    # pylint: disable=too-many-lines,maybe-no-member,c0103
    LOWESTTRAFFIC = '800'
    LOWTRAFFIC = '1000'
    MEDIUMTRAFFIC = '1200'
    HIGHTRAFFIC = '1400'
    started = datetime.now()
    bigpy.main('1', '1', LOWESTTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', LOWESTTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', LOWESTTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', LOWTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', LOWTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', LOWTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', MEDIUMTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', MEDIUMTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', MEDIUMTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', HIGHTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', HIGHTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', HIGHTRAFFIC)
    print "\n[INFO]    Final runtime: " + str((datetime.now() - started)) + "\n"

if __name__ == '__main__':
    main()
