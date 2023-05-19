from kodeerimine import dekodeeri_seifidest, kodeeri_seifidesse
import argparse
from failid import *

def main():
    # Saame argumendid
    parser = argparse.ArgumentParser(
        prog='MELLON',
        description='Mitme failiga korraga töötav steganograafia programm.')
    parser.add_argument('--saladused', nargs='+')
    parser.add_argument('--seifid', nargs='+')
    parser.add_argument('--dekodeeri_faili', nargs='?', default="")
    args = parser.parse_args()

    saladuse_failid = args.saladused
    seifi_failid = args.seifid
    dekodeerimisfail = args.dekodeeri_faili

    if dekodeerimisfail != "":
        dekodeeri_seifidest(seifi_failid, dekodeerimisfail)
    else:
        kodeeri_seifidesse(seifi_failid, saladuse_failid)

if __name__ == "__main__":
    main()
