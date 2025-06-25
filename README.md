# 🏔️ Duluth Tourism Recovery Analysis

**End-to-End Data Pipeline for Tourism Industry Analysis**

> Automated extraction and analysis of tourism data from Minnesota Department of Revenue PDFs to understand COVID-19's economic impact on Duluth's tourism sector.

## 🎯 Project Overview

This project demonstrates a complete data engineering pipeline that transforms unstructured government PDFs into actionable business intelligence. By analyzing 4 years of Minnesota sales tax data, we reveal insights into Duluth's tourism recovery post-COVID-19.

### Key Achievements
- 📊 **$660M+ Tourism Economy Analyzed** across St. Louis County
- 🏢 **967 Tourism Establishments** tracked across 4 industry sectors
- 📈 **100% Automated Extraction** from 376 pages of complex PDF reports

## 📊 Data Sources

- **Minnesota Department of Revenue Annual Sales Tax Reports (2019-2022)**
- **Industry Sectors**: Accommodation, Food Services, Recreation, Museums
- **Geographic Scope**: St. Louis County (Duluth metropolitan area)

## 🛠️ Technical Architecture

### Data Extraction Pipeline

cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

venv/
env/
ENV/

.ipynb_checkpoints

.DS_Store

node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

build/
dist/
