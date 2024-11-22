
# import tomllib
import os
import re

TOML_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pyproject.toml")
INIT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),"instrumentlab","__init__.py")

new_version = None

def update_toml_file():
    ''' Open the toml file, find the version number, and increment it.
    '''
    global new_version
    
    with open(TOML_FILE, 'r') as rf:                # read entire toml file
        data = rf.readlines()
    
    with open(TOML_FILE, 'w') as wf:                # start rewriting it
        for line in data:                           # go over all the lines
            
            m = re.match('version = \"(\d*).(\d*).(\d*)\"', line)   # does it contain the version number ?
            if m:
                v1,v2,v3 = m.group(1),m.group(2),m.group(3)         # get all parts
                
                new_version = f"{v1}.{v2}.{int(v3)+1}"              # build new version number
    
                print( f"Update version from {v1}.{v2}.{v3} to {new_version}")
                
                wf.write(f'version = "{new_version}"\n')                 # write new version number

            else:
                wf.write(line)                      # just copy all other lines


def update_init_file():
    ''' Open the __init__ file of the package, and fill in the version number.
    '''
    with open(INIT_FILE, 'r') as rf:                # read entire init file
        data = rf.readlines()
    
    with open(INIT_FILE, 'w') as wf:                # start rewriting it
        for line in data:                           # go over all the lines
            
            if line.startswith("__version__"):      # write new version
                wf.write(f'__version__ = "{new_version}"\n')
            else:
                wf.write(line)                      # just copy all other lines


if __name__=="__main__":
    update_toml_file()
    assert new_version is not None, "Version number not found in toml file"
    update_init_file()
    
    
    
    