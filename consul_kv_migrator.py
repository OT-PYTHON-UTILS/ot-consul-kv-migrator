import ast
import getopt
import sys
import socket
from consul_kv import Connection
from prettytable import PrettyTable
import urllib.request,urllib.parse,urllib.error

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
    print("Usage: python <NAME-OF-SCRIPT>.py ... [ -<OPTIONS> <VALUES>]\n")
    print("Mendatory Option and arguments\n")
    print("-s : Provide source consul URL")
    print("     FORMAT: -s <VALUE>\n")
    print("-d : Provide destination consul URL")
    print("     FORMAT: -d <VALUE>\n")
    print("-o : Provide database hostname")
    print("     FORMAT: -o <VALUE>")
    print("     SUPPORTED TAGS:")
    print("         - json")
    print("         - table\n")
    print("AUTHOR: https://github.com/b44rawat")
    sys.exit()

try:
  _sourceConsulObjectVar = Connection(endpoint=_sourceConsulLink)
except NameError:
    print('Check with -h tag to get more detail about -s option')
    sys.exit()
except urllib.error.URLError:
    print('Check with -h tag to get more detail about -s option')
    sys.exit()
except socket.gaierror:
    print('Check with -h tag to get more detail about -s option')
    sys.exit()


try:
  _destinationConsulObjectVar = Connection(endpoint=_destinationConsulLink)
except NameError:
    print('Check with -h tag to get more detail about -d option')
    sys.exit()
except urllib.error.URLError:
    print('Check with -h tag to get more detail about -d option')
    sys.exit()
except socket.gaierror:
    print('Check with -h tag to get more detail about -d option')
    sys.exit()

try:
  _consulKvPathVar = _sourceConsulObjectVar.get('.', recurse=True)
except ValueError as e:
  print("Check with -h tag to get more detail about -s option")
  sys.exit()
except urllib.error.URLError as e:
  print("Check with -h tag to get more detail about -s option")
  sys.exit()
except urllib.error.HTTPError as e:
  print("Check with -h tag to get more detail about -s option")
  sys.exit()
except NameError as e:
  print("Check with -h tag to get more detail about -s option")
  sys.exit()

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

if __name__ == "__main__":
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
