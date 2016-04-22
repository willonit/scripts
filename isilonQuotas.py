#!/usr/bin/env python

# Create Quotas on Isilon OneFS
# Quotas will be created on directories 1 level deep in <rootDir> of the size specified by <quotaSize>
# This script has been designed to run as a scheduled job

import json,commands,os

# Rootdir should be specified as An absolute path within the /ifs file system
rootDir = "/ifs/"

# Size should be specified as a  scaled value formatted as <integer>[kMGTP]
quotaSize = "20G"

# Get list of quotas and add to reverse sorted array
quotas = json.loads(commands.getoutput('isi quota quotas list --no-header --no-footer --format json'))
quotaDirs = [ ]
for quota in quotas:
  quotaDirs.append( quota['path'])
quotaDirs.sort(reverse=True)

# Get subdirectories of rootDir in sorted array
if rootDir[len(rootDir)-1] != '/':
  rootDir+='/'
osDirs = os.listdir(rootDir)
childDirs = [ ]
for child in osDirs:
  childDirs.append(rootDir+child)
childDirs.sort()

# Set quota if one does not already exists
createdQuotas = 0
quota = quotaDirs.pop()
for dir in childDirs:
  if dir ==  quota:
    if quotaDirs: quota = quotaDirs.pop()
  else:
    cmd = "isi quota quotas create %s directory --hard-threshold %s" % (dir, quotaSize)
    out = commands.getstatusoutput(cmd)
    if out[0] != 0:
      print "ERROR creating quota for %s : %s" % (dir,out[1])
    else:
      createdQuotas+=1


print "Created %s quotas" % (createdQuotas)
