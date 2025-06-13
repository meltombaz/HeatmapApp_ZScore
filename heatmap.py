import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Molecule Heatmap", layout="centered")

# Title
st.title("别忘了给我做生日面")

# File upload
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        if df.shape[1] < 2 or 'Molecule' not in df.columns:
            st.error("The file must have a 'Molecule' column and at least one numeric condition column.")
        else:
            # Reshape for seaborn
            data_long = pd.melt(df, id_vars='Molecule', var_name='Condition', value_name='Average Delta Z-Score')
            
            # Preserve original row (Molecule) order
            gene_order = df['Molecule'].tolist()
            
            # Pivot and preserve column order
            heatmap_data = data_long.pivot(index='Molecule', columns='Condition', values='Average Delta Z-Score')
            heatmap_data = heatmap_data.reindex(gene_order)  # Preserve row order
            original_col_order = [col for col in df.columns if col != 'Molecule']
            heatmap_data = heatmap_data[original_col_order]  # Preserve column order

            # User input for title
            custom_title = st.text_input("Enter a title for your heatmap:", value="Average Δ Z-Score Heatmap")

            # Plot
            plt.figure(figsize=(6, max(6, len(heatmap_data) * 0.25)))  # Dynamic height
            ax = sns.heatmap(
                heatmap_data,
                annot=heatmap_data.round(2),
                fmt='',
                cmap=sns.diverging_palette(240, 10, as_cmap=True),
                center=0,
                linewidths=0.5,
                cbar_kws={'label': 'Average ΔZ-Score'}
            )

            plt.title(custom_title, fontsize=14, fontweight='bold')
            plt.xticks(fontsize=10, fontfamily='sans-serif')
            plt.yticks(fontsize=10, fontfamily='sans-serif', rotation=0)
            plt.xlabel("", fontsize=12, fontweight='bold', fontfamily='sans-serif')
            plt.ylabel("", fontsize=12, fontweight='bold', fontfamily='sans-serif')
            plt.tight_layout()

            st.pyplot(plt)

            st.success("✅ Heatmap generated successfully!")

            # Show image at the bottom of the page
            st.markdown(
                """
                <div style="text-align: center; margin-top: 50px;">
                    <img src="https://i0.wp.com/msshiandmrhe.com/wp-content/uploads/2022/12/WeChat-Image_20221220155529.jpg?resize=800%2C840&ssl=1" 
                        alt="Birthday noodles" width="300" style="border-radius: 10px;">
                </div>
                """,
                unsafe_allow_html=True
            )


    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("Please upload an Excel file with gene expression data.")
