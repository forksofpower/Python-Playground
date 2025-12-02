# 
# Python Dependency Injection Example
#
import json
from typing import Any

type Data = list[dict[str, Any]]

class DataPipeline:
    def run(self) -> None:
        # Hardcoded loader
        data = self._load_data_from_csv()
        
        # Hardcoded transformation
        cleaned = [row for row in data if row["age"] is not None]
        
        # Hardcoded Export
        self._export_to_json(cleaned)
        
    def _load_data_from_csv(self) -> Data:
        # Simulate reading from CSV
        return [
            {"name": "Patrick", "age": 37},
            {"name": "Eric", "age": None},
            {"name": "Clyde", "age": 13},
        ]
        
    def _export_to_json(self, data: Data) -> None:
        with open("output.json", "w") as file:
            json.dump(data, file, indent=2)
            
    
def main() -> None:
    pipeline = DataPipeline()
    pipeline.run()
    print("Pipeline completed. Output written to output.json")

if __name__ == "__main__":
    main()