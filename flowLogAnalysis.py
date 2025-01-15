from collections import defaultdict
from constants import (
    LOOKUP_TABLE_DIR,
    LOOKUP_TABLE_FILE,
    FLOW_LOG_INPUT_DIR,
    FLOW_LOG_INPUT_FILENAME,
    FLOW_LOG_OUTPUT_DIR,
    FLOW_LOG_OUTPUT_FILENAME,
    DSTPORT_COL_INDEX,
    PROTOCOL_COL_INDEX
)
import csv
import sys


from protocolData import getProtocolName


class FlowLogDataAnalyzer:
    def __init__(self) -> None:
        self.tagLookup = defaultdict(str)
        self.portProtocolCounts = defaultdict(int)
        self.tagCounts = defaultdict(int)

    '''
    - reads the lookup table file at the path passed as the argument
    - stores the port, protocol, tag data in a dictionary in the class
    - key is (port, protocol) tuple and value is the tag
    '''
    def loadLookupTableData(self, lookupTableFile) -> None:
        with open(lookupTableFile, mode = 'r') as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if len(line) != 3:
                    continue
                # unpack each row/line into port, protocol, tag
                port, protocol, tag = line
                if (port, protocol) not in self.tagLookup:
                    self.tagLookup[(port, protocol)] = tag


    '''
    - reads the flow log data file at the path passed as the argument
    - parses each row/line and extracts the dstport and protocol
    - stores the count for each (port, protocol) combination in a dictionary
    - key is (port, protocol) tuple and value is the count
    '''
    def readFlowLogData(self, flowLogFile) -> None:
        with open(flowLogFile, mode='r') as file:
            for line in file:
                line = line.strip()
                fields = line.split()
                if len(fields) <= PROTOCOL_COL_INDEX:
                    continue
                dstport = fields[DSTPORT_COL_INDEX]
                protocol = fields[PROTOCOL_COL_INDEX]

                protocolName = getProtocolName(int(protocol))
                self.portProtocolCounts[(dstport, protocolName)] += 1


    '''
    - for each (port, protocol) combination in the flow log data, identify the tag
    - if there is no tag data for a (port, protocol) pair, it defaults to "Untagged"
    - stores the count for each tag in a dictionary
    - key is the tag and value is the count
    '''
    def _getTagCounts(self) -> None:
        for key, val in self.portProtocolCounts.items():
            tag = "Untagged"
            if key in self.tagLookup:
                tag = self.tagLookup[key]
            
            self.tagCounts[tag] += val


    '''
    - write the (tag, count) data to the output file in csv format
    '''
    def logTagData(self, outputFile) -> None:
        self._getTagCounts()

        with open(outputFile, 'w', newline='') as csvfile:
            fieldnames = ['tag', 'count']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for key, val in self.tagCounts.items():
                writer.writerow([key, val])

            writer.writerow([])


    '''
    - append the (port, protocol, count) data to the output file in csv format
    '''
    def logPortProtocolData(self, outputFile) -> None:
        with open(outputFile, mode='a', newline='') as csvfile:
            fieldnames = ['port', 'protocol', 'count']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for key, val in self.portProtocolCounts.items():
                writer.writerow([key[0], key[1], val])


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 0 and len(args) != 3:
        print("Please run the program in one of the following two ways:\n")
        print("1. with either no extra command line arguments at all")
        print("% python3 flowLogAnalysis.py\n")
        print("2. with exactly 3 extra command line arguments.")
        print("% python3 flowLogAnalysis.py <flow log> <lookup table> <output file>\n")
        print("Refer to README.txt for more details\n")

    # initialize the input and output file paths to the default values
    flowLogFile = FLOW_LOG_INPUT_DIR + FLOW_LOG_INPUT_FILENAME
    lookupTableFile = LOOKUP_TABLE_DIR + LOOKUP_TABLE_FILE
    outputFile = FLOW_LOG_OUTPUT_DIR + FLOW_LOG_OUTPUT_FILENAME
    
    # if custom file paths are provided, use them instead of the default values
    if len(args) == 3:
        flowLogFile = args[0]
        lookupTableFile = args[1]
        outputFile = args[2]
    
    flowLogs = FlowLogDataAnalyzer()

    flowLogs.loadLookupTableData(lookupTableFile)
    flowLogs.readFlowLogData(flowLogFile)
    flowLogs.logTagData(outputFile)
    flowLogs.logPortProtocolData(outputFile)
