import json
import argparse
from typing import Any, Callable, Protocol
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

type Providers = DataLoader | Transformer | Exporter
    
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
                if (row['age'] in ["", 'null']):
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

class RemovePatrick(Transformer):
    def transform(self, data: Data) -> Data:
        return [row for row in data if row["name"] != "Patrick"]

class JSONExporter(Exporter):
    def __init__(self, filename: str) -> None:
        self.filename = filename
    
    def _export_to_json(self, data: Data) -> None:
        with open(self.filename, "w") as filename:
            json.dump(data, filename, indent=2)
            
    def export(self, data: Data) -> None:
        self._export_to_json(data)

class Container:
    def __init__(self) -> None:
        self._providers: dict[str, tuple[Callable[[], Providers], bool]] = {}
        self._singletons: dict[str, Any] = {}
    
    def register(self, name: str, provider: Callable[[], Providers], singleton: bool = False) -> None:
        self._providers[name] = (provider, singleton)
        
    def resolve(self, name: str) -> Any:
        if name in self._singletons:
            return self._singletons[name]
        
        if name not in self._providers:
            raise ValueError(f"No provider registered for {name}.")
        
        provider, singleton = self._providers[name]
        instance = provider()
        
        if singleton:
            self._singletons[name] = True
        
        return instance
        
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
    
    # Set up the DI container
    container = Container()
    container.register(
        "loader", 
        InMemoryDataLoader if  args.loader == 'memory' else lambda: CSVDataLoader("input.csv"), 
        singleton=True
    )
    container.register("transformer", RemovePatrick)
    container.register("exporter", lambda: JSONExporter("output.json"), singleton=True)
    container.register("pipeline", lambda: DataPipeline(
        loader=container.resolve("loader"),
        transformer=container.resolve("transformer"),
        exporter=container.resolve("exporter")
    ))
    
    # Resolve and run the pipeline
    pipeline = container.resolve('pipeline')
    pipeline.run()
    print("Pipeline completed. Output written to output.json")

if __name__ == "__main__":
    main()