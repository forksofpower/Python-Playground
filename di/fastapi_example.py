from fastapi import Body, FastAPI, Depends
from typing import Protocol, Any, List, Dict
import uvicorn

type Data = List[Dict[str, Any]]

app = FastAPI()

# Transformor interface and implementation
class Transformer(Protocol):
    def transform(self, data: Data) -> Data:
        ...
class CleanMissingFields(Transformer):
    def transform(self, data: Data) -> Data:
        return [row for row in data if row.get("age") is not None]
    
# Dependency
def get_transformer() -> Transformer:
    return CleanMissingFields()

# Endpoint
@app.post("/process")
def process_data(
    data: Data = Body(...),
    transformer: Transformer = Depends(get_transformer)
) -> dict[str, Any]:
    processed = transformer.transform(data)
    return {"processed_data": processed}

def main() -> None:
    uvicorn.run("fastapi_example:app", host="0.0.0.0", port=8000, reload=True)
    
if __name__ == "__main__":
    main()