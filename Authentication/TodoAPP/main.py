#================================================#
#     Design  Auth Server with FastAPI       #
#              FastAPI Practices                 #
#================================================#

#Router: modulariZa funciones

# libraries ---------------


from fastapi import FastAPI
from database import engine
import models
from routers import auth,todos


## API Design ---------------
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

## desde acá se incluyen los routers

app.include_router(auth.router)
app.include_router(todos.router)
