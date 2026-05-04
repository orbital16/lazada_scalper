#!/usr/bin/env python3
"""
Lazada Stock Monitor - UI Edition
Multi-product monitoring with stock screener interface
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import json
from pathlib import Path
from stock_monitor import LazadaStockMonitor

# Page config
st.set_page_config(
    page_title="Lazada Stock Monitor",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = []

if 'logs' not in st.session_state:
    st.session_state.logs = []

if 'monitor' not in st.session_state:
    st.session_state.monitor = LazadaStockMonitor()
    st.session_state.monitor.load_cookies()

if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

# Load saved products
PRODUCTS_FILE = Path('products.json')

def load_products():
    """Load products from file"""
    if PRODUCTS_FILE.exists():
        with open(PRODUCTS_FILE, 'r') as f:
            st.session_state.products = json.load(f)

def save_products():
    """Save products to file"""
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(st.session_state.products, f, indent=2)

def add_log(message, level="info"):
    """Add entry to log"""
    log_entry = {
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'message': message,
        'level': level
    }
    st.session_state.logs.insert(0, log_entry)  # Newest first

    # Keep only last 100 logs
    st.session_state.logs = st.session_state.logs[:100]

def check_product_stock(product):
    """Check stock for a single product"""
    monitor = st.session_state.monitor

    try:
        stock_info = monitor.check_stock_pdp_api(product['item_id'])

        if stock_info:
            product['name'] = stock_info['name'][:50]
            product['price'] = stock_info['price']
            product['in_stock'] = stock_info['in_stock']
            product['last_check'] = datetime.now().strftime('%H:%M:%S')

            # Check for status change
            if 'prev_status' in product and product['prev_status'] != stock_info['in_stock']:
                if stock_info['in_stock']:
                    add_log(f"🔥 {product['name']} - NOW IN STOCK!", "success")
                else:
                    add_log(f"⚠️  {product['name']} - Out of stock", "warning")

            product['prev_status'] = stock_info['in_stock']

            # Count SKUs
            product['sku_count'] = len(stock_info['skus'])

            # Get available quantities
            available_skus = [sku for sku in stock_info['skus'] if sku['available']]
            if available_skus:
                product['quantity'] = sum(sku.get('stock', 0) for sku in available_skus)
            else:
                product['quantity'] = 0

            return True
        else:
            add_log(f"❌ Failed to check {product.get('name', product['item_id'])}", "error")
            return False

    except Exception as e:
        add_log(f"❌ Error checking {product.get('name', product['item_id'])}: {str(e)}", "error")
        return False

# Load products on startup
if not st.session_state.products:
    load_products()

# Header
st.title("📊 Lazada Stock Monitor")
st.markdown("Real-time multi-product stock monitoring")

# Sidebar - Add Products
with st.sidebar:
    st.header("➕ Add Product")

    with st.form("add_product_form"):
        product_url = st.text_input(
            "Lazada Product URL",
            placeholder="https://www.lazada.sg/products/...-i123456789.html"
        )

        submit = st.form_submit_button("Add Product")

        if submit and product_url:
            # Parse URL
            info = st.session_state.monitor.get_product_info(product_url)

            if info:
                # Check if already exists
                existing = any(p['item_id'] == info['item_id'] for p in st.session_state.products)

                if existing:
                    st.error("Product already in watchlist!")
                else:
                    new_product = {
                        'item_id': info['item_id'],
                        'sku_id': info['sku_id'],
                        'url': product_url,
                        'name': 'Loading...',
                        'price': 'N/A',
                        'in_stock': False,
                        'last_check': 'Never',
                        'sku_count': 0,
                        'quantity': 0
                    }

                    st.session_state.products.append(new_product)
                    save_products()
                    add_log(f"✅ Added product: {info['item_id']}", "success")
                    st.success("Product added!")
                    st.rerun()
            else:
                st.error("Invalid URL format")

    st.markdown("---")

    # Monitoring controls
    st.header("⚙️ Monitoring")

    check_interval = st.slider(
        "Check interval (seconds)",
        min_value=1,
        max_value=10,
        value=2,
        help="How often to check stock"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start", disabled=st.session_state.monitoring or len(st.session_state.products) == 0):
            st.session_state.monitoring = True
            add_log("🚀 Monitoring started", "success")
            st.rerun()

    with col2:
        if st.button("⏸️ Stop", disabled=not st.session_state.monitoring):
            st.session_state.monitoring = False
            add_log("⏹️  Monitoring stopped", "info")
            st.rerun()

    if len(st.session_state.products) == 0:
        st.info("Add products to start monitoring")

    st.markdown("---")

    # Stats
    st.header("📈 Stats")
    total_products = len(st.session_state.products)
    in_stock = sum(1 for p in st.session_state.products if p.get('in_stock', False))

    st.metric("Total Products", total_products)
    st.metric("In Stock", in_stock)
    st.metric("Out of Stock", total_products - in_stock)

# Main content area
if len(st.session_state.products) == 0:
    st.info("👈 Add products from the sidebar to get started")
else:
    # Product table
    st.header("🛍️ Product Watchlist")

    # Convert to dataframe for display
    df_data = []
    for idx, product in enumerate(st.session_state.products):
        status = "✅ IN STOCK" if product.get('in_stock', False) else "❌ OUT OF STOCK"

        df_data.append({
            'Index': idx,
            'Status': status,
            'Product': product.get('name', 'Loading...'),
            'Price': product.get('price', 'N/A'),
            'Quantity': product.get('quantity', 0),
            'SKUs': product.get('sku_count', 0),
            'Last Check': product.get('last_check', 'Never'),
            'Item ID': product['item_id'],
        })

    df = pd.DataFrame(df_data)

    # Display table
    st.dataframe(
        df[['Status', 'Product', 'Price', 'Quantity', 'SKUs', 'Last Check', 'Item ID']],
        use_container_width=True,
        hide_index=True
    )

    # Action buttons
    st.subheader("🎯 Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Check All Now"):
            with st.spinner("Checking stock..."):
                for product in st.session_state.products:
                    check_product_stock(product)
                save_products()
                add_log(f"✅ Checked {len(st.session_state.products)} products", "info")
            st.rerun()

    with col2:
        remove_idx = st.number_input(
            "Remove product index",
            min_value=0,
            max_value=len(st.session_state.products) - 1,
            value=0
        )

        if st.button("🗑️ Remove"):
            removed = st.session_state.products.pop(remove_idx)
            save_products()
            add_log(f"🗑️  Removed: {removed.get('name', removed['item_id'])}", "info")
            st.rerun()

    with col3:
        if st.button("🧹 Clear All"):
            st.session_state.products = []
            save_products()
            add_log("🧹 Cleared all products", "info")
            st.rerun()

    # Export buttons
    st.subheader("💾 Export")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"lazada_stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("📥 Export to JSON"):
            json_data = json.dumps(st.session_state.products, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"lazada_stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Log section
st.markdown("---")
st.header("📝 Activity Log")

if st.session_state.logs:
    # Display logs
    log_df = pd.DataFrame(st.session_state.logs)

    # Color code by level
    def color_level(level):
        if level == 'success':
            return '🟢'
        elif level == 'warning':
            return '🟡'
        elif level == 'error':
            return '🔴'
        else:
            return '⚪'

    log_df[''] = log_df['level'].apply(color_level)

    st.dataframe(
        log_df[['', 'timestamp', 'message']],
        use_container_width=True,
        hide_index=True,
        height=300
    )

    if st.button("🧹 Clear Logs"):
        st.session_state.logs = []
        st.rerun()
else:
    st.info("No activity yet. Add products and start monitoring!")

# Auto-refresh when monitoring
if st.session_state.monitoring:
    st.info(f"🔄 Monitoring active - checking every {check_interval} seconds")

    # Check all products
    for product in st.session_state.products:
        check_product_stock(product)

    save_products()

    # Wait and refresh
    time.sleep(check_interval)
    st.rerun()

# Footer
st.markdown("---")
st.caption("📊 Lazada Stock Monitor | Made with Streamlit")
