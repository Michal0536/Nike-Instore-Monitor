# Product Stock Monitor

## Overview
This project monitors the stock levels of products in real-time, providing alerts when stock changes occur. It supports simultaneous monitoring of multiple products using multithreading.

## Features
- Real-time updates on stock levels for various stores.
- Alerts for changes in stock.
- Multithreaded monitoring for efficiency.

## Requirements
- Python 3.10
- Required packages: `requests`, `colorama`, `csv`, `datetime`, `threading`

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://your-repository-url
   cd your-project-directory
   ```

2. **Install dependencies:**
   ```bash
   pip install requests colorama
   ```

## Usage

1. **Prepare your data files:**
   - Populate `skus.csv` and `stores.csv` with the product codes (SKUs) and store information you want to monitor.

2. **Run the script:**
   ```bash
   python monitor_script.py
   ```
   - The script will monitor each SKU in separate threads, logging updates to the console.

This setup allows you to track product availability efficiently, helping you stay informed about important stock changes.