# Catalog Maker – High-Speed Product Catalog Platform

## 1. Project Overview

Catalog Maker is a reusable, mobile-friendly product catalog platform built using **Python, Streamlit, and SQLite**.

The system imports product information from multiple e-commerce sources into a centralized database and provides a fast catalog interface for customers and an admin panel for managing products.

For this demonstration, **Shopify and WooCommerce imports are simulated locally** because live API credentials were not provided.

---

## 2. Objectives

* Create a centralized product catalog.
* Import products from Shopify and WooCommerce sources.
* Store normalized product information in SQLite.
* Provide fast product browsing and searching.
* Support product management through an admin panel.
* Provide two different catalog designs.
* Support wishlist and WhatsApp enquiries.
* Maintain synchronization history.

---

## 3. Technology Stack

| Component                | Technology |
| ------------------------ | ---------- |
| Frontend/UI              | Streamlit  |
| Backend                  | Python     |
| Database                 | SQLite     |
| Data Processing          | Pandas     |
| HTTP/Integration Support | Requests   |
| Image Handling           | Image URLs |
| Communication            | WhatsApp   |
| Development              | VS Code    |

---

## 4. System Architecture

```text
        Shopify / WooCommerce
                 ↓
          Import / Sync Engine
                 ↓
          Central SQLite DB
                 ↓
       Internal Catalog Layer
                 ↓
           Streamlit UI
          ↙           ↘
     Customer          Admin
      Catalog           Panel
```

The central database separates the product catalog from external sources.

---

## 5. Project Structure

```text
Catalog_Maker/
│
├── app.py
├── database1.py
├── requirements.txt
├── README.md
└── catalog.db
```

### `app.py`

Contains the Streamlit customer catalog and admin panel.

### `database1.py`

Contains SQLite database creation and database operations.

### `catalog.db`

SQLite database containing products, categories, settings, and synchronization logs.

---

## 6. Main Features

### Customer Catalog

* Product browsing
* Product search
* Category filtering
* Availability filtering
* Product details
* Product images
* Larger image view
* Wishlist
* Multi-product selection
* WhatsApp enquiry
* Mobile-friendly interface

### Admin Panel

* Dashboard
* Product management
* Add/edit/delete products
* Category management
* Shopify demo import
* WooCommerce demo import
* Product synchronization
* Simulated source updates
* Sync history
* WhatsApp number configuration
* Catalog design selection

### Catalog Designs

The application supports two substantially different designs:

1. **Grid Design**
2. **Large Image Design**

Both designs use the same centralized database.

---

## 7. Product Data

Each product can contain:

* Product name
* SKU
* Price
* Description
* Category
* Image URL
* Product URL
* Stock
* Availability
* Source
* Source ID
* Last updated time

---

## 8. Demo Data

The application supports:

* 50 Shopify demo products
* 50 WooCommerce demo products

The products are imported into the same centralized SQLite database.

Example:

```text
Shopify → 50 products
WooCommerce → 50 products
                 ↓
          Central Database
                 ↓
          Customer Catalog
```

---

## 9. Synchronization

The synchronization module demonstrates:

* New product import
* Existing product updates
* Price changes
* Stock changes
* Source-based synchronization
* Synchronization history

The application also provides a **Simulate Source Update** option to demonstrate how a source change can be reflected in the central catalog.

Failed or unavailable external sources do not require deleting existing catalog data.

---

## 10. WhatsApp Enquiry

Customers can select multiple products and generate a pre-filled WhatsApp enquiry.

Example message:

```text
Hi, I am interested in the following products:

- Product 1
- Product 2
- Product 3

Please share more details and pricing.
```

No cart or checkout system is required.

---

## 11. Wishlist

Users can add products to a wishlist while browsing the catalog.

The current implementation maintains wishlist state during the browsing session.

---

## 12. Performance Approach

The application is designed with a lightweight architecture to keep catalog navigation fast.

Performance-related features include:

* SQLite indexed/local database approach
* Minimal product data retrieval
* Search and filtering
* Image URLs instead of storing large image files
* Expandable product details
* Lightweight Streamlit interface
* Simple centralized data layer

---

## 13. Installation

### Step 1: Create virtual environment

```bash
python -m venv venv
```

### Step 2: Activate environment

Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run application

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 14. Demo Workflow

```text
Open Application
       ↓
Admin Dashboard
       ↓
Import Shopify Demo Data
       ↓
Import WooCommerce Demo Data
       ↓
Verify 100 Products
       ↓
Run Synchronization
       ↓
Show Sync History
       ↓
Change Catalog Design
       ↓
Customer Catalog
       ↓
Search / Filter
       ↓
Product Details
       ↓
Wishlist
       ↓
Multi-product Selection
       ↓
WhatsApp Enquiry
```

---

## 15. Demo Source Limitation

For this submission, live Shopify and WooCommerce API credentials were not available.

Therefore, the application demonstrates the **same normalized import and synchronization workflow using locally simulated Shopify and WooCommerce product data**.

The architecture is designed so that a real API connector can replace the demo import layer in a production deployment.

---

## 16. Future Enhancements

Possible future improvements include:

* Live Shopify API integration
* Live WooCommerce API integration
* Scheduled background synchronization
* Persistent browser-based wishlist
* Image optimization/CDN
* Redis caching
* REST API using FastAPI
* Cloud deployment
* PWA support
* Analytics
* Multiple client catalogs
* Recommendation engine

---

## 17. Conclusion

Catalog Maker provides a centralized and reusable product catalog system with product import, synchronization, administration, customer browsing, wishlist functionality, and WhatsApp enquiries.

The project demonstrates how products from different e-commerce sources can be normalized into a single catalog database and presented through multiple customer-facing designs.
