
Kafka Implementation of standard raclette.  To use follow the same standard raclette procedures but use a modified config file, using kafkareader and kafka saver.

Example:

[main]

[io]
reader=kafkareader
# Options for the Atlas REST API
start = 2018-09-02T12:00
stop = 2018-09-02T13:00
# Fetch data by chunks of chunk_size seconds. Set a smaller value if you have
# memory problems
chunk_size = 1800
msm_ids =  1748022, 1748024, 11645084, 11645087, 2244316, 2244318, 2244316, 2244318, 2435592, 2435594, 1796567, 1796569, 2904335, 2904338, 1618360, 1618362, 7970886, 7970889, 7970886, 7970889, 6886972, 6886975, 12237261 
probe_ids = 

# Options for the output
saver=kafkasaver
results = results/ASC_start/results_%(start)s.sql
log = results/ASC_start/log_%(start)s.log

[timetrack]
converter = allin_cy

[tracksaggregator]
window_size = 1800
significance_level = 0.05
# ignore links visited by small number of tracks/traceroutes
min_tracks = 5 

[anomalydetector]
enable = 1 

[lib]
ip2asn_directory = raclette/lib/
ip2asn_db = data/rib.20180701.pickle
ip2asn_ixp = 
