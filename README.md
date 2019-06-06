# kafka-migration
Post Kafka Installation Instructions.

Part One: Procucing Ripe ATLAS Data to kafka

Download test_cousteau.py
Can be ran in one of two ways

Just "python test_Cousteau.py"

Continuously downloads new data every ten minutes.  This continues infinitely.

alternatively you can use "python test_cousteau.py 2018-09-02-12:00 2018-09-02-17:00"
e.g. test_cousteau.py with start time and end time.

Downloads all of the traceroutes in the given time frame.

Part Two: Using Raclette With kafka

For the most part just run raclette as you would normally, but change asc-start.conf so that:

reader = kafkareader
and
saver = kafkasaver

the start and stop times should line up with the input for test_cousteau.py
so if you use 2018-09-02-12:00 2018-09-02-17:00

within the config file start and stop should be:
start = 2018-09-02T12:00
stop = 2018-09-02T17:30  #(should be fine if you use exactly 17:00, but Ive been using a buffer to make sure it times out properly)


As it is now, this should create the sql database as it always has, by consuming the data produced by test_cousteau, while also storing the sql data within kafka for later use, where it can be made into the tables again, if necessary.

POSSIBLE PROBLEMS.

The most likely one, if youre getting no output, is that kafkareader isnt properly reading what test_cousteau is producing.  If thats the case, check within test_cousteau.py, and look for producer.send("______").  whatever is in producer.send, should correspond to self.consumer.subscribe("______") within kafkareader.  (if youre having trouble, its probably best to create an entirely new topic to put into both.  using existing topics can get messy if there is pre existing data there and youre just trying to get it to work)

