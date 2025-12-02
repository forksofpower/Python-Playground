# Python Dependency Injection Example

This project demonstrates the evolution of dependency injection in Python, starting from a hardcoded implementation, moving to manual dependency injection, and finally using a Dependency Injection (DI) container. It also includes a FastAPI example.

## Prerequisites

- Python 3.12+
- `uv` package manager (recommended)

## Examples

### 1. Hardcoded Implementation

This example shows a data pipeline where dependencies (loader, transformer, exporter) are hardcoded within the class.

**Characteristics:**
- **Tight Coupling:** The `DataPipeline` class knows exactly which classes to instantiate (`CSVDataLoader`, etc.).
- **Difficult Testing:** You cannot easily swap out the real CSV loader for a mock one during testing.

**Run:**
```bash
uv run hardcoded.py
```

### 2. Manual Dependency Injection

This example introduces protocols (interfaces) and injects dependencies manually via the constructor. This allows for swapping implementations (e.g., CSV vs. In-Memory loader).

**Characteristics:**
- **Decoupling:** `DataPipeline` depends on abstractions (`DataLoader`), not concrete classes.
- **Flexibility:** You can pass different implementations at runtime.
- **Manual Wiring:** You are responsible for creating instances and passing them together in `main()`.

**Run:**
```bash
uv run manual.py
```

**CLI Arguments:**
- `--loader`: Choose the data loader implementation. Options: `memory` (default), `csv`.

**Run with CSV loader:**
```bash
uv run manual.py --loader csv
```

### 3. DI Container

This example uses a custom Dependency Injection Container to manage the creation and lifecycle of dependencies.

**Characteristics:**
- **Centralized Wiring:** The container handles the registration and resolution of dependencies.
- **Lifecycle Management:** The container can manage singletons (shared instances) versus transient instances.
- **Scalability:** Easier to manage complex dependency graphs as the application grows.

**Run:**
```bash
uv run main.py
```

**CLI Arguments:**
- `--loader`: Choose the data loader implementation. Options: `memory` (default), `csv`.

**Run with CSV loader:**
```bash
uv run main.py --loader csv
```

### 4. FastAPI Example

This example demonstrates how to use dependency injection in a FastAPI application using `Depends`.

**Characteristics:**
- **Framework Integration:** FastAPI's `Depends` system acts as a built-in DI container.
- **Request Scope:** Dependencies can be scoped to the request lifecycle.

**Run:**
```bash
uv run fastapi_example.py
```

**Test the endpoint:**
```bash
curl -X POST "http://127.0.0.1:8000/process" \
     -H "Content-Type: application/json" \
     -d '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": null}]'
```
