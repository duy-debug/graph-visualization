# Graph Manager: Comprehensive Visualization & Data Analysis Tool

**Developer:** Tran Mai Ngoc Duy - ID: 65130650  
**Class:** 65CNTT1  
**Supervisor:** Ph.D. Pham Thi Thu Thuy  
**Project:** Major Base Project - GRAPH REPRESENTATION SIMULATION USING ADJACENCY MATRIX AND ADJACENCY LIST

---

## PROJECT OVERVIEW

**Graph Manager** is a professional desktop application developed in Python, designed to help users model, manage, and visualize complex graph structures. The tool supports various graph types (directed, undirected, weighted, and unweighted) and provides real-time analytical tools for academic and practical graph theory applications.

---

## KEY FEATURES

### 1. Robust Data Management
- **Smart Data Import**: Interactive text editing with real-time graph updates (Auto-update).
- **Comprehensive File I/O**: Import/export graph structures using standard `.txt` formats with detailed analytical reports.
- **Auto-Attribute Detection**: Intelligently detects directed/undirected and weighted properties from input data.

### 2. Advanced Visualization & Interaction
- **Dynamic Graphics**: Powered by **NetworkX** and **Matplotlib** for professional-grade layout computation and rendering.
- **Interactive Canvas**: Support for dragging and dropping nodes to customize visual layouts.
- **Highlighting System**: Easily emphasize critical nodes and edges via double-click interactions or text-based queries.

### 3. Mathematical Analysis & Presentation
- **Adjacency Representation**: Real-time display of both Adjacency Matrix and Adjacency List views.
- **Graph Metrics**: Automated computation of graph density and classification (Sparse vs. Dense).
- **Template Library**: Includes built-in sample data like the famous *Zachary's Karate Club* for testing and demonstration.

---

## CORE TECHNOLOGIES

| Technology | Role |
|-----------|-----------|
| **Python 3.13+** | Core programming language |
| **Tkinter** | Standard GUI framework for desktop components |
| **NetworkX** | Graph theory logic, algorithms, and layout computation |
| **Matplotlib** | Canvas rendering and interactive graphic components |

---

## SYSTEM ARCHITECTURE

- **`graph_app/app.py`**: The main Controller & View; manages the GUI, event loop, and real-time synchronization.
- **`graph_app/graph_data.py`**: The Model layer; defines the core Graph data structure and fundamental graph operations.
- **`graph_app/graph_io.py`**: Utility module; handles file parsing, report generation, and sample data loading.
- **`graph_app/benchmark.py`**: Performance evaluation module; measures processing time of various graph operations.

---

## INSTALLATION & EXECUTION

1. **Install Dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Application**:
   ```bash
   python -m graph_app.app
   ```
3. **Run Performance Benchmark**:
   ```bash
   python -m graph_app.benchmark
   ```

---

## PERFORMANCE BENCHMARK

The `benchmark.py` module provides tools for measuring application performance with the following features:

### Measured Metrics:
- **Structure Creation Time**: Time to initialize graph from edge list.
- **Edge Check Time**: Time to query edge existence (1000 iterations).
- **Neighbor Retrieval Time**: Time to access adjacent vertices (1000 iterations).
- **Adjacency Matrix Generation Time**: Time to create adjacency matrix representation.
- **Adjacency List Generation Time**: Time to create adjacency list text representation.
- **Drawing Time**: Time to render graph using Matplotlib.

### Default Test Configurations:
- **Node counts**: 50, 200, 500
- **Densities**: 10%, 30%, 50%

Benchmark results will be exported to `benchmark_results.txt` in the `graph_app` directory.

---

## INPUT FILE FORMAT (.txt)

Input files should follow this structure:
- **Line 1**: Total number of nodes.
- **Line 2**: Directed flag (`1` for Directed, `0` for Undirected).
- **Following Lines**: Edge list in the format `source destination [weight]`.

Example:
```text
3
1
A B 5.0
B C 3.0
```

---

## LICENSE & ACKNOWLEDGMENTS

This project was developed as part of the **Major Base Project** program at **Nha Trang University**.

**Student:** Tran Mai Ngoc Duy  
**Student ID:** 65130650  
**Completion Date:** December 2025
