import pandas as pd
import numpy as np

dt = np.arange(9).reshape((3, 3))
print(dt)

data = pd.DataFrame(np.arange(9).reshape((3, 3)),
                    index=pd.Index(["dog", "pig", "cat"], name="state"),
                    columns=pd.Index(["1", "2", "3"], name="number"))

print(data)
print("=========")
print(data.stack())
tmp = data.unstack(0)
print(tmp)
