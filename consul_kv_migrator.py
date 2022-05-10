from consul_kv import Connection
import json
import ast
from prettytable import PrettyTable
import getopt
import sys

argv = sys.argv[1:]

def _emptyCheckerFunc(argv):
  if not argv:
    print("use -h tag to get more information about the utility")
    exit()

_emptyCheckerFunc(argv)

try:
  opts, args = getopt.getopt(argv, "s:d:o:h")

except getopt.GetoptError:
  print("USAGE:")
  print("-h:  To get more information about the script options")
  print("FORMAT: python script.py -h")
  print("")
  exit()


for opt, arg in opts:

  if opt in ['-s']:
    _sourceConsulLink = arg
  if opt in ['-d']:
    _destinationConsulLink = arg
  if opt in ['-o']:
    _outputType = arg
  elif opt in ['-h']:
    print("Usage: python <NAME-OF-SCRIPT>.py ... [ -<OPTIONS> <VALUES>]")
    print("")
    print("Mendatory Option and arguments")
    print("")
    print("-s : Provide source consul URL")
    print("     FORMAT: -s <VALUE>")
    print("")
    print("-d : Provide destination consul URL")
    print("     FORMAT: -d <VALUE>")
    print("")
    print("-o : Provide database hostname")
    print("")
    print("     FORMAT: -o <VALUE>")
    print("     SUPPORTED TAGS:")
    print("         - json")
    print("         - table")
    print("")
    print("")
    print("AUTHOR: https://github.com/b44rawat")
    print("")
    sys.exit()

try:
    _sourceConsulObjectVar = Connection(endpoint=_sourceConsulLink)
    _destinationConsulObjectVar = Connection(endpoint=_destinationConsulLink)
except:
    print('Check with -h tag to get more detail about utils options')
    sys.exit()

_consulKvPathVar = _sourceConsulObjectVar.get('.', recurse=True)

def _consulMigrateKv():
    _consulKvOutputStoreJsonVar=[]
    for _KeyconsulKvPathVar in _consulKvPathVar:
        try:
            _destinationConsulObjectVar.put(_KeyconsulKvPathVar, _consulKvPathVar[_KeyconsulKvPathVar])
        except:
            _consulPutObjectStatusVar = "fail"
        else:
            _consulPutObjectStatusVar = "pass"        
        FIRSTVALUE="{ 'key': '" + _KeyconsulKvPathVar + "', 'value': '" + _consulKvPathVar[_KeyconsulKvPathVar] + "', 'status': '" + _consulPutObjectStatusVar + "'}"
        _consulKvOutputStoreJsonVar.append(FIRSTVALUE)
    return _consulKvOutputStoreJsonVar

_consulMigrateOutputKvVar = _consulMigrateKv()

_consulKvOutputStoreTableVar = PrettyTable(["Key", "Value", "Status"])

def formattedFunction(__consulKvOutputStoreJsonVar):
    _realdict = ast.literal_eval(__consulKvOutputStoreJsonVar)
    _consulKvOutputStoreTableVar.add_row([_realdict['key'], _realdict['value'], _realdict['status']])

for _tableConsulMigrateOutputKvVar in _consulMigrateOutputKvVar:
    formattedFunction(_tableConsulMigrateOutputKvVar)

if _outputType == "json":
    print(_consulMigrateOutputKvVar)
elif _outputType == "table":     
    print(_consulKvOutputStoreTableVar)
else:
    print("Check with -h tag to get more detail about utils options")
