from datetime import datetime
import bigpy

def main():
    """
    Runs all simulations including the real blockchain ones
    """
    # pylint: disable=too-many-lines,maybe-no-member,c0103
    MINIMUMTRAFFIC = '400'
    EVENLOWESTTRAFFIC = '600'
    LOWESTTRAFFIC = '800'
    LOWTRAFFIC = '1000'
    MEDIUMTRAFFIC = '1200'
    HIGHTRAFFIC = '1400'
    started = datetime.now()
    bigpy.main('1', '1', MINIMUMTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', MINIMUMTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '2', MINIMUMTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', EVENLOWESTTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', EVENLOWESTTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '2', EVENLOWESTTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', LOWESTTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', LOWESTTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '2', LOWESTTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', LOWTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', LOWTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '2', LOWTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', MEDIUMTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', MEDIUMTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '2', MEDIUMTRAFFIC)
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', HIGHTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', HIGHTRAFFIC)
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '2', HIGHTRAFFIC)
    print "\n[INFO]    Final runtime: " + str((datetime.now() - started)) + "\n"

if __name__ == '__main__':
    main()
