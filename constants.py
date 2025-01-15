'''
default values for input and output directories and files
these are used only if command line arguments are not passed
'''

'''
- default lookup table directory is the current directory
- default lookup table filename is "lookup_table.csv"
'''
LOOKUP_TABLE_DIR = ""
LOOKUP_TABLE_FILE = "lookup_table.csv"

'''
- default flow log input data directory is the current directory
- default flow log input data filename is "input.log"
'''
FLOW_LOG_INPUT_DIR = ""
FLOW_LOG_INPUT_FILENAME = "input.log"

'''
- default flow log output data directory is the current directory
- default flow log output data filename is "input.log"
'''
FLOW_LOG_OUTPUT_DIR = ""
FLOW_LOG_OUTPUT_FILENAME = "output.log"

'''
- column indices to be looked at in each row/line of the flow log data
  in order to read the dstport and protocol
- taken from https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields
'''
DSTPORT_COL_INDEX = 6
PROTOCOL_COL_INDEX = 7