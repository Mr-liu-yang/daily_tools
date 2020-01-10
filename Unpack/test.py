import os
import sys

with open("list", "w") as fff:
 for i,j,k in os.walk("/home/pangu/work_jiami/akana/tomcat/webapps/android/cache/File/c64995c1c4ab40cb27a5bb5a14924d6e1bdc16789cff500b3288c0d3c4601e65ee37849ec6a5198116dc427d9d005e3a/AndroidProject/assets/init"):
  for l in k:
   fff.write(os.path.abspath(os.path.join(i, l)) + "\n")
