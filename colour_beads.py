import sys

cmm_fname=str(sys.argv[1])
id_file=str(sys.argv[2])
rgb=str(sys.argv[3])
blend=str(sys.argv[4])

blend = blend.upper()
rgb_given = rgb.split(",")

'''
def convert_cmm_to_dict(cmm_file):
  cmm_dict = {}
  for line in cmm_file:
    if line.startswith("<marker "):
      marker_dict = {}
      line=line.rstrip()
      line=line.split()
      key=line[-1].replace("beadID=","").replace("\"","").replace("/","").replace(">","")
      
      marker_id = line[1].replace("id=","").replace("\"","")
      marker_dict["marker_id"] = marker_id

      x = line[2].replace("x=","").replace("\"","")
      marker_dict["x"] = x

      y = line[3].replace("y=","").replace("\"","")
      marker_dict["y"] = y

      z = line[4].replace("z=","").replace("\"","")
      marker_dict["z"] = z

      radius = line[5].replace("radius=","").replace("\"","")
      marker_dict["radius"] = radius

      r = line[6].replace("r=","").replace("\"","")
      marker_dict["r"] = r

      g = line[7].replace("g=","").replace("\"","")
      marker_dict["g"] = g

      b = line[8].replace("b=","").replace("\"","")
      marker_dict["b"] = b

      chr_id = line[9].replace("chrID=","").replace("\"","")
      marker_dict["chr_id"] = chr_id

      bead_id = line[10].replace("beadID=","").replace("\"","")
      marker_dict["bead_id"] = bead_id

      cmm_dict[key] = marker_dict
  return cmm_dict
'''

def rgb_float(val):
  return float(val)/255.0

with open(cmm_fname) as cf:
  cmm_file=cf.readlines()

with open(id_file) as idf:
  id_list=idf.readlines()

id_list = [id.rstrip() for id in id_list]

#cmm_dict = convert_cmm_to_dict(cmm_file)

cmm_dict = {}
for line in cmm_file:
  if line.startswith("<marker "):
    line=line.rstrip()
    line=line.split()
    key=line[-1].replace("beadID=","").replace("\"","").replace("/","").replace(">","")
    cmm_dict[key] = line

if blend == "OVERRIDE": 
  for k in cmm_dict.iterkeys():
    if k in id_list:
      cmm_dict[k][6] = "r=\"" + str(rgb_float(rgb_given[0])) + "\""
      cmm_dict[k][7] = "g=\"" + str(rgb_float(rgb_given[1])) + "\""
      cmm_dict[k][8] = "b=\"" + str(rgb_float(rgb_given[2])) + "\""
    else:
      cmm_dict[k][6] = "r=\"" + str(rgb_float(105)) + "\""
      cmm_dict[k][7] = "g=\"" + str(rgb_float(105)) + "\""
      cmm_dict[k][8] = "b=\"" + str(rgb_float(105)) + "\""
elif blend == "BLEND":
  for k in cmm_dict.iterkeys():
    if k in id_list:
      ex_r = cmm_dict[k][6].replace("r=","").replace("\"","")
      ex_g = cmm_dict[k][7].replace("g=","").replace("\"","")
      ex_b = cmm_dict[k][8].replace("b=","").replace("\"","")
     
      if ex_r == str(rgb_float(105)) and ex_g == str(rgb_float(105)) and ex_b == str(rgb_float(105)):
        cmm_dict[k][6] = "r=\"" + str(rgb_float(rgb_given[0])) + "\""
        cmm_dict[k][7] = "g=\"" + str(rgb_float(rgb_given[1])) + "\""
        cmm_dict[k][8] = "b=\"" + str(rgb_float(rgb_given[2])) + "\""
      else:
        r = (float(ex_r)+rgb_float(rgb_given[0]))/2
        g = (float(ex_g)+rgb_float(rgb_given[1]))/2
        b = (float(ex_b)+rgb_float(rgb_given[2]))/2
        cmm_dict[k][6] = "r=\"" + str(r) + "\""
        cmm_dict[k][7] = "g=\"" + str(g) + "\""
        cmm_dict[k][8] = "b=\"" + str(b) + "\""

for line in cmm_file:
  if line.startswith("<marker "):
    line=line.rstrip()
    line=line.split()
    key=line[-1].replace("beadID=","").replace("\"","").replace("/","").replace(">","")
    print ' '.join(cmm_dict[key])
  else:
    print line.rstrip()
