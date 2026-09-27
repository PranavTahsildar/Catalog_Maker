
import streamlit as st
import pandas as pd
import urllib.parse

from database1 import (
    init_db,
    add_product,
    get_products,
    delete_product,
    update_product,
    add_category,
    get_categories,
    save_setting,
    get_setting,
    add_sync_log,
    get_sync_logs
)


# ============================================================
# INITIALIZATION
# ============================================================

init_db()

st.set_page_config(
    page_title="Catalog Maker",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #666;
        margin-bottom: 25px;
    }

    .product-box {
        padding: 15px;
        border: 1px solid #dddddd;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    .price {
        font-size: 24px;
        font-weight: 700;
    }

    .stock {
        font-weight: 600;
    }

    .small-text {
        color: #666;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "selected_products" not in st.session_state:
    st.session_state.selected_products = []


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛍️ Catalog Maker")

st.sidebar.caption(
    "High-Speed Product Catalog Platform"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Customer Catalog",
        "Wishlist",
        "Admin Panel"
    ]
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_product_dataframe():

    products = get_products()

    columns = [
        "id",
        "source",
        "source_id",
        "name",
        "sku",
        "price",
        "description",
        "category",
        "image_url",
        "product_url",
        "stock",
        "availability",
        "updated_at"
    ]

    return pd.DataFrame(products, columns=columns)


def whatsapp_link(products):

    number = get_setting(
        "whatsapp",
        "919999999999"
    )

    message = (
        "Hi, I am interested in the following products:\n\n"
    )

    for i, product in enumerate(products, start=1):

        message += (
            f"{i}. {product['name']} - "
            f"₹{product['price']:,.2f}\n"
        )

        if product["product_url"]:
            message += (
                f"{product['product_url']}\n"
            )

    message += (
        "\nPlease share more details and pricing."
    )

    encoded_message = urllib.parse.quote(message)

    return (
        f"https://wa.me/{number}"
        f"?text={encoded_message}"
    )


# ============================================================
# CUSTOMER CATALOG
# ============================================================

if page == "Customer Catalog":

    st.markdown(
        '<div class="main-title">🛍️ Catalog Maker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Browse our products and enquire directly on WhatsApp.'
        '</div>',
        unsafe_allow_html=True
    )

    df = get_product_dataframe()

    if df.empty:

        st.warning(
            "No products available. "
            "Go to Admin Panel → Import Demo Data."
        )

        st.stop()

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search = st.text_input(
        "🔍 Search products",
        placeholder="Search by product name..."
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    categories = ["All"] + get_categories()

    with col1:

        category = st.selectbox(
            "Category",
            categories
        )

    with col2:

        availability = st.selectbox(
            "Availability",
            [
                "All",
                "In Stock",
                "Out of Stock"
            ]
        )

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    filtered = df.copy()

    if search:

        filtered = filtered[
            filtered["name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if category != "All":

        filtered = filtered[
            filtered["category"] == category
        ]

    if availability != "All":

        filtered = filtered[
            filtered["availability"] == availability
        ]

    st.write(
        f"**{len(filtered)} products found**"
    )

    # --------------------------------------------------------
    # MULTI PRODUCT WHATSAPP
    # --------------------------------------------------------

    selected_ids = st.session_state.selected_products

    selected_df = df[
        df["id"].isin(selected_ids)
    ]

    if not selected_df.empty:

        st.info(
            f"{len(selected_df)} product(s) selected"
        )

        link = whatsapp_link(
            selected_df.to_dict("records")
        )

        st.markdown(
            f"[💬 Enquire About Selected Products]({link})"
        )

        st.divider()

    # --------------------------------------------------------
    # ACTIVE DESIGN
    # --------------------------------------------------------

    design = get_setting(
        "design",
        "Grid Design"
    )

    # ========================================================
    # DESIGN 1 - GRID
    # ========================================================

    if design == "Grid Design":

        st.subheader(
            "Featured Products"
        )

        rows = [
            filtered.iloc[i:i + 3]
            for i in range(
                0,
                len(filtered),
                3
            )
        ]

        for row in rows:

            cols = st.columns(3)

            for col, (_, product) in zip(
                cols,
                row.iterrows()
            ):

                with col:

                    st.markdown(
                        '<div class="product-box">',
                        unsafe_allow_html=True
                    )

                    if product["image_url"]:

                        st.image(
                            product["image_url"],
                            use_container_width=True
                        )

                    st.subheader(
                        product["name"]
                    )

                    st.markdown(
                        f'<div class="price">'
                        f'₹{product["price"]:,.2f}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.caption(
                        product["category"]
                    )

                    st.write(
                        product["availability"]
                    )

                    # Wishlist

                    if st.button(
                        "❤️ Wishlist",
                        key=f"grid_wish_{product['id']}"
                    ):

                        if product["id"] not in st.session_state.wishlist:

                            st.session_state.wishlist.append(
                                product["id"]
                            )

                            st.success(
                                "Added to wishlist"
                            )

                        else:

                            st.info(
                                "Already in wishlist"
                            )

                    # Selection

                    selected = st.checkbox(
                        "Select for enquiry",
                        key=f"grid_select_{product['id']}"
                    )

                    if selected:

                        if product["id"] not in st.session_state.selected_products:

                            st.session_state.selected_products.append(
                                product["id"]
                            )

                    else:

                        if product["id"] in st.session_state.selected_products:

                            st.session_state.selected_products.remove(
                                product["id"]
                            )

                    # Details

                    with st.expander(
                        "View Details"
                    ):

                        st.write(
                            product["description"]
                        )

                        st.write(
                            f"**SKU:** {product['sku']}"
                        )

                        if product["product_url"]:

                            st.markdown(
                                f"[View Source Product]"
                                f"({product['product_url']})"
                            )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

    # ========================================================
    # DESIGN 2 - LARGE IMAGE
    # ========================================================

    else:

        st.subheader(
            "Premium Catalog"
        )

        for _, product in filtered.iterrows():

            col1, col2 = st.columns(
                [1.5, 2]
            )

            with col1:

                if product["image_url"]:

                    st.image(
                        product["image_url"],
                        use_container_width=True
                    )

            with col2:

                st.subheader(
                    product["name"]
                )

                st.markdown(
                    f'<div class="price">'
                    f'₹{product["price"]:,.2f}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.write(
                    f"Category: {product['category']}"
                )

                st.write(
                    f"Availability: "
                    f"{product['availability']}"
                )

                st.write(
                    product["description"]
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "❤️ Wishlist",
                        key=f"large_wish_{product['id']}"
                    ):

                        if product["id"] not in st.session_state.wishlist:

                            st.session_state.wishlist.append(
                                product["id"]
                            )

                            st.success(
                                "Added to wishlist"
                            )

                        else:

                            st.info(
                                "Already in wishlist"
                            )

                with c2:

                    selected = st.checkbox(
                        "Select",
                        key=f"large_select_{product['id']}"
                    )

                    if selected:

                        if product["id"] not in st.session_state.selected_products:

                            st.session_state.selected_products.append(
                                product["id"]
                            )

                    else:

                        if product["id"] in st.session_state.selected_products:

                            st.session_state.selected_products.remove(
                                product["id"]
                            )

            st.divider()


# ============================================================
# WISHLIST
# ============================================================

elif page == "Wishlist":

    st.title("❤️ My Wishlist")

    df = get_product_dataframe()

    wishlist_df = df[
        df["id"].isin(
            st.session_state.wishlist
        )
    ]

    if wishlist_df.empty:

        st.info(
            "Your wishlist is empty."
        )

    else:

        for _, product in wishlist_df.iterrows():

            col1, col2 = st.columns(
                [1, 3]
            )

            with col1:

                if product["image_url"]:

                    st.image(
                        product["image_url"],
                        use_container_width=True
                    )

            with col2:

                st.subheader(
                    product["name"]
                )

                st.write(
                    f"₹{product['price']:,.2f}"
                )

                if st.button(
                    "Remove",
                    key=f"remove_wish_{product['id']}"
                ):

                    st.session_state.wishlist.remove(
                        product["id"]
                    )

                    st.rerun()


# ============================================================
# ADMIN PANEL
# ============================================================

elif page == "Admin Panel":

    st.title("⚙️ Admin Panel")

    admin_page = st.selectbox(
        "Admin Section",
        [
            "Dashboard",
            "Products",
            "Categories",
            "Import Demo Data",
            "Synchronization",
            "Settings",
            "Catalog Design"
        ]
    )

    # ========================================================
    # DASHBOARD
    # ========================================================

    if admin_page == "Dashboard":

        df = get_product_dataframe()

        total = len(df)

        shopify = len(
            df[df["source"] == "Shopify"]
        )

        woo = len(
            df[df["source"] == "WooCommerce"]
        )

        categories = len(
            get_categories()
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Products",
            total
        )

        c2.metric(
            "Shopify",
            shopify
        )

        c3.metric(
            "WooCommerce",
            woo
        )

        c4.metric(
            "Categories",
            categories
        )

        st.subheader(
            "System Architecture"
        )

        st.code(
            """
Shopify / WooCommerce
          ↓
     Import Engine
          ↓
      SQLite DB
          ↓
  Internal Catalog Layer
          ↓
      Streamlit UI
       ↙       ↘
   Customer    Admin
            """
        )

    # ========================================================
    # PRODUCTS
    # ========================================================

    elif admin_page == "Products":

        st.subheader(
            "Product Management"
        )

        df = get_product_dataframe()

        if df.empty:

            st.info(
                "No products available."
            )

        else:

            st.dataframe(
                df[
                    [
                        "id",
                        "source",
                        "name",
                        "sku",
                        "price",
                        "category",
                        "availability"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    # ========================================================
    # CATEGORIES
    # ========================================================

    elif admin_page == "Categories":

        st.subheader(
            "Category Management"
        )

        new_category = st.text_input(
            "Enter new category"
        )

        if st.button(
            "➕ Add Category"
        ):

            if new_category.strip():

                add_category(
                    new_category.strip()
                )

                st.success(
                    "Category added."
                )

                st.rerun()

            else:

                st.warning(
                    "Please enter a category name."
                )

        st.write(
            "Existing Categories"
        )

        for category in get_categories():

            st.write(
                f"• {category}"
            )

    # ========================================================
    # IMPORT DEMO DATA
    # ========================================================

    elif admin_page == "Import Demo Data":

        st.header(
            "Import Products"
        )

        st.info(
            "Demo mode is enabled because no Shopify or "
            "WooCommerce API credentials are configured. "
            "Products are imported into the central SQLite database."
        )

        products_df = get_product_dataframe()

        shopify_count = (
            len(
                products_df[
                    products_df["source"] == "Shopify"
                ]
            )
            if not products_df.empty
            else 0
        )

        woo_count = (
            len(
                products_df[
                    products_df["source"] == "WooCommerce"
                ]
            )
            if not products_df.empty
            else 0
        )

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # SHOPIFY
        # ----------------------------------------------------

        with col1:

            st.subheader(
                "Shopify"
            )

            st.metric(
                "Products",
                shopify_count
            )

            if st.button(
                "Import Shopify Demo Products"
            ):

                if shopify_count >= 50:

                    st.success(
                        "Shopify already contains "
                        "50 or more products."
                    )

                else:

                    products_to_add = 50 - shopify_count

                    for i in range(
                        shopify_count + 1,
                        51
                    ):

                        add_product(
                            source="Shopify",
                            source_id=f"shopify_demo_{i}",
                            name=f"Shopify Product {i}",
                            sku=f"SHOP-{i:04d}",
                            price=499 + (i * 25),
                            description=f"Demo Shopify product {i}",
                            category=(
                                "Electronics"
                                if i % 2 == 0
                                else "Accessories"
                            ),
                            image_url=(
                                "https://images.unsplash.com/"
                                "photo-1523275335684-37898b6baf30"
                            ),
                            product_url=(
                                f"https://shopify-demo.example/"
                                f"product/{i}"
                            ),
                            stock=20 + i,
                            availability="In Stock"
                        )

                    add_sync_log(
                        "Shopify",
                        products_to_add,
                        0,
                        "Success"
                    )

                    st.success(
                        f"Shopify import completed. "
                        f"{products_to_add} products added."
                    )

                    st.rerun()

        # ----------------------------------------------------
        # WOOCOMMERCE
        # ----------------------------------------------------

        with col2:

            st.subheader(
                "WooCommerce"
            )

            st.metric(
                "Products",
                woo_count
            )

            if st.button(
                "Import WooCommerce Demo Products"
            ):

                if woo_count >= 50:

                    st.success(
                        "WooCommerce already contains "
                        "50 or more products."
                    )

                else:

                    products_to_add = 50 - woo_count

                    for i in range(
                        woo_count + 1,
                        51
                    ):

                        add_product(
                            source="WooCommerce",
                            source_id=f"woo_demo_{i}",
                            name=f"WooCommerce Product {i}",
                            sku=f"WOO-{i:04d}",
                            price=599 + (i * 30),
                            description=f"Demo WooCommerce product {i}",
                            category=(
                                "Fashion"
                                if i % 2 == 0
                                else "Home"
                            ),
                            image_url=(
                                "https://images.unsplash.com/"
                                "photo-1505740420928-5e560c06d30e"
                            ),
                            product_url=(
                                f"https://woocommerce-demo.example/"
                                f"product/{i}"
                            ),
                            stock=15 + i,
                            availability="In Stock"
                        )

                    add_sync_log(
                        "WooCommerce",
                        products_to_add,
                        0,
                        "Success"
                    )

                    st.success(
                        f"WooCommerce import completed. "
                        f"{products_to_add} products added."
                    )

                    st.rerun()

        # ----------------------------------------------------
        # CENTRAL DATABASE
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "Central Product Database"
        )

        updated_df = get_product_dataframe()

        if not updated_df.empty:

            shopify_total = len(
                updated_df[
                    updated_df["source"] == "Shopify"
                ]
            )

            woo_total = len(
                updated_df[
                    updated_df["source"] == "WooCommerce"
                ]
            )

            total = len(updated_df)

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Products",
                total
            )

            c2.metric(
                "Shopify",
                shopify_total
            )

            c3.metric(
                "WooCommerce",
                woo_total
            )

            st.dataframe(
                updated_df[
                    [
                        "id",
                        "source",
                        "name",
                        "sku",
                        "price",
                        "category",
                        "availability"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    # ========================================================
    # SYNCHRONIZATION
    # ========================================================

    elif admin_page == "Synchronization":

        st.header(
            "Synchronization"
        )

        st.info(
            "Demo synchronization simulates changes from "
            "Shopify and WooCommerce and updates the "
            "central SQLite catalog."
        )

        products_df = get_product_dataframe()

        if products_df.empty:

            st.warning(
                "No products available. "
                "Import demo products first."
            )

        else:

            shopify_df = products_df[
                products_df["source"] == "Shopify"
            ]

            woo_df = products_df[
                products_df["source"] == "WooCommerce"
            ]

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # SHOPIFY SYNC
            # ------------------------------------------------

            with col1:

                st.subheader(
                    "Shopify Sync"
                )

                st.metric(
                    "Shopify Products",
                    len(shopify_df)
                )

                if st.button(
                    "Sync Shopify"
                ):

                    updated = 0

                    try:

                        for _, product in shopify_df.iterrows():

                            new_price = (
                                float(product["price"]) + 10
                            )

                            update_product(
                                product["id"],
                                product["name"],
                                new_price,
                                product["category"],
                                product["description"],
                                product["stock"],
                                product["image_url"]
                            )

                            updated += 1

                        add_sync_log(
                            "Shopify",
                            0,
                            updated,
                            "Success"
                        )

                        st.success(
                            f"Shopify sync completed. "
                            f"{updated} products updated."
                        )

                        st.rerun()

                    except Exception as e:

                        add_sync_log(
                            "Shopify",
                            0,
                            updated,
                            f"Failed: {str(e)}"
                        )

                        st.error(
                            f"Shopify synchronization failed: {e}"
                        )

            # ------------------------------------------------
            # WOOCOMMERCE SYNC
            # ------------------------------------------------

            with col2:

                st.subheader(
                    "WooCommerce Sync"
                )

                st.metric(
                    "WooCommerce Products",
                    len(woo_df)
                )

                if st.button(
                    "Sync WooCommerce"
                ):

                    updated = 0

                    try:

                        for _, product in woo_df.iterrows():

                            new_price = (
                                float(product["price"]) + 15
                            )

                            update_product(
                                product["id"],
                                product["name"],
                                new_price,
                                product["category"],
                                product["description"],
                                product["stock"],
                                product["image_url"]
                            )

                            updated += 1

                        add_sync_log(
                            "WooCommerce",
                            0,
                            updated,
                            "Success"
                        )

                        st.success(
                            f"WooCommerce sync completed. "
                            f"{updated} products updated."
                        )

                        st.rerun()

                    except Exception as e:

                        add_sync_log(
                            "WooCommerce",
                            0,
                            updated,
                            f"Failed: {str(e)}"
                        )

                        st.error(
                            f"WooCommerce synchronization failed: {e}"
                        )

            st.divider()

            # ------------------------------------------------
            # SIMULATE SOURCE CHANGE
            # ------------------------------------------------

            st.subheader(
                "Simulate Source Update"
            )

            st.write(
                "Use this option to simulate a product price "
                "or stock change in the external source before "
                "running synchronization."
            )

            source_choice = st.selectbox(
                "Select Source",
                [
                    "Shopify",
                    "WooCommerce"
                ]
            )

            source_products = products_df[
                products_df["source"] == source_choice
            ]

            if not source_products.empty:

                selected_product = st.selectbox(
                    "Select Product",
                    source_products["name"].tolist()
                )

                selected_row = source_products[
                    source_products["name"] == selected_product
                ].iloc[0]

                new_price = st.number_input(
                    "New Price",
                    min_value=0.0,
                    value=float(selected_row["price"]) + 100,
                    step=10.0
                )

                new_stock = st.number_input(
                    "New Stock",
                    min_value=0,
                    value=int(selected_row["stock"]) + 5,
                    step=1
                )

                if st.button(
                    "Apply Simulated Source Change"
                ):

                    update_product(
                        int(selected_row["id"]),
                        selected_row["name"],
                        new_price,
                        selected_row["category"],
                        selected_row["description"],
                        new_stock,
                        selected_row["image_url"]
                    )

                    st.success(
                        f"{selected_product} updated successfully."
                    )

                    st.rerun()

            st.divider()

            # ------------------------------------------------
            # SYNC HISTORY
            # ------------------------------------------------

            st.subheader(
                "Sync History"
            )

            logs = get_sync_logs()

            if logs:

                logs_df = pd.DataFrame(
                    logs,
                    columns=[
                        "id",
                        "source",
                        "added",
                        "updated",
                        "status",
                        "sync_time"
                    ]
                )

                st.dataframe(
                    logs_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No synchronization history available."
                )

    # ========================================================
    # SETTINGS
    # ========================================================

    elif admin_page == "Settings":

        st.subheader(
            "⚙️ Catalog Settings"
        )

        whatsapp = st.text_input(
            "WhatsApp Number",
            get_setting(
                "whatsapp",
                "919999999999"
            )
        )

        if st.button(
            "Save WhatsApp Number"
        ):

            save_setting(
                "whatsapp",
                whatsapp
            )

            st.success(
                "WhatsApp number saved."
            )

    # ========================================================
    # CATALOG DESIGN
    # ========================================================

    elif admin_page == "Catalog Design":

        st.subheader(
            "🎨 Catalog Design"
        )

        current_design = get_setting(
            "design",
            "Grid Design"
        )

        design = st.radio(
            "Select Active Catalog Design",
            [
                "Grid Design",
                "Large Image Design"
            ],
            index=(
                0
                if current_design == "Grid Design"
                else 1
            )
        )

        if st.button(
            "Save Active Design"
        ):

            save_setting(
                "design",
                design
            )

            st.success(
                f"{design} is now active."
            )

            st.info(
                "Open Customer Catalog to view the design."
            )
 
