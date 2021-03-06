import os, sys
import platform
from datetime import datetime
is_verbose = True

# Takes a timestamp and puts out a string with the approxomation of the age
def age(from_date, since_date = None, target_tz=None, include_seconds=False):
  if from_date is None:
    return "Unknown"

  from_date = datetime.fromtimestamp(from_date)
  if since_date is None:
    since_date = datetime.now(target_tz)

  distance_in_time = since_date - from_date
  distance_in_seconds = int(round(abs(distance_in_time.days * 86400 + distance_in_time.seconds)))
  distance_in_minutes = int(round(distance_in_seconds/60))


  if distance_in_minutes <= 1:
    if include_seconds:
      for remainder in [5, 10, 20]:
        if distance_in_seconds < remainder:
          return "less than %s seconds ago" % remainder
        if distance_in_seconds < 40:
          return "half a minute"
        elif distance_in_seconds < 60:
          return "less than a minute ago"
        else:
          return "1 minute ago"
      else:
        if distance_in_minutes == 0:
          return "less than a minute ago"
        else:
          return "1 minute ago"
  elif distance_in_minutes < 45:
    return "%s minutes ago" % distance_in_minutes
  elif distance_in_minutes < 90:
    return "about 1 hour ago"
  elif distance_in_minutes < 1440:
    return "about %d hours ago" % (round(distance_in_minutes / 60.0))
  elif distance_in_minutes < 2880:
    return "1 day ago"
  elif distance_in_minutes < 43220:
    return "%d days ago" % (round(distance_in_minutes / 1440))
  elif distance_in_minutes < 86400:
    return "about 1 month ago"
  elif distance_in_minutes < 525600:
    return "%d months ago" % (round(distance_in_minutes / 43200))
  elif distance_in_minutes < 1051200:
    return "about 1 year ago"
  else:
    return "over %d years ago" % (round(distance_in_minutes / 525600))

def set_verbosity(b):
    global is_verbose
    is_verbose = b

def print_error(*args):
    if not is_verbose: return
    args = [str(item) for item in args]
    sys.stderr.write(" ".join(args) + "\n")
    sys.stderr.flush()

def print_msg(*args):
    # Stringify args
    args = [str(item) for item in args]
    sys.stdout.write(" ".join(args) + "\n")
    sys.stdout.flush()


def user_dir():
    if "HOME" in os.environ:
        return os.path.join(os.environ["HOME"], ".electrum")
    elif "LOCALAPPDATA" in os.environ:
        return os.path.join(os.environ["LOCALAPPDATA"], "Electrum")
    elif "APPDATA" in os.environ:
        return os.path.join(os.environ["APPDATA"], "Electrum")
    else:
        #raise BaseException("No home directory found in environment variables.")
        return 

def appdata_dir():
    """Find the path to the application data directory; add an electrum folder and return path."""
    if platform.system() == "Windows":
        return os.path.join(os.environ["APPDATA"], "Electrum")
    elif platform.system() == "Linux":
        return os.path.join(sys.prefix, "share", "electrum")
    elif (platform.system() == "Darwin" or
          platform.system() == "DragonFly"):
        return "/Library/Application Support/Electrum"
    else:
        raise Exception("Unknown system")


def get_resource_path(*args):
    return os.path.join(".", *args)


def local_data_dir():
    """Return path to the data folder."""
    assert sys.argv
    prefix_path = os.path.dirname(sys.argv[0])
    local_data = os.path.join(prefix_path, "data")
    return local_data


def format_satoshis(x, is_diff=False, num_zeros = 0):
    from decimal import Decimal
    s = Decimal(x)
    sign, digits, exp = s.as_tuple()
    digits = map(str, digits)
    while len(digits) < 9:
        digits.insert(0,'0')
    digits.insert(-8,'.')
    s = ''.join(digits).rstrip('0')
    if sign: 
        s = '-' + s
    elif is_diff:
        s = "+" + s

    p = s.find('.')
    s += "0"*( 1 + num_zeros - ( len(s) - p ))
    s += " "*( 9 - ( len(s) - p ))
    s = " "*( 5 - ( p )) + s
    return s
