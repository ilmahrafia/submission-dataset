import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set judul dashboard
st.title("📊 Dashboard E-Commerce")

# Load dataset dari file yang diunggah
all_df = pd.read_csv("dashboard/all_data.csv")

# Mengonversi kolom tanggal jika tersedia
date_column = "order_purchase_timestamp"  # Ganti dengan nama kolom tanggal yang benar
if date_column in all_df.columns:
    all_df[date_column] = pd.to_datetime(all_df[date_column])

# Sidebar untuk memilih analisis
st.sidebar.header("📌 Pilih Analisis")
option = st.sidebar.radio("Pilih Data yang Ingin Ditampilkan", ["Seller dengan Pesanan Terbanyak", "Produk Paling Banyak Dibeli"])

# Filter berdasarkan rentang tanggal
if date_column in all_df.columns:
    min_date = all_df[date_column].min()
    max_date = all_df[date_column].max()
    date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)
    all_df = all_df[(all_df[date_column] >= pd.to_datetime(date_range[0])) & (all_df[date_column] <= pd.to_datetime(date_range[1]))]

# Filter berdasarkan kategori produk
if "product_category_name" in all_df.columns:
    categories = all_df["product_category_name"].dropna().unique()
    selected_categories = st.sidebar.multiselect(
        "Pilih Kategori Produk", 
        categories, 
        default=categories[:5]  # Menampilkan 5 kategori pertama sebagai default
    )
    all_df = all_df[all_df["product_category_name"].isin(selected_categories)]

# memilih seller dengan pesanan terbanyak
if option == "Seller dengan Pesanan Terbanyak":
    st.subheader("🏅 Seller dengan Pesanan Terbanyak")
    top_sellers = all_df['seller_id'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_sellers.index, y=top_sellers.values, palette="magma", ax=ax, legend=False)
    ax.set_xlabel("Seller ID")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Seller dengan Pesanan Terbanyak")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=10)
    st.pyplot(fig)

# memilih produk paling banyak dibeli
elif option == "Produk Paling Banyak Dibeli":
    st.subheader("🛒 Produk Paling Banyak Dibeli")
    top_products = all_df['product_category_name'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_products.values, y=top_products.index, palette="Blues_r", ax=ax, legend=False)
    ax.set_xlabel("Jumlah Dibeli")
    ax.set_ylabel("Nama Produk")
    ax.set_title("Produk Paling Banyak Dibeli")
    st.pyplot(fig)
