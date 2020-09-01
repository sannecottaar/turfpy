# TRAVEL TIME PREDICTION SCRIPT FOR RF ANALYSIS#################
# This script computes predicted travel times for user defined phases based on TauP
# Predicted times are added to the events header information

# Example: python3 3_add_travel_times P S P660s P410s

from obspy import read
import glob
import sys
from obspy.taup import TauPyModel

# Loads PREM model
model = TauPyModel(model="prem")

# Find list of stations directories
stations = glob.glob('../Data/*')

# Add phase names as additional arguments (these are the TauP phase names)
phase = []
for i in range(1, len(sys.argv)):
    phase.append(sys.argv[i])
count = 0
# Loop through stations
for stadir in stations:
        print("STATION:", stadir)
        stalist = glob.glob(stadir + '/*PICKLE')

        # Loop through events
        for s, sta in enumerate(stalist):
                    print(s)
                    seis = read(sta, format='PICKLE')

                    if not hasattr(seis[0].stats, 'traveltimes'):
                            seis[0].stats.traveltimes = dict()
                            # Loop through phases and call TauP_time to get
                            # traveltime
                    for ph in range(len(phase)):

                        if not phase[ph] in seis[0].stats.traveltimes:
                                # Extract only first time value and if value
                                # does not exists ttime=None
                                try:
                                        evdep_km = seis[0].stats['evdp']
                                        dist_deg = seis[0].stats['dist']
                                        arrivals = model.get_travel_times(
                                            source_depth_in_km=evdep_km,
                                            distance_in_degree=dist_deg,
                                            phase_list=[phase[ph]])

                                        ttime = arrivals[0].time
                                        print(phase[ph], ttime)
                                except:
                                        ttime = None
                                        print(phase[ph], ttime)
                                seis[0].stats.traveltimes[phase[ph]] = ttime
                        else:
                                print(
                                    'already calculated ttime for',
                                    phase[ph],
                                    '\t',
                                    sta)

                    seis.write(sta, 'PICKLE')
                    count += 1
