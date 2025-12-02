import json
import argparse
from typing import Any, Protocol
import csv

type Data = list[dict[str, Any]]

# Define abstract classes
class DataLoader(Protocol):
    def load(self) -> Data:
        ...

class Transformer(Protocol):
    def transformer(self, data: Data) -> Data:
        ...
        
class Exporter(Protocol):
    def export(self, data: Data) -> None:
        ...
    
# Implementations of components
class CSVDataLoader(DataLoader):
    def __init__(self, filename: str):
        self.filename = filename
        self.data = []
    
    def load(self) -> Data:
        with open(self.filename, mode='r', newline='', encoding='utf-8') as csv_file:
            # create a csv reader object
            reader = csv.DictReader(csv_file)
            
            # Iterate over each row in the csv file
            for row in reader:
                if (row['age'] == "" or row['age'] == 'null'):
                    row['age'] = None
                    
                self.data.append(row)
            
            return self.data
            
    
class InMemoryDataLoader(DataLoader):
    def load(self) -> Data:
        return [
            {"name": "Big BOI", "age": 37},
            {"name": "Paul Wall", "age": None},
            {"name": "Clyde", "age": 13},
        ]

class CleanMissingFields(Transformer):
    def transform(self, data: Data) -> Data:
        return [row for row in data if row["age"] is not None]

class JSONExporter(Exporter):
    def __init__(self, filename: str) -> None:
        self.filename = filename
    
    def _export_to_json(self, data: Data) -> None:
        with open(self.filename, "w") as filename:
            json.dump(data, filename, indent=2)
            
    def export(self, data: Data) -> None:
        self._export_to_json(data)

# Data Pipeline using Dependency Injection
class DataPipeline:
    def __init__(self,loader: DataLoader, transformer: Transformer, exporter: Exporter) -> None:
        self.loader = loader
        self.transformer = transformer
        self.exporter = exporter
    
    def run(self) -> None:
        data = self.loader.load()
        cleaned = self.transformer.transform(data)
        self.exporter.export(cleaned)

def main() -> None:
    parser = argparse.ArgumentParser(description="DataPipelin program")
    parser.add_argument('-l', '--loader', choices=['csv', 'memory'], default='memory', help="Data loader")
    args = parser.parse_args()
    match (args.loader):
        case 'csv':
            loader = CSVDataLoader("input.csv")
        case 'memory':
            loader = InMemoryDataLoader()
            
    transformer = CleanMissingFields()
    exporter = JSONExporter("output.json")
    pipeline = DataPipeline(loader, transformer, exporter)
    pipeline.run()
    print("Pipeline completed. Output written to output.json")

if __name__ == "__main__":
    main()