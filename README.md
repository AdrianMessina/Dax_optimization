# 🚀 DAX Optimization Suite

**Comprehensive toolset for analyzing and optimizing DAX queries in Power BI**

> Developed by **Adrián Javier Messina** | YPF S.A. | January 2026

[![Version](https://img.shields.io/badge/version-1.1-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-19-blue.svg)](https://react.dev)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📚 Table of Contents

- [Overview](#overview)
- [Applications](#applications)
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains a suite of tools designed to help Power BI developers optimize their DAX code by detecting anti-patterns, measuring complexity, and providing actionable suggestions for improvement.

### Applications Included

This repository contains three applications with different approaches:

1. **dax-optimizer** - React/TypeScript web application with Monaco Editor
2. **dax-optimizer-streamlit** - Basic Python/Streamlit web app for quick analysis
3. **dax-optimizer-streamlit-v1.1** - Advanced version with PBIP file support and measure ranking

## 🚀 Quick Start

### Option 1: Streamlit Advanced (Recommended)

```bash
cd dax-optimizer-streamlit-v1.1
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

### Option 2: React Web App

```bash
cd dax-optimizer
npm install
npm run dev
```

### Option 3: Streamlit Basic

```bash
cd dax-optimizer-streamlit
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

## ⭐ Features

### Core Capabilities

- ✅ **DAX Pattern Detection**: Identifies anti-patterns and performance issues
- ✅ **Complexity Scoring**: Measures code complexity (0-100 scale)
- ✅ **PBIP File Support**: Analyzes complete Power BI Project files
- ✅ **Measure Ranking**: Prioritizes measures by impact and optimization potential
- ✅ **Smart Suggestions**: Provides specific optimization recommendations
- ✅ **Multiple Interfaces**: Choose between React, Streamlit basic, or Streamlit advanced

### Detection Capabilities

#### 🔴 Critical Issues
- Nested iterators (SUMX inside SUMX)
- FILTER(ALL(Table), ...) on full tables
- Measures used in calculated columns
- Unnecessary context transitions

#### ⚠️ Warnings
- FILTER without KEEPFILTERS in CALCULATE
- Nested CALCULATE functions
- Repeated expressions without variables
- Expensive functions (CROSSJOIN, GENERATE, LOOKUPVALUE)

#### ℹ️ Info
- Complex code without variables
- Repeated measure references
- Refactoring opportunities

## 📦 Installation

### Prerequisites

- **For Python apps**: Python 3.8+ and pip
- **For React app**: Node.js 18+ and npm

### Corporate Proxy Configuration

If you're behind a corporate proxy:

```bash
export HTTPS_PROXY=http://proxy-azure
export HTTP_PROXY=http://proxy-azure

# Install Python packages
pip install -r requirements.txt

# Or install Node packages
npm install
```

## 📖 Documentation

Each application has its own detailed documentation:

- **[dax-optimizer-streamlit-v1.1/README.md](dax-optimizer-streamlit-v1.1/README.md)** - Advanced Streamlit version (recommended)
- **[dax-optimizer/README.md](dax-optimizer/README.md)** - React web application
- **[dax-optimizer-streamlit/README.md](dax-optimizer-streamlit/README.md)** - Basic Streamlit version

Additional documentation:

- **[CHANGELOG.md](dax-optimizer-streamlit-v1.1/CHANGELOG.md)** - Version history
- **[ROADMAP.md](dax-optimizer-streamlit-v1.1/ROADMAP.md)** - Future development plans

## 🏗️ Architecture

```
dax-optimization/
├── dax-optimizer/                      # React + TypeScript app
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   ├── package.json
│   └── README.md
│
├── dax-optimizer-streamlit/            # Basic Streamlit app
│   ├── core/
│   │   ├── dax_parser.py
│   │   ├── dax_analyzer.py
│   │   └── dax_suggestions.py
│   ├── streamlit_app/
│   │   └── app.py
│   ├── requirements.txt
│   └── README.md
│
└── dax-optimizer-streamlit-v1.1/       # Advanced Streamlit app
    ├── core/
    │   ├── dax_parser.py
    │   ├── dax_analyzer.py
    │   ├── dax_suggestions.py
    │   ├── pbip_extractor.py          # NEW: PBIP support
    │   └── measure_ranker.py           # NEW: Ranking system
    ├── streamlit_app/
    │   └── app.py
    ├── requirements.txt
    └── README.md
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Built with [React](https://react.dev/) and [Vite](https://vitejs.dev/)
- DAX best practices from [SQLBI](https://www.sqlbi.com/)
- Power BI documentation from [Microsoft](https://learn.microsoft.com/power-bi/)

## 📧 Contact

**Adrián Javier Messina**
Desarrollador de visualización Sr. - YPF S.A.
Email: adrianjavier.messina@set.ypf.com

---

**Made with ❤️ for the Power BI community**
