import urx
import numpy as np
from elementary_transformations import rx,ry,rz,tx,ty,tz
import time

rob = urx.Robot("160.69.69.23")

pos = rob.getl()
print(pos)



print("Closing")
# закрыть захват
rob.send_program('set_tool_digital_out(0, True)')
rob.send_program('set_tool_digital_out(1, False)')
time.sleep(2)

print("Opening")
# открыть захват
rob.send_program('set_tool_digital_out(0, False)')
rob.send_program('set_tool_digital_out(1, True)')
time.sleep(2)


print("Finished")
rob.stop()
rob.close()
exit(0)