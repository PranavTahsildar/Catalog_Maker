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
        font-size: 16px;
        margin-bottom: 15px;
    }

    .product-box {
        padding: 15px;
        border: 1px solid #dddddd;
        border-radius: 12px;
        margin-bottom: 20px;
        background: white;
    }

    .price {
        font-size: 24px;
        font-weight: 700;
        margin-top: 5px;
    }

    .stock {
        font-weight: 600;
    }

    .small-text {
        color: #666;
        font-size: 14px;
    }

    .speed-info {
        color: #666;
        font-size: 14px;
        margin-bottom: 15px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
    }

    div[data-testid="stImage"] img {
        border-radius: 10px;
    }

    @media (max-width: 768px) {

        .main-title {
            font-size: 28px;
        }

        .subtitle {
            font-size: 14px;
        }

        .product-box {
            padding: 10px;
        }

        .price {
            font-size: 20px;
        }

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

    return pd.DataFrame(
        products,
        columns=columns
    )


def whatsapp_link(products):

    number = get_setting(
        "whatsapp",
        "919999999999"
    )

    message = (
        "Hi, I am interested in the following products:\n\n"
    )

    for i, product in enumerate(
        products,
        start=1
    ):

        message += (
            f"{i}. {product['name']} - "
            f"₹{float(product['price']):,.2f}\n"
        )

        if product["product_url"]:
            message += (
                f"{product['product_url']}\n"
            )

        message += "\n"

    message += (
        "Please share more details and pricing."
    )

    encoded_message = urllib.parse.quote(
        message
    )

    return (
        f"https://wa.me/{number}"
        f"?text={encoded_message}"
    )


def add_to_wishlist(product_id):

    if product_id not in st.session_state.wishlist:

        st.session_state.wishlist.append(
            product_id
        )

        return True

    return False


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

    st.markdown(
        '<div class="speed-info">'
        '⚡ Fast catalog • SQLite-powered database • '
        'Mobile-friendly interface'
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
        placeholder="Search by product name, SKU or category..."
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    categories = [
        "All"
    ] + get_categories()

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

    with st.spinner("Loading products..."):

        filtered = df.copy()

        if search:

            search_text = search.strip()

            filtered = filtered[
                filtered["name"].str.contains(
                    search_text,
                    case=False,
                    na=False
                )
                |
                filtered["sku"].str.contains(
                    search_text,
                    case=False,
                    na=False
                )
                |
                filtered["category"].str.contains(
                    search_text,
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
            f"💬 {len(selected_df)} product(s) selected for enquiry"
        )

        link = whatsapp_link(
            selected_df.to_dict("records")
        )

        st.markdown(
            f"[💬 Enquire About Selected Products]({link})"
        )

        if st.button(
            "Clear Selected Products"
        ):

            st.session_state.selected_products = []

            st.rerun()

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

        for start in range(
            0,
            len(filtered),
            3
        ):

            row = filtered.iloc[
                start:start + 3
            ]

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

                    # Product Image

                    if product["image_url"]:

                        st.image(
                            product["image_url"],
                            use_container_width=True
                        )

                        with st.expander(
                            "🔍 View Larger Image"
                        ):

                            st.image(
                                product["image_url"],
                                use_container_width=True
                            )

                    # Product Name

                    st.subheader(
                        product["name"]
                    )

                    # Price

                    st.markdown(
                        f'<div class="price">'
                        f'₹{float(product["price"]):,.2f}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # Category

                    st.caption(
                        f"Category: {product['category']}"
                    )

                    # Availability

                    if product["availability"] == "In Stock":

                        st.success(
                            f"✓ {product['availability']}"
                        )

                    else:

                        st.error(
                            f"✕ {product['availability']}"
                        )

                    # Wishlist

                    if st.button(
                        "❤️ Wishlist",
                        key=f"grid_wish_{product['id']}"
                    ):

                        if add_to_wishlist(
                            product["id"]
                        ):

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

                        st.write(
                            f"**Stock:** {product['stock']}"
                        )

                        st.write(
                            f"**Source:** {product['source']}"
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

                    with st.expander(
                        "🔍 View Larger Image"
                    ):

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
                    f'₹{float(product["price"]):,.2f}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.write(
                    f"**Category:** "
                    f"{product['category']}"
                )

                if product["availability"] == "In Stock":

                    st.success(
                        f"✓ {product['availability']}"
                    )

                else:

                    st.error(
                        f"✕ {product['availability']}"
                    )

                st.write(
                    product["description"]
                )

                st.write(
                    f"**SKU:** {product['sku']}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "❤️ Wishlist",
                        key=f"large_wish_{product['id']}"
                    ):

                        if add_to_wishlist(
                            product["id"]
                        ):

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

                if product["product_url"]:

                    st.markdown(
                        f"[View Source Product]"
                        f"({product['product_url']})"
                    )

            st.divider()


# ============================================================
# WISHLIST
# ============================================================

elif page == "Wishlist":

    st.title(
        "❤️ My Wishlist"
    )

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

        st.write(
            f"{len(wishlist_df)} saved product(s)"
        )

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

                st.markdown(
                    f"### ₹{float(product['price']):,.2f}"
                )

                st.write(
                    f"Category: {product['category']}"
                )

                st.write(
                    f"Availability: "
                    f"{product['availability']}"
                )

                if st.button(
                    "Remove",
                    key=f"remove_wish_{product['id']}"
                ):

                    st.session_state.wishlist.remove(
                        product["id"]
                    )

                    st.rerun()

            st.divider()


# ============================================================
# ADMIN PANEL
# ============================================================

elif page == "Admin Panel":

    st.title(
        "⚙️ Admin Panel"
    )

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
            df[
                df["source"] == "Shopify"
            ]
        )

        woo = len(
            df[
                df["source"] == "WooCommerce"
            ]
        )

        category_count = len(
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
            category_count
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
  Customer     Admin
            """
        )

        st.success(
            "Catalog system is operational."
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
                        "availability",
                        "stock"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader(
                "Edit Product"
            )

            product_options = {
                f"{row['id']} - {row['name']}":
                row["id"]
                for _, row in df.iterrows()
            }

            selected_label = st.selectbox(
                "Select Product",
                list(product_options.keys())
            )

            selected_id = product_options[
                selected_label
            ]

            selected_product = df[
                df["id"] == selected_id
            ].iloc[0]

            edit_name = st.text_input(
                "Product Name",
                value=str(
                    selected_product["name"]
                )
            )

            edit_price = st.number_input(
                "Price",
                min_value=0.0,
                value=float(
                    selected_product["price"]
                ),
                step=10.0
            )

            edit_category = st.text_input(
                "Category",
                value=str(
                    selected_product["category"]
                )
            )

            edit_description = st.text_area(
                "Description",
                value=str(
                    selected_product["description"]
                )
            )

            edit_stock = st.number_input(
                "Stock",
                min_value=0,
                value=int(
                    selected_product["stock"]
                ),
                step=1
            )

            edit_image = st.text_input(
                "Image URL",
                value=str(
                    selected_product["image_url"]
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Save Changes"
                ):

                    update_product(
                        int(selected_id),
                        edit_name,
                        edit_price,
                        edit_category,
                        edit_description,
                        edit_stock,
                        edit_image
                    )

                    st.success(
                        "Product updated successfully."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "🗑️ Delete Product"
                ):

                    delete_product(
                        int(selected_id)
                    )

                    if selected_id in st.session_state.wishlist:

                        st.session_state.wishlist.remove(
                            selected_id
                        )

                    if selected_id in st.session_state.selected_products:

                        st.session_state.selected_products.remove(
                            selected_id
                        )

                    st.success(
                        "Product deleted successfully."
                    )

                    st.rerun()

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

        st.divider()

        st.write(
            "Existing Categories"
        )

        existing_categories = get_categories()

        if existing_categories:

            for category in existing_categories:

                st.write(
                    f"• {category}"
                )

        else:

            st.info(
                "No categories available."
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

        if products_df.empty:

            shopify_count = 0
            woo_count = 0

        else:

            shopify_count = len(
                products_df[
                    products_df["source"] == "Shopify"
                ]
            )

            woo_count = len(
                products_df[
                    products_df["source"] == "WooCommerce"
                ]
            )

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # SHOPIFY IMPORT
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

                    products_to_add = (
                        50 - shopify_count
                    )

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
        # WOOCOMMERCE IMPORT
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

                    products_to_add = (
                        50 - woo_count
                    )

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

            total = len(
                updated_df
            )

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
                    "🔄 Sync Shopify"
                ):

                    updated = 0

                    try:

                        for _, product in shopify_df.iterrows():

                            new_price = (
                                float(product["price"]) + 10
                            )

                            update_product(
                                int(product["id"]),
                                product["name"],
                                new_price,
                                product["category"],
                                product["description"],
                                int(product["stock"]),
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
                            "Failed"
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
                    "🔄 Sync WooCommerce"
                ):

                    updated = 0

                    try:

                        for _, product in woo_df.iterrows():

                            new_price = (
                                float(product["price"]) + 15
                            )

                            update_product(
                                int(product["id"]),
                                product["name"],
                                new_price,
                                product["category"],
                                product["description"],
                                int(product["stock"]),
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
                            "Failed"
                        )

                        st.error(
                            f"WooCommerce synchronization failed: {e}"
                        )

            st.divider()

            # ------------------------------------------------
            # SIMULATE SOURCE UPDATE
            # ------------------------------------------------

            st.subheader(
                "🧪 Simulate Source Update"
            )

            st.write(
                "Simulate a price or stock change from an "
                "external Shopify or WooCommerce source."
            )

            source_choice = st.selectbox(
                "Select Source",
                [
                    "Shopify",
                    "WooCommerce"
                ],
                key="sync_source"
            )

            source_products = products_df[
                products_df["source"] == source_choice
            ]

            if not source_products.empty:

                selected_product = st.selectbox(
                    "Select Product",
                    source_products["name"].tolist(),
                    key="sync_product"
                )

                selected_row = source_products[
                    source_products["name"] == selected_product
                ].iloc[0]

                new_price = st.number_input(
                    "New Price",
                    min_value=0.0,
                    value=(
                        float(selected_row["price"]) + 100
                    ),
                    step=10.0,
                    key="sync_price"
                )

                new_stock = st.number_input(
                    "New Stock",
                    min_value=0,
                    value=(
                        int(selected_row["stock"]) + 5
                    ),
                    step=1,
                    key="sync_stock"
                )

                if st.button(
                    "Apply Simulated Source Change",
                    key="apply_source_change"
                ):

                    try:

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

                    except Exception as e:

                        st.error(
                            f"Unable to update product: {e}"
                        )

            st.divider()

            # ------------------------------------------------
            # SYNC HISTORY
            # ------------------------------------------------

            st.subheader(
                "📋 Sync History"
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

        st.caption(
            "Enter the number with country code. "
            "Example: 919876543210"
        )

        if st.button(
            "💾 Save WhatsApp Number"
        ):

            save_setting(
                "whatsapp",
                whatsapp
            )

            st.success(
                "WhatsApp number saved successfully."
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

        st.write(
            f"Current active design: **{current_design}**"
        )

        if st.button(
            "💾 Save Active Design"
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