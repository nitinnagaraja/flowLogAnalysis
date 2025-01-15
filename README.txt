The main program is in flowLogAnalysis.py

To execute the program with default input and output file paths and names, run the following.
% python3 flowLogAnalysis.py
  File paths and names used in this case are declared in constants.py

To execute the program with input and output file paths and names passed as arguments, run the following.
% python3 flowLogAnalysis.py input.log lookup_table.csv output.log
  The program accepts the three command line arguments in exactly that order shown above.
  Here,
  input.log is the first argument. It is the input file with the flow log data
  lookup_table.csv is the second argument. It is the input file with the lookup table data
  output.log is the third and last argument. It is the output file where the output will be written
    - NOTE: if output.log already exists, it will be overwritten (!!!)
  

--------------------------------
ASSUMPTIONS AND BEHAVIORS
--------------------------------

1.  The flow log input data file does not have headers. All the non-empty rows are flow log records.

2.  Each row/line in the flow log data ideally has the following 14 fields/columns.
    ["version", "account-id", "interface-id", "srcaddr", "dstaddr", "srcport", "dstport", "protocol", "packets", "bytes", "start", "end", "action", "log-status"]
    This is derived from the flow log data format here - https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields

3. "dstport" and "protocol" are the 7th and 8th columns in each row. If a row has less than 8 columns, ignore that row and we carry on.

4. The mapping from protocol numbers to protocol names is done in protocolData.py based on uses https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml 
   If the protocol number in the flow log record
        - is not in the [0, 255] range for whatever reason, the protocol will be listed as "invalid"
        - is associated with a protocol that does not have an assigned keyword/name, the protocol will be listed as "unassigned"

5. If a row in the lookup table does not have exactly 3 columns (dstport, protocol, tag - in that order), ignore that row and carry on.

6. If a tag is not found in the lookup table file for a (dstport, protocol) combination, the tag will be listed as "Untagged"

7. Tag count data is first written to the output file in CSV format.

8. (dstport, protocol) count data is appended to the same output file as above in CSV format.

9. There are separate methods to handle the different responsibilities, so that they can be independently called if/when needed.