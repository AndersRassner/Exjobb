from datetime import datetime
import bigpy

def main():
    """
    Runs all simulations including the simulated blockchain ones
    """
    # pylint: disable=too-many-lines,maybe-no-member,c0103
    started = datetime.now()
    bigpy.main('1', '1', '960')
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', '960')
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', '960')
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', '1600')
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', '1600')
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', '1600')
    print "\n[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('1', '1', '2800')
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('2', '1', '2800')
    print "[INFO]    Current runtime: " + str((datetime.now() - started)) + "\n"
    bigpy.main('3', '1', '2800')
    print "\n[INFO]    Final runtime: " + str((datetime.now() - started)) + "\n"

if __name__ == '__main__':
    main()
