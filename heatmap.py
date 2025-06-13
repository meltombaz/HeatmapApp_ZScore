import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(page_title="Gene Expression Heatmap", layout="centered")
st.title("Heatmap Maker")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)

        # Validate structure
        if df.shape[1] < 2 or 'Gene' not in df.columns:
            st.error("The file must contain a 'Gene' column and at least one numeric condition column.")
        else:
            # Custom title input
            custom_title = st.text_input("Enter a title for your heatmap:", value="Zhuo Heatmap")

            # Clustering option
            cluster_rows = st.checkbox("Cluster (reorder) genes by similarity", value=False)

            # Prepare data
            data_long = pd.melt(df, id_vars='Gene', var_name='Condition', value_name='Expression')
            heatmap_data = data_long.pivot(index='Gene', columns='Condition', values='Expression')

            # Plot heatmap
            if cluster_rows:
                st.write("🔁 Clustering genes based on expression similarity...")
                g = sns.clustermap(
                    heatmap_data,
                    annot=heatmap_data.round(2),
                    fmt='',
                    cmap=sns.diverging_palette(240, 10, as_cmap=True),
                    center=0,
                    linewidths=0.5,
                    figsize=(6, max(6, len(heatmap_data) * 0.25)),
                    cbar_kws={'label': 'Expression'}
                )
                plt.title(custom_title, fontsize=14, fontweight='bold')
                st.pyplot(g.fig)
            else:
                st.write("📊 Keeping original gene order...")
                plt.figure(figsize=(6, max(6, len(heatmap_data) * 0.25)))
                ax = sns.heatmap(
                    heatmap_data,
                    annot=heatmap_data.round(2),
                    fmt='',
                    cmap=sns.diverging_palette(240, 10, as_cmap=True),
                    center=0,
                    linewidths=0.5,
                    cbar_kws={'label': 'Expression'}
                )
                plt.title(custom_title, fontsize=14, fontweight='bold')
                plt.xticks(fontsize=10, fontfamily='sans-serif')
                plt.yticks(fontsize=10, fontfamily='sans-serif', rotation=0)
                plt.xlabel("Condition", fontsize=12, fontweight='bold', fontfamily='sans-serif')
                plt.ylabel("Gene", fontsize=12, fontweight='bold', fontfamily='sans-serif')
                plt.tight_layout()
                st.pyplot(plt)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("Please upload an Excel file with gene expression data. First column = 'Gene', others = conditions.")
